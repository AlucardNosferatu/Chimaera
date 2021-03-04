import numpy as np
import random


def fake_results():
    ids = []
    for i in range(10):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(30):
        a = 0
        b = 0
        while [a, b] in relationships or a == b:
            a = random.choice(ids)
            b = random.choice(ids)
        relationships.append([a, random.randint(0, 9), b])
    return relationships, ids


def get_matrix(relationships, ids):
    matrix_3d = np.zeros((10, 10, 10))
    matrix_2d = np.zeros((10, 10))
    for rel in relationships:
        a = ids.index(rel[0])
        b = rel[1]
        c = ids.index(rel[2])
        matrix_3d[a, c, b] = 1
        matrix_2d[a, c] = b
    return matrix_3d, matrix_2d


if __name__ == "__main__":
    rels, ids = fake_results()
    m = get_matrix(rels, ids)
