import time

from transitions import Machine
import numpy as np
import random


class Matter(object):
    pass


def fake_results():
    ids = []
    rel_ids = []
    for i in range(5):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(10):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(30):
        a = 0
        b = 0
        c = 0
        while [a, b, c] in relationships or a == c:
            a = random.choice(ids)
            b = random.choice(rel_ids)
            c = random.choice(ids)
        relationships.append([a, b, c])
    return relationships, ids, rel_ids


def parse_rel_ids(rels, mode):
    if 'on_dst' in mode:
        rel_ids = []
        for rel in rels:
            a, b, c = rel
            if 'on_rel' in mode:
                # rel和dst都相同的才合并
                temp = [b, c]
            else:
                # 只根据dst相同的合并不同rel
                temp = [c]
            if temp not in rel_ids:
                rel_ids.append(temp)
        return rel_ids
    else:
        # 完全不合并
        return rels


def tutorial():
    model = Matter()

    # The states argument defines the name of states
    states = ['solid', 'liquid', 'gas', 'plasma']

    # The trigger argument defines the name of the new triggering method
    transitions = [
        {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
        {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
        {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
        {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}]

    machine = Machine(model=model, states=states, transitions=transitions, initial='solid')

    # Test
    print(model.state)  # solid
    model.melt()
    print(model.state)  # liquid
    model.evaporate()
    print(model.state)


def get_transitions(rels, ids, mode=None):
    if mode is None:
        mode = ['on_dst']
    states = []
    for id in ids:
        states.append('s{}'.format(ids.index(id)))

    rel_ids = parse_rel_ids(rels, mode)

    transitions = []
    for rel_id in rel_ids:
        for rel in rels:
            start_i = len(rel) - len(rel_id)
            if rel[start_i:] == rel_id:
                transition = {
                    'trigger': 't{}'.format(rel_ids.index(rel_id)),
                    'source': 's{}'.format(ids.index(rel[0])),
                    'dest': 's{}'.format(ids.index(rel[-1]))
                }
                transitions.append(transition)
    return states, transitions, rel_ids


if __name__ == "__main__":
    rels, ids, rel_ids = fake_results()
    ids.sort()
    states, transitions, fsm_rel_ids = get_transitions(rels, ids)
    model = Matter()
    event_index = random.randint(0, len(fsm_rel_ids) - 1)
    machine = Machine(model=model, states=states, transitions=transitions, initial='s{}'.format(event_index))
    while True:
        try:
            event_index = random.randint(0, len(fsm_rel_ids) - 1)
            exec('model.t{}()'.format(event_index))
            print('Triggered:', 's{}'.format(event_index))
            print('Current state:', model.state)
        except Exception as e:
            continue
            print(repr(e))
            print('Attempted to trigger:', 's{}'.format(event_index))
            print('Current state:', model.state)
            # time.sleep(1)
        print('')
    print('Done')
