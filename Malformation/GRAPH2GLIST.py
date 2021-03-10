import numpy as np
import random


class Glist:
    def __init__(self):
        self.head = None
        self.tail = None

    pass


def fake_results():
    ids = []
    rel_ids = []
    for i in range(4):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(4):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(10):
        a = 0
        b = 0
        c = 0
        while [a, b, c] in relationships or a == c:
            a = random.choice(ids)
            b = random.choice(rel_ids)
            c = random.choice(ids)
        relationships.append([a, b, c])
    return relationships, ids, rel_ids


def rels2glist(rels):
    parsed = [False] * len(rels)
    ids = []
    for rel in rels:
        if rel[0] not in ids:
            ids.append(rel[0])
        if rel[2] not in ids:
            ids.append(rel[2])
    glist = []
    for i in range(len(ids)):
        SGL = Glist()
        SGL.tail = []
        SGL.rel = None
        SGL.head = ids[i]
        recursive_linking(parsed, [SGL], rels)
        glist.append(SGL)
    return glist


def recursive_linking(parsed, SGL_list, rels, prev_gl=None):
    if prev_gl is None:
        prev_gl = []
    ngl_list = []
    if SGL not in prev_gl:
        prev_gl.append(SGL)
    for i in range(len(rels)):
        if not parsed[i]:
            a, b, c = rels[i]
            if a == SGL.head:
                NGL = Glist()
                NGL.head = c
                NGL.rel = b
                NGL.tail = []
                SGL.tail.append(NGL)
                ngl_list.append(NGL)
                prev_gl.append(NGL)
                parsed[i] = True
    recursive_linking(parsed, ngl_list, rels, prev_gl=prev_gl)


if __name__ == "__main__":
    # rels, ids, rel_ids = fake_results()
    # rels = [[110, 4, 78], [163, 6, 9], [9, 7, 110], [78, 7, 163], [110, 7, 9], [78, 8, 9], [9, 6, 163], [110, 7, 78],
    #         [78, 4, 110], [9, 7, 163]]
    rels = [
        [1, 1, 2],
        [1, 1, 3],
        [2, 1, 4],
        [3, 1, 4]
    ]
    SGL = rels2glist(rels)
    print('Done')
