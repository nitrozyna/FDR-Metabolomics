from matchms.similarity import CosineGreedy
from rdkit.Chem.inchi import InchiToInchiKey, MolToInchiKey
import bisect
from collections import namedtuple

Hit = namedtuple('Hit', ['query', 'target', 'score', 'hit'])


def inchis_equal(s1, s2):
    return s1.metadata['inchi'].split("/")[:4] == s2.metadata['inchi'].split("/")[:4]
    # return InchiToInchiKey(s1.metadata['inchi']).split('-')[0] == InchiToInchiKey(s2.metadata['inchi']).split('-')[0]


def get_hits(query_spec, library_spec, precursor_tol=1, metaKey='parent_mass', cosine_tol=0.1):
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
            found = False
            scores = []
            for l in library_spec[pos:pos2]:
                if inchis_equal(q, l):
                    found = True
                s, _ = cosine_greedy.pair(q, l)
                scores.append((s, l))
            # if all( s[0] == 0.0 for s in scores ):
            #    print(q.get('compound_name'))
            if found:
                scores.sort(key=lambda x: x[0], reverse=True)
                # query, target, best cosine score, hit_true
                hits.append(Hit(q, scores[0][1], scores[0][0], inchis_equal(q, scores[0][1])))
            else:
                misses.append(q)
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
