import copy

import numpy as np
from numpy.random import uniform
from sklearn.mixture import GaussianMixture
from spec2vec.vector_operations import calc_vector


# checking if a given matrix is positive definite
def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)


def generate_knockoffs(model, document_spectra, diagonal_matrix, n_components, intensity_weighting_power=0.5,
                       allowed_missing_percentage=15, embeddings=None):
    vector_size = model.vector_size
    print(f"Embedding vector size: {vector_size}")

    if embeddings is None:
        embeddings = np.zeros((len(document_spectra), vector_size), dtype="float")
        for i, doc in enumerate(document_spectra):
            embeddings[i, 0:vector_size] = calc_vector(model, doc,
                                                       intensity_weighting_power,
                                                       allowed_missing_percentage)

    gm = GaussianMixture(n_components=n_components, covariance_type='diag').fit(embeddings)

    n_dim = len(embeddings[0])

    all_knockoffs = []
    idxs = list(range(n_components))
    for point in embeddings:
        component = np.random.choice(idxs, p=gm.predict_proba([point])[0])
        mu = gm.means_[component]
        cov = gm.covariances_[component]

        Sigma = np.eye(n_dim) * cov
        D = np.eye(n_dim) * diagonal_matrix

        joint_cov = np.hstack((Sigma, Sigma - D))
        joint_cov = np.vstack((joint_cov, np.hstack((Sigma - D, Sigma))))

        assert is_pos_def(joint_cov), "Joint covariance matrix has to be positive definite"

        A = np.eye(n_dim) - np.dot(D, np.linalg.inv(Sigma))
        kmu = np.dot(np.dot(D, np.linalg.inv(Sigma)), mu)
        B = np.dot(A, point.T)
        kmu += B
        kSigma = 2 * D - np.dot(np.dot(D, np.linalg.inv(Sigma)), D)
        ko = np.random.multivariate_normal(kmu.flatten(), kSigma, 1)
        all_knockoffs.append(ko)

    knockoff_documents = []
    for ko, v, d in zip(all_knockoffs, embeddings, document_spectra):
        knockoff_doc = copy.deepcopy(d)
        knockoff_doc._obj.set('inchi', 'knockoff')
        knockoff_doc._obj.set('inchikey_inchi', 'knockoff')
        knockoff_doc._obj.set('vector', ko[0])
        knockoff_documents.append(knockoff_doc)
    return knockoff_documents
