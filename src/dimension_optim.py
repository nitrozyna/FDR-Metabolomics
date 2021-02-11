import cosine_calc
import gensim
import matplotlib.pyplot as plt
import numpy as np
import os
from matchms.importing import load_from_json
from spec2vec.SpectrumDocument import SpectrumDocument


json_file_name = 'C:\\Users\\Gosia\\Desktop\\FDR-datsets\\specs.json'
spec_with_precursor = load_from_json(json_file_name)

inchi_dict = {}
for s in spec_with_precursor:
    ik = s.metadata['inchikey_inchi']
    init_ik = ik.split('-')[0]
    if not init_ik in inchi_dict:
        inchi_dict[init_ik] = [s]
    else:
        inchi_dict[init_ik].append(s)

documents_query = []
documents_lib = []
spectrums_lib = []
spectrums_query = []


def init(query_size=1500, library_size=2500, unseen_query_size=500, unique_match=True):
    global documents_query
    global documents_lib
    global spectrums_lib
    global spectrums_query
    singletons = set([i for i, v in inchi_dict.items() if len(v) == 1])
    multis = set([i for i, v in inchi_dict.items() if len(v) > 1])

    matching_keys = np.random.choice(list(multis), size=query_size - unseen_query_size, replace=False)
    other_keys = np.random.choice(list(singletons), size=library_size - query_size + 2 * unseen_query_size,
                                  replace=False)

    query_spec = []
    library_spec = []
    for q in matching_keys:
        ss = np.random.choice(inchi_dict[q], size=2, replace=False)
        query_spec.append(ss[0])
        if unique_match:
            library_spec.append(ss[1])
        else:
            for s_ in ss[1:]:
                library_spec.append(s_)
    for i, o in enumerate(other_keys):
        ss = np.random.choice(inchi_dict[o], size=1, replace=False)
        if i < unseen_query_size:
            query_spec.append(ss[0])
        else:
            library_spec.append(ss[0])

    assert len(query_spec) == query_size

    spectrums_lib = library_spec
    spectrums_query = query_spec

    documents_query = [SpectrumDocument(s, n_decimals=2) for s in spectrums_query]
    documents_lib = [SpectrumDocument(s, n_decimals=2) for s in spectrums_lib]


folder_name = 'C:\\Users\\Gosia\\Desktop'
path_models = os.path.join(folder_name, "trained_models_1")


def f(size, intensity_weighting_power=0.5, allowed_missing_percentage=15):
    #model_file = os.path.join(path_models, "spec2vec_librarymatching_size_%d.model" % size)
    iterations = [1, 3, 5, 10]

    # Train model with size 10 and default parameters
    from spec2vec.vector_operations import calc_vector
    model_file = os.path.join(path_models, "spec2vec_size_%d.model"%size)

    # Load pretrained model
    model = gensim.models.Word2Vec.load(model_file)

    cos_hits, _ = cosine_calc.get_hits(spectrums_query, spectrums_lib, cosine_tol=.005)
    hits, _ = cosine_calc.get_hits(documents_query, documents_lib, spec2vec_model=model,
                                   intensity_weighting_power=intensity_weighting_power,
                                   allowed_missing_percentage=allowed_missing_percentage)

    test_matches_cos = []
    test_matches_s2v = []

    thresholds = np.array([x / 20 for x in range(0,20)]+[.98,.99,.997,.999])

    # for every query
    # find its 'hit'
    # if True match, 1
    # if False match, 0
    # otherwise, -1

    cos_hit_dict = {hit.query.metadata['spectrum_id']: hit for hit in cos_hits}
    hit_dict = {hit.query: hit for hit in hits}

    for threshold in thresholds:
        print(f"Checking matches for spec2vec score > {threshold:.2f}")
        test_matches = []
        for spec in spectrums_query:
            if spec.metadata['spectrum_id'] in cos_hit_dict and cos_hit_dict[spec.metadata['spectrum_id']].score > threshold:
                test_matches.append(1 * cos_hit_dict[spec.metadata['spectrum_id']].hit)
            else:
                test_matches.append(-1)
        # Make arrays from lists:
        test_arr = np.array(test_matches)
        test_matches_cos.append([np.sum(test_arr == 1), np.sum(test_arr == 0), np.sum(test_arr == -1)])

        test_matches = []
        for doc in documents_query:
            if doc in hit_dict and hit_dict[doc].score > threshold:
                hit = hit_dict[doc]
                test_matches.append(1 * hit.hit)
            else:
                test_matches.append(-1)

        # Make arrays from lists:
        test_arr = np.array(test_matches)
        test_matches_s2v.append([np.sum(test_arr == 1), np.sum(test_arr == 0), np.sum(test_arr == -1)])

    min_match = 6
    test_matches_cos_arr = np.array(test_matches_cos)
    test_matches_s2v_arr = np.array(test_matches_s2v)

    label_picks = [0, 4, 8, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    plt.figure(figsize=(7, 6))
    plt.style.use('ggplot')
    num_max_cos = np.sum(test_matches_cos_arr[0, :])
    num_max = np.sum(test_matches_s2v_arr[0, :])

    plt.plot(test_matches_cos_arr[:, 1] / num_max_cos, test_matches_cos_arr[:, 0] / num_max_cos,
             'o-', color='black', label='Cosine')

    plt.plot(test_matches_s2v_arr[:, 1] / num_max, test_matches_s2v_arr[:, 0] / num_max,
             'o-', label='Spec2Vec')

    for i, threshold in enumerate(thresholds):
        if i in label_picks:
            plt.annotate(">{:.2}".format(threshold),
                         (test_matches_cos_arr[i, 1] / num_max_cos, test_matches_cos_arr[i, 0] / num_max_cos),
                         textcoords="offset points", xytext=(2, -10), fontsize=12)
            plt.annotate(">{:.2}".format(threshold),
                         (test_matches_s2v_arr[i, 1] / num_max, test_matches_s2v_arr[i, 0] / num_max),
                         textcoords="offset points", xytext=(2, -10), fontsize=12)

    # plt.plot(test_matches_ROC_min2_arr[:,1]/num_max, test_matches_ROC_min2_arr[:,0]/num_max,
    #         '.--', color='black', alpha=0.5, label='cosine (min match = 2)')

    plt.title('true/false positives per query')
    plt.legend(fontsize=14)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('false positives rate', fontsize=16)
    plt.ylabel('true positive rate', fontsize=16)
    plt.xlim(0,.8)
    plt.ylim(0,.5)

    filename2 = "tfr_%d_%.2f_%.2f.png" % (size, intensity_weighting_power, allowed_missing_percentage)
    plt.savefig(os.path.join(folder_name, 'FDR-Metabolomics', 'data', 'opt_lcms_dim', filename2))
