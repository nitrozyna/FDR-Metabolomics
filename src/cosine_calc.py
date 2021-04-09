import bisect
from collections import namedtuple

import numpy as np
from matchms.similarity import CosineGreedy
from rdkit.Chem import MolFromSmiles, MolFromInchi
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt
from spec2vec.vector_operations import calc_vector, cosine_similarity_matrix

Hit = namedtuple('Hit', ['query', 'target', 'score', 'hit'])


def inchis_equal(s1, s2, spec2vec=False):
    meta1 = getMeta(s1, spec2vec)
    meta2 = getMeta(s2, spec2vec)
    return meta1.get('inchikey', meta1.get('inchikey_inchi', '')).split("-")[0] == \
           meta2.get('inchikey', meta2.get('inchikey_inchi', '')).split("-")[0]


def passatutto_inchis_equal(s1, s2, spec2vec=False):
    return getMeta(s1, spec2vec).get('inchi', "").split("/")[:4] == \
           getMeta(s2, spec2vec).get('inchi', "").split("/")[:4]


def getMeta(spec, spec2vec=False):
    if spec2vec:
        return spec._obj.metadata
    else:
        return spec.metadata


def get_spec2vec_hits(documents_query, documents_lib, model, precursor_tol=1,
                      metaKey='parent_mass', decoys=False, passatutto=False,
                      intensity_weighting_power=0, allowed_missing_percentage=0,
                      embeddings_query=None, embeddings_library=None):
    if embeddings_query is None:
        embeddings_query = np.zeros((len(documents_query), model.vector_size), dtype="float")
        for i, q in enumerate(documents_query):
            embeddings_query[i, 0:model.vector_size] = calc_vector(model, q,
                                                                   intensity_weighting_power=intensity_weighting_power,
                                                                   allowed_missing_percentage=allowed_missing_percentage)
    if embeddings_library is None:
        embeddings_library = np.zeros((len(documents_lib), model.vector_size), dtype="float")
        if decoys:
            for i, l in enumerate(documents_lib):
                embeddings_library[i, 0:model.vector_size] = l._obj.metadata['vector']
        else:
            for i, l in enumerate(documents_lib):
                embeddings_library[i, 0:model.vector_size] = calc_vector(model, l,
                                                                         intensity_weighting_power=intensity_weighting_power,
                                                                         allowed_missing_percentage=allowed_missing_percentage)
    hits = []
    for q_idx, query in enumerate(documents_query):
        if metaKey not in query._obj.metadata:
            continue
        min_mz = query._obj.metadata[metaKey] - precursor_tol
        max_mz = query._obj.metadata[metaKey] + precursor_tol
        l_idxs = []
        for l_idx, doc_lib in enumerate(documents_lib):
            if min_mz <= doc_lib._obj.metadata[metaKey] <= max_mz:
                l_idxs.append(l_idx)
        if not l_idxs:
            continue

        embeddings_lib = np.zeros((len(l_idxs), model.vector_size), dtype="float")
        for i, l_idx in enumerate(l_idxs):
            embeddings_lib[i] = embeddings_library[l_idx]

        scores_for_query = cosine_similarity_matrix(embeddings_query[q_idx:q_idx + 1], embeddings_lib)[0]
        best_score = max(scores_for_query)
        idxs = [idx for idx, score in enumerate(scores_for_query) if score == best_score]
        if len(idxs) != 1:
            print("tie between %s for query %s", idxs, query)
        target = documents_lib[l_idxs[idxs[0]]]
        if decoys:
            hits.append(Hit(query, target, best_score, 'decoy'))
        else:
            if passatutto:
                hits.append(Hit(query, target, best_score, passatutto_inchis_equal(query, target, model)))
            else:
                hits.append(Hit(query, target, best_score, inchis_equal(query, target, model)))
    return hits


def get_hits(query_spec, library_spec, precursor_tol=1, metaKey='parent_mass', cosine_tol=0.1, decoys=False,
             passatutto=False, min_match_count=6):
    cosine = CosineGreedy(tolerance=cosine_tol)
    library_spec.sort(key=lambda x: getMeta(x)[metaKey])

    hits = []
    library_prec_list = [getMeta(x)[metaKey] for x in library_spec]
    for q_idx, q in enumerate(query_spec):
        if metaKey not in getMeta(q):
            continue
        min_mz = getMeta(q)[metaKey] - precursor_tol
        max_mz = getMeta(q)[metaKey] + precursor_tol
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
            score, match_count = cosine.pair(q, l).item()
            if score != score:
                print('got nan for', q.get('compound_name'), l.get('compound_name'))
                continue
            if match_count >= min_match_count:
                scores.append((score, l))
        scores.sort(key=lambda x: x[0], reverse=True)
        if scores:
            score, target = scores[0]
            if decoys:
                hits.append(Hit(q, target, score, 'decoy'))
            else:
                if passatutto:
                    hits.append(Hit(q, target, score, passatutto_inchis_equal(q, target)))
                else:
                    hits.append(Hit(q, target, score, inchis_equal(q, target)))
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
