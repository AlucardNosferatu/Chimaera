import numpy as np
import random


class Glist:
    def __init__(self):
        self.tail = None

    pass


def fake_results():
    ids = []
    rel_ids = []
    for i in range(5):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(5):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(20):
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
    glist = []
    head_list = []
    tail_list = []
    for rel in rels:
        a, b, c = rel
        TGL = Glist()
        TGL.rel = b
        TGL.head = a
        TGL.tail = [c]
        start = 0
        for i in range(tail_list.count([a])):
            pos = tail_list.index([a], start)
            glist[pos].tail += [TGL]
            start = pos + 1
        glist.append(TGL)
        head_list.append(a)
        tail_list.append([c])
    return glist, head_list, tail_list


def is_tail(gla, glb):
    if type(glb.tail) is int:
        return False
    else:
        if gla.head == glb.tail.head and gla.tail == glb.tail.tail and gla.rel == glb.tail.rel:
            return True
        else:
            return is_tail(gla, glb.tail)


if __name__ == "__main__":
    rels, ids, rel_ids = fake_results()
    glist, head_list, tail_list = rels2glist(rels)
    blacklist = []
    for i in range(len(glist)):
        gla = glist[i]
        for j in range(i + 1, len(glist)):
            glb = glist[j]
            if is_tail(gla, glb):
                blacklist.append(i)
                break
    blacklist.sort(reverse=True)
    for pos in blacklist:
        del glist[pos]
        del head_list[pos]
        del tail_list[pos]
    print('Done')
