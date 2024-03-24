import numpy as np


def norm(vector):
    norm = np.linalg.norm(vector, axis=-1, keepdims=True)
    return vector / norm


def dot_product(a, b):
    return b @ a.T


def cosine_similarity(a, b):
    a_norm = norm(a)
    b_norm = norm(b)
    return b_norm @ a_norm.T


def euclidean(a, b, use_similarity=True):
    distances = np.linalg.norm(a - b, axis=1)
    similarities = 1 / (1 + distances)
    return similarities if use_similarity else distances


OPSET_LOOKUP = {
    "dot": dot_product,
    "cosine": cosine_similarity,
    "euclidean": euclidean,
}
