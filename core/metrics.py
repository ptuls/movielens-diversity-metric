# -*- coding: utf-8 -*-
import numpy as np


def cosine_similarity(a, b):
    """
    Compute the cosine similarity between vectors a and b.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def compute_center(model, movies, ratings):
    """
    Compute the center of user movie vectors.
    """
    center = np.zeros((model.vector_size,))
    total_weight = 0
    # iterating this way handles the problem when a movie might not be found in the model
    for i in range(len(movies)):
        movie = movies[i]
        rating = ratings[i]
        try:
            movie_vec = model[movie]
            center += rating * movie_vec
            total_weight += rating
        except KeyError:
            logger.warning(f"{movie} not contained in model")
            continue
    center /= total_weight
    return center


def compute_score(model, movies, ratings, center):
    """
    Once we have computed the center we can then compute the GS-score based on the
    user's center and the cosine similarity between each movie vector and the center.
    We assume ratings are positive.
    """
    score = 0
    total_weight = 0
    for i in range(len(movies)):
        movie = movies[i]
        rating = ratings[i]
        try:
            movie_vec = model[movie]
            score += rating * cosine_similarity(movie_vec, center)
            total_weight += rating
        except KeyError:
            logger.warning(f"{movie} not contained in model")
            continue

    # removing some numerical errors
    return score / max(total_weight, 1.0)


def generalist_specialist_score(model, movies, ratings):
    """
    Based on the generalist-specialist score from Anderson et al.,
    "Algorithmic Effects on the Diversity of Consumption on Spotify".
    """
    center = compute_center(model, movies, ratings)
    score = compute_score(model, movies, ratings, center)
    return score
