import cosine_calc
import gensim
import matplotlib.pyplot as plt
import numpy as np
import os
from matchms.filtering import normalize_intensities
from matchms.importing import load_from_json
from spec2vec import SpectrumDocument

def post_process(s):
    s = normalize_intensities(s)
    # s = select_by_mz(s, mz_from=0, mz_to=1000)
    # s = require_minimum_number_of_peaks(s, n_required=10)
    return s


documents_query = []
documents_lib = []
spectrums_lib = []
spectrums_query = []


def init(query_size=1000, min_identical_matches=1, spec2vec_decimal_places=2,
         folder_name='C:\\Users\\Gosia\\Desktop'):
    global documents_query
    global documents_lib
    global spectrums_lib
    global spectrums_query

    spec_with_precursor = load_from_json(
        r'C:\Users\Gosia\Desktop\gnps_positive_ionmode_cleaned_by_matchms_and_lookups.json')
    # apply post processing steps to the data
    spec_with_precursor = [post_process(s) for s in spec_with_precursor if s.metadata.get('inchikey')]
    # omit spectrums that didn't qualify for analysis
    spec_with_precursor = [s for s in spec_with_precursor if s is not None]

    inchi_dict = {}
    for s in spec_with_precursor:
        ik = s.metadata['inchikey']
        init_ik = ik.split('-')[0]
        if not init_ik in inchi_dict:
            inchi_dict[init_ik] = [s]
        else:
            inchi_dict[init_ik].append(s)

    multis = set([i for i, v in inchi_dict.items() if len(v) > min_identical_matches])

    matching_keys = np.random.choice(list(multis), size=query_size, replace=False)

    query_spec = {}
    library_spec = []
    # We select `query_size` queries that have at least `min_identical_matches` matching spectra in the library,
    for q in matching_keys:
        spec_to_add = np.random.choice(inchi_dict[q], size=1, replace=False)
        query_spec[spec_to_add[0].metadata['spectrum_id']] = spec_to_add[0]

    # And everything else goes into the library
    for s in spec_with_precursor:
        if s.metadata['spectrum_id'] not in query_spec:
            library_spec.append(s)

    spectrums_lib = library_spec
    spectrums_query = list(query_spec.values())
    documents_lib = [SpectrumDocument(s, n_decimals=spec2vec_decimal_places) for s in spectrums_lib]
    documents_query = [SpectrumDocument(s, n_decimals=spec2vec_decimal_places) for s in spectrums_query]


def calculate_thresholds(model_file, intensity_weighting_power, allowed_missing_percentage, cos_min_match=6):
    print('using model %s' % model_file)

    # Load pretrained model
    model = gensim.models.Word2Vec.load(model_file)
    vector_size = model.vector_size

    cos_hits = cosine_calc.get_hits(spectrums_query, spectrums_lib, cosine_tol=.005, min_match_count=cos_min_match)
    hits = cosine_calc.get_spec2vec_hits(documents_query, documents_lib, model=model,
                                         intensity_weighting_power=intensity_weighting_power,
                                         allowed_missing_percentage=allowed_missing_percentage)

    cos_hit_dict = {hit.query.metadata['spectrum_id']: hit for hit in cos_hits}
    hit_dict = {hit.query: hit for hit in hits}

    test_matches_cos = []
    test_matches_s2v = []
    thresholds = np.array([x / 20 for x in range(20)] + [.98])
    for threshold in thresholds:
        print(f"Checking matches for similarity score > {threshold:.2f}")
        test_matches = []
        # for every query
        for spec in spectrums_query:
            # find its 'hit'
            if spec.metadata['spectrum_id'] in cos_hit_dict and cos_hit_dict[
                spec.metadata['spectrum_id']].score > threshold:
                test_matches.append(1 * cos_hit_dict[spec.metadata['spectrum_id']].hit)
            else:
                test_matches.append(-1)
        # if True match, 1
        # if False match, 0
        # otherwise ('decoy'), -1
        test_arr = np.array(test_matches)
        test_matches_cos.append([np.sum(test_arr == 1), np.sum(test_arr == 0), np.sum(test_arr == -1)])

        # Then the repeat the same procedure for Spec2Vec matches
        test_matches = []
        for doc in documents_query:
            if doc in hit_dict and hit_dict[doc].score > threshold:
                hit = hit_dict[doc]
                test_matches.append(1 * hit.hit)
            else:
                test_matches.append(-1)
        test_arr = np.array(test_matches)
        test_matches_s2v.append([np.sum(test_arr == 1), np.sum(test_arr == 0), np.sum(test_arr == -1)])

    # Convert lists to np.array
    test_matches_cos_arr = np.array(test_matches_cos)
    test_matches_s2v_arr = np.array(test_matches_s2v)

    # Plot the outcome
    label_picks = [0, 4, 8, 12, 16, 18, 20]
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
                         textcoords="offset points", xytext=(2, -10), fontsize=12, color='red')

    plt.title('true/false positives per threshold')
    plt.legend(fontsize=14)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('false positive rate', fontsize=16)
    plt.ylabel('true positive rate', fontsize=16)
    plt.xlim(0, .35)
    plt.ylim(.1, .8)

    # And save it down so that we can compare multiple plots more easily
    filename = "%s.png" % model_file
    plt.savefig(filename)
    print('saved outcome to', filename)
