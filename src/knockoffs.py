import copy

import cosine_calc
import numpy as np
import plot_q_vals
from numpy.random import uniform
from q_value_calc import calculate_q_value
from sklearn.mixture import GaussianMixture
from spec2vec.vector_operations import calc_vector


# checking if a given matrrix is positive definite
def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)


def generate_knockoffs(model, document_spectra, intensity_weighting_power=0.5, allowed_missing_percentage=15,
                       n_components=1, sigma_multiplier=1, randomness=True,
                       diagonal_matrix=0.13):
    # embedding given documents
    vector_size = model.vector_size
    print(f"Embedding vector size: {vector_size}")

    embeddings_spec2vec_lib = np.zeros((len(document_spectra), vector_size), dtype="float")
    for i, doc in enumerate(document_spectra):
        embeddings_spec2vec_lib[i, 0:vector_size] = calc_vector(model, doc,
                                                                intensity_weighting_power,
                                                                allowed_missing_percentage)

    # creating the gaussian mixture
    gm = GaussianMixture(n_components=n_components, covariance_type='diag').fit(embeddings_spec2vec_lib)

    n_dim = len(embeddings_spec2vec_lib[0])
    # diagonal matrix

    
    all_knockoffs = []
    # generate N knock-offs
    idxs = list(range(n_components))
    for point in embeddings_spec2vec_lib:
        
        component = np.random.choice( idxs, p=gm.predict_proba( [point] )[0] )
        mu = gm.means_[component]
        cov = gm.covariances_[component]
        
        Sigma = np.eye(n_dim) * cov
        Sigma = Sigma * sigma_multiplier

        D = np.eye(n_dim) * diagonal_matrix

        joint_cov = np.hstack((Sigma, Sigma - D))
        joint_cov = np.vstack((joint_cov, np.hstack((Sigma - D, Sigma))))

        assert is_pos_def(joint_cov), "Joint covariance matrix has to be positive definite"

        A = np.eye(n_dim) - np.dot(D, np.linalg.inv(Sigma))
        kmu = np.dot(np.dot(D, np.linalg.inv(Sigma)), mu)
        B = np.dot(A, point.T)
        kmu += B
        if randomness:
            kSigma = 2 * D - np.dot(np.dot(D, np.linalg.inv(Sigma)), D)
            ko = np.random.multivariate_normal(kmu.flatten(), kSigma, 1)
            all_knockoffs.append(ko)
        else:
            all_knockoffs.append([kmu])

            
    knockoff_documents = []
    for ko, v, d in zip(all_knockoffs, embeddings_spec2vec_lib, document_spectra):
        e = copy.deepcopy(d)
        e._obj.set('inchi', 'knockoff')
        e._obj.set('inchikey_inchi', 'knockoff')
        e._obj.set('vector', ko[0])
        knockoff_documents.append(e)
    return knockoff_documents


def evaluate_knockoff_performance(documents_lib, documents_query, knockoff_documents, model, intensity_weighting_power=0.5,
                                  allowed_missing_percentage=15, save_file=None):
    hits_knockoffs, _ = cosine_calc.get_hits(documents_query, knockoff_documents, decoys=True, spec2vec_model=model,
                                             intensity_weighting_power=intensity_weighting_power,
                                             allowed_missing_percentage=allowed_missing_percentage)
    hits, _ = cosine_calc.get_hits(documents_query, documents_lib, spec2vec_model=model,
                                   intensity_weighting_power=intensity_weighting_power,
                                   allowed_missing_percentage=allowed_missing_percentage)

    q_list_true = calculate_q_value(hits)
    q_list_estimated = calculate_q_value(hits + hits_knockoffs, True)

    def combine_true_est(q_vals_true, q_vals_est):
        res = []
        q_idx = 0
        for q_value_e, _, score in q_vals_est:
            while q_idx < len(q_vals_true) - 1 and q_vals_true[q_idx + 1][2] >= score:
                q_idx += 1
            res.append((score, q_vals_true[q_idx][0], q_value_e))
        return res

    scores, trues, estimateds = zip(*combine_true_est(q_list_true, q_list_estimated))

    plot_q_vals.plot_q_vals({'knockoffs': (trues, estimateds)}, filename=save_file)
    return q_list_true, q_list_estimated
