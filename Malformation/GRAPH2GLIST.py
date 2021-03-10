import numpy as np
import random


def fake_results():
    ids = []
    rel_ids = []
    for i in range(1):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(3):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(5):
        a = 0
        b = 0
        c = 0
        while [a, b, c] in relationships or a == c:
            a = random.choice(ids)
            b = random.choice(rel_ids)
            c = random.choice(ids)
        relationships.append([a, b, c])
    return relationships, ids, rel_ids


if __name__ == "__main__":
    rels, ids, rel_ids = fake_results()
    for rel in rels:
        print(rel[1], rel[0], rel[2])
    print('Done')
