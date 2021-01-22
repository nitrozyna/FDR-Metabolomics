from spec2vec import Spec2Vec
from spec2vec.model_building import train_new_word2vec_model
import numpy as np
from sklearn.mixture import GaussianMixture
import copy
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy.ma as ma
from numpy.random import uniform, seed
from matplotlib import cm
from scipy.stats import multivariate_normal
from spec2vec.SpectrumDocument import SpectrumDocument
from matchms import Spectrum
import importlib
import cosine_calc
from q_value_calc import calculate_q_value
import plot_q_vals

from matchms.importing import load_from_json
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

library_spec = set()
query_spec = set()
singletons = set([i for i,v in inchi_dict.items() if len(v) == 1])
multis = set([i for i,v in inchi_dict.items() if len(v) > 1])
print(len(singletons), len(multis))

query_size = 1500
library_size = 2500
import numpy as np

used = set()
query_keys = np.random.choice(list(multis), size=query_size, replace=False)
other_library_keys = np.random.choice(list(singletons), size=library_size-query_size, replace=False)

query_spec = []
library_spec = []
for q in query_keys:
    ss = np.random.choice(inchi_dict[q], size=2, replace=False)
    query_spec.append(ss[0])
    library_spec.append(ss[1])
for o in other_library_keys:
    ss = np.random.choice(inchi_dict[o], size=1, replace=False)
    library_spec.append(ss[0])

import os
folder_name = 'C:\\Users\\Gosia\\Desktop'

assert len(library_spec) == library_size
assert len(query_spec) == query_size

spectrums_lib = library_spec
spectrums_query = query_spec

documents_query = [SpectrumDocument(s, n_decimals=2) for s in spectrums_query]
documents_lib = [SpectrumDocument(s, n_decimals=2) for s in spectrums_lib]


path_models = os.path.join(folder_name, "trained_models")


def f(size, intensity_weighting_power = 0.5, allowed_missing_percentage = 15, factorD=0.13):

    model_file = os.path.join(path_models, "spec2vec_librarymatching_size_%d.model" % size)

    iterations = [1, 3, 5, 10]

    #Train model with size 10 and default parameters
    from spec2vec.vector_operations import calc_vector
    model = train_new_word2vec_model(documents_lib, iterations, model_file, size = size)

    vector_size = model.vector_size
    print(f"Embedding vector size: {vector_size}")

    embeddings_spec2vec_lib = np.zeros((len(documents_lib), vector_size), dtype="float")
    for i, doc in enumerate(documents_lib):
        embeddings_spec2vec_lib[i, 0:vector_size] = calc_vector(model, doc,
                                                            intensity_weighting_power,
                                                            allowed_missing_percentage)

    gm = GaussianMixture().fit(embeddings_spec2vec_lib)

    def is_pos_def(x):
        return np.all(np.linalg.eigvals(x) > 0)

    # seed(1234)
    nDim = len(embeddings_spec2vec_lib[0])
    # define the mean and covariance
    mu = gm.means_[0]
    Sigma = gm.covariances_[0]
    D = np.eye(nDim)*factorD

    joint_cov = np.hstack((Sigma, Sigma-D))
    joint_cov = np.vstack((joint_cov, np.hstack((Sigma-D,Sigma))))

    assert(is_pos_def(joint_cov))

    A = np.eye(nDim) - np.dot(D,np.linalg.inv(Sigma))

    all_knockoffs = []
    # generate a sample
    for point in embeddings_spec2vec_lib:
        # generate N knock-offs
        kmu = np.dot(np.dot(D,np.linalg.inv(Sigma)),mu)
        B = np.dot(A, point.T)
        kmu += B
        kSigma = 2*D - np.dot(np.dot(D,np.linalg.inv(Sigma)), D)
        ko = np.random.multivariate_normal(kmu.flatten(), kSigma, 1)
        all_knockoffs.append(ko)


    knockoff_documents = []
    for ko,v,d in zip(all_knockoffs,embeddings_spec2vec_lib,documents_lib):
        #print("knockoff:",ko,"vector",v,"document",d)
        #print("\n")
        e = copy.deepcopy(d)
        e._obj.set('inchi', 'knockoff')
        e._obj.set('vector', ko[0])
        knockoff_documents.append(e)
    #print(knockoff_documents)


    hits_knockoffs, _ = cosine_calc.get_hits(documents_query, knockoff_documents, decoys=True, spec2vec_model=model,
                                                            intensity_weighting_power=intensity_weighting_power,
                                                            allowed_missing_percentage=allowed_missing_percentage)
    hits, _ = cosine_calc.get_hits(documents_query, documents_lib, spec2vec_model=model,
                                                            intensity_weighting_power=intensity_weighting_power,
                                                            allowed_missing_percentage=allowed_missing_percentage)

    # Calculating true q-value scores
    q_list_true = calculate_q_value(hits)

    # Calculating estimated q-value scores
    q_list_estimated = calculate_q_value(hits+hits_knockoffs,True)


    # plot estimated and true q-values
    def combine_true_est(q_val_true, q_val_est):
        res = []
        q_idx = 0
        for q_e, _, score in q_val_est:
            while q_idx < len(q_val_true) - 1 and q_val_true[q_idx + 1][2] >= score:
                q_idx += 1
            res.append((score, q_val_true[q_idx][0], q_e))
        return res


    scores, trues, estimateds = zip(*combine_true_est(q_list_true, q_list_estimated))

    folder_path = r"C:\Users\Gosia\Desktop\FDR-Metabolomics\meetings\Figures\spec2vec_dimensions_exp_lcms"
    filename1 = "q_%d_%.2f_%d_%.2f.png" % (size, intensity_weighting_power, allowed_missing_percentage, factorD)
    plot_q_vals.plot_q_vals({'knockoffs': (trues, estimateds)}, os.path.join(folder_path,filename1))

    documents_query_s2v = documents_query

    test_matches_s2v = []

    cosine_thresholds = np.arange(0, 1, 0.05)

    # for every query
    # find its 'hit'
    # if True match, 1
    # if False match, 0
    # otherwise, -1

    hit_dict = {hit.query: hit for hit in hits}

    for threshold in cosine_thresholds:
        print(f"Checking matches for spec2vec score > {threshold:.2f}")
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
    test_matches_s2v_arr = np.array(test_matches_s2v)

    thresholds = np.arange(0, 1, 0.05)
    label_picks = [0, 4, 8, 12, 14, 15, 16, 17, 18, 19]

    plt.figure(figsize=(7, 6))
    plt.style.use('ggplot')
    num_max = np.sum(test_matches_s2v_arr[0, :])

    plt.plot(test_matches_s2v_arr[:, 1] / num_max, test_matches_s2v_arr[:, 0] / num_max,
             'o-', label='Spec2Vec')
    for i, threshold in enumerate(thresholds):
        if i in label_picks:
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

    filename2 = "tfr_%d_%.2f_%d_%.2f.png" % (size, intensity_weighting_power, allowed_missing_percentage, factorD)
    plt.savefig(os.path.join(folder_path,filename2))
