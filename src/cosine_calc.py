from matchms.similarity import CosineGreedy
from rdkit.Chem.inchi import InchiToInchiKey, MolToInchiKey
import bisect
from collections import namedtuple
import numpy as np

Hit = namedtuple('Hit', ['query', 'target', 'score', 'hit'])


def inchis_equal(s1, s2):
    return s1.metadata.get('inchi',"").split("/")[:4] == s2.metadata.get('inchi', "").split("/")[:4]
    # return InchiToInchiKey(s1.metadata['inchi']).split('-')[0] == InchiToInchiKey(s2.metadata['inchi']).split('-')[0]


def get_hits(query_spec, library_spec, precursor_tol=1, metaKey='parent_mass', cosine_tol=0.1, decoys=False, include_impossible_hits=True):
    cosine_greedy = CosineGreedy(tolerance=cosine_tol)
    library_spec.sort(key=lambda x: x.metadata[metaKey])
    hits = []
    misses = []
    library_prec_list = [x.metadata[metaKey] for x in library_spec]
    for q in query_spec:
        if metaKey not in q.metadata:
            continue
        min_mz = q.metadata[metaKey] - precursor_tol
        max_mz = q.metadata[metaKey] + precursor_tol
        pos = bisect.bisect_right(library_prec_list, min_mz)
        pos2 = pos
        while pos2 < len(library_prec_list) and library_prec_list[pos2] < max_mz:
            pos2 += 1
        if pos == pos2:
            # nothing in precursor range
            misses.append(q)
        else:
            found = decoys
            scores = []
            for l in library_spec[pos:pos2]:
                if inchis_equal(q, l):
                    found = True
                s, _ = cosine_greedy.pair(q, l)
                if s != s:
                    print('got nan for', q.get('compound_name'))
                    continue
                scores.append((s, l))
            # if all( s[0] == 0.0 for s in scores ):
            #    print(q.get('compound_name'))
            scores.sort(key=lambda x: x[0], reverse=True)
            score, target = scores[0]
            if found:
                if decoys:
                    hits.append(Hit(q, target, score, 'decoy'))
                else:
                    hits.append(Hit(q, target, score, inchis_equal(q, scores[0][1])))
            else:
                misses.append(q)
                if include_impossible_hits:
                    hits.append(Hit(q, target, score, False))
    return hits, misses


def add_exact_mass(specs):
    from rdkit.Chem import MolFromSmiles, MolToSmiles, MolFromInchi
    from rdkit.Chem.rdMolDescriptors import CalcExactMolWt, CalcMolFormula
    for s in specs:
        mol = MolFromSmiles(s.get('smiles'))
        if mol is None:
            mol = MolFromInchi(s.get('inchi'))
        exact_mass_smi = CalcExactMolWt(mol)
        if abs(exact_mass_smi - s.get('parent_mass', 0.0) > 1):
            print(exact_mass_smi, s.get('parent_mass'))

        s.set('exact_mass', exact_mass_smi)
