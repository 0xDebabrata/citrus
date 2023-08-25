def get_cosine_similarity(vec_a: list[float], vec_b: list[float]):
    if len(vec_a) != len(vec_b):
        raise ValueError("Vector dimensions must match for calculating cosine distance")

    score = 0.0
    for i in range(0, len(vec_a)):
        score += vec_a[i] * vec_b[i]

    return score

