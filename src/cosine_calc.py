import bisect
from collections import namedtuple

from matchms.similarity import CosineGreedy
from rdkit.Chem import MolFromSmiles, MolFromInchi
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt
from spec2vec.vector_operations import calc_vector, cosine_similarity

Hit = namedtuple('Hit', ['query', 'target', 'score', 'hit'])


def inchis_equal(s1, s2, spec2vec=False):
    return getMeta(s1, spec2vec).get('inchikey_inchi', "").split("-")[0] == \
           getMeta(s2, spec2vec).get('inchikey_inchi', "").split("-")[0]


def passatutto_inchis_equal(s1, s2, spec2vec=False):
    return getMeta(s1, spec2vec).get('inchi', "").split("/")[:4] == \
           getMeta(s2, spec2vec).get('inchi', "").split("/")[:4]


def getMeta(spec, spec2vec=False):
    if spec2vec:
        return spec._obj.metadata
    else:
        return spec.metadata


def get_hits(query_spec, library_spec, precursor_tol=1, metaKey='parent_mass', cosine_tol=0.1, decoys=False,
             spec2vec_model=None,
             intensity_weighting_power=0,
             allowed_missing_percentage=0, passatutto=False):
    if spec2vec_model is None:
        cosine = CosineGreedy(tolerance=cosine_tol)
    library_spec.sort(key=lambda x: getMeta(x, spec2vec_model)[metaKey])

    if spec2vec_model:
        ref_vectors = []
        query_vectors = []
        for q in query_spec:
            query_vectors.append(calc_vector(spec2vec_model, q,
                                             intensity_weighting_power=intensity_weighting_power,
                                             allowed_missing_percentage=allowed_missing_percentage))
        for l in library_spec:
            ref_vectors.append(calc_vector(spec2vec_model, l,
                                           intensity_weighting_power=intensity_weighting_power,
                                           allowed_missing_percentage=allowed_missing_percentage))

    hits = []
    library_prec_list = [getMeta(x, spec2vec_model)[metaKey] for x in library_spec]
    for q_idx, q in enumerate(query_spec):
        if metaKey not in getMeta(q, spec2vec_model):
            continue
        min_mz = getMeta(q, spec2vec_model)[metaKey] - precursor_tol
        max_mz = getMeta(q, spec2vec_model)[metaKey] + precursor_tol
        pos = bisect.bisect_right(library_prec_list, min_mz)
        pos2 = pos
        while pos2 < len(library_prec_list) and library_prec_list[pos2] < max_mz:
            pos2 += 1
        # nothing in precursor range
        if pos == pos2:
            continue
        scores = []
        for l_idx in range(pos, pos2):
            l = library_spec[l_idx]
            if spec2vec_model:
                if decoys:
                    reference_vector = l._obj.metadata['vector']
                else:
                    reference_vector = ref_vectors[l_idx]
                query_vector = query_vectors[q_idx]
                score = cosine_similarity(reference_vector, query_vector)
            else:
                score, match_count = cosine.pair(q, l)
            if score != score:
                print('got nan for', q.get('compound_name'))
                continue
            if spec2vec_model is not None or match_count >= 6:
                scores.append((score, l))
        scores.sort(key=lambda x: x[0], reverse=True)
        if scores:
            score, target = scores[0]
            if decoys:
                hits.append(Hit(q, target, score, 'decoy'))
            else:
                if passatutto:
                    hits.append(Hit(q, target, score, passatutto_inchis_equal(q, scores[0][1], spec2vec_model)))
                else:
                    hits.append(Hit(q, target, score, inchis_equal(q, scores[0][1], spec2vec_model)))
    return hits


def add_exact_mass(specs):
    for s in specs:
        mol = MolFromSmiles(s.get('smiles'))
        if mol is None:
            mol = MolFromInchi(s.get('inchi'))
        exact_mass_smi = CalcExactMolWt(mol)
        if abs(exact_mass_smi - s.get('parent_mass', 0.0) > 1):
            print(exact_mass_smi, s.get('parent_mass'))
        s.set('exact_mass', exact_mass_smi)
