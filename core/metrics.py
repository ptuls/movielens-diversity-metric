# -*- coding: utf-8 -*-
from collections import Counter
from math import log
import numpy as np


def cosine_similarity(a, b):
    """
    Compute the cosine similarity between vectors a and b.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def compute_center(model, movies_ratings, verbose):
    """
    Compute the center of user movie vectors.
    """
    center = np.zeros((model.vector_size,))
    total_weight = 0
    # iterating this way handles the problem when a movie might not be found in the model
    i = 0
    for movie in movies_ratings:
        try:
            movie_vec = model[movie]
            rating = movies_ratings[movie]
            center += rating * movie_vec
            total_weight += rating
        except KeyError:
            if verbose:
                logger.warning(f"{movie} not contained in model")
            continue
    center /= total_weight
    return center


def compute_score(model, movies_ratings, center, verbose):
    """
    Once we have computed the center we can then compute the GS-score based on the
    user's center and the cosine similarity between each movie vector and the center.
    We assume ratings are positive.
    """
    score, total_weight = 0, 0
    i = 0
    for movie in movies_ratings:
        try:
            movie_vec = model[movie]
            rating = movies_ratings[movie]
            score += rating * cosine_similarity(movie_vec, center)
            total_weight += rating
        except KeyError:
            if verbose:
                logger.warning(f"{movie} not contained in model")
            continue

    # removing some numerical errors
    return score / max(total_weight, 1.0)


def generalist_specialist_score(model, movies_ratings, verbose=False):
    """
    Based on the generalist-specialist score from Anderson et al.,
    "Algorithmic Effects on the Diversity of Consumption on Spotify".
    """
    center = compute_center(model, movies_ratings, verbose)
    score = compute_score(model, movies_ratings, center, verbose)
    return score
    

def compute_shannon_entropy(movie_list):
    """
    Compute Shannon Entropy of a user's movie diversity.
    """
    total_movies = len(movie_list)
    view_count = Counter(movie_list)
    H = 0
    for value in view_count.values():
        p = value / total_movies
        H += -p * log(p, 2)
    return H
