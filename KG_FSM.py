from state_machine import *
import numpy as np
import random


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


@acts_as_state_machine
class Person:
    name = 'Billy'

    sleeping = State(initial=True)
    running = State()
    cleaning = State()

    run = Event(from_states=sleeping, to_state=running)
    cleanup = Event(from_states=running, to_state=cleaning)
    sleep = Event(from_states=(running, cleaning), to_state=sleeping)

    @before('sleep')
    def do_one_thing(self):
        print("{} is sleepy".format(self.name))

    @before('sleep')
    def do_another_thing(self):
        print("{} is REALLY sleepy".format(self.name))

    @after('sleep')
    def snore(self):
        print("Zzzzzzzzzzzz")

    @after('sleep')
    def big_snore(self):
        print("Zzzzzzzzzzzzzzzzzzzzzz")


def test_billy():
    person = Person()
    print(person.current_state == Person.sleeping)  # True
    print(person.is_sleeping)  # True
    print(person.is_running)  # False
    person.run()
    print(person.is_running)  # True
    person.sleep()

    # Billy is sleepy
    # Billy is REALLY sleepy
    # Zzzzzzzzzzzz
    # Zzzzzzzzzzzzzzzzzzzzzz

    print(person.is_sleeping)  # True


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


class GBody:
    states = []
    events = []
    initial_state = State(initial=True)
    name = ''

    def __init__(self, name, rels, ids, mode=None):
        if mode is None:
            mode = ['on_dst']
        self.name = name
        for id in ids:
            state = State()
            self.states.append(state)
        rel_ids = parse_rel_ids(rels, mode)
        for rel_id in rel_ids:
            t_state = self.states[ids.index(rel_id[-1])]
            f_states = [self.initial_state]
            for rel in rels:
                start_i = len(rel) - len(rel_id)
                if rel[start_i:] == rel_id:
                    f_states.append(self.states[ids.index(rel[0])])
            event = Event(from_states=tuple(f_states), to_state=t_state)
            self.events.append(event)


if __name__ == "__main__":
    # test_billy()
    rels, ids, rel_ids = fake_results()

    GWilliam = GBody('William', rels, ids)

    @acts_as_state_machine
    class GBInterface:
        name = GWilliam.name
        sleeping = GWilliam.initial_state
        running = GWilliam.states[0]
        cleaning = GWilliam.states[1]
        run = GWilliam.events[0]
        cleanup = GWilliam.events[1]
        sleep = GWilliam.events[2]

        @before('sleep')
        def do_one_thing(self):
            print("{} is sleepy".format(self.name))

        @before('sleep')
        def do_another_thing(self):
            print("{} is REALLY sleepy".format(self.name))

        @after('sleep')
        def snore(self):
            print("Zzzzzzzzzzzz")

        @after('sleep')
        def big_snore(self):
            print("Zzzzzzzzzzzzzzzzzzzzzz")


    GMonster = GBInterface()
    person = Person()
    GMonster.sleep()
    print('Done')
