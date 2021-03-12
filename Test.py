import hy
import greetings
from transitions import Machine
from NN_MATRIX import get_matrix
from Chimaera import kg2swip
from GRAPH2GLIST import get_symbol_str
from HY_EXECUTOR import reg_func_tree, force_reload, reg_func, exe_func, ft
from SWIP_CLIENT2 import append_rule, find_all_match
from KG_CLIENT2 import init_kg, find_rel, id2node
from KG_FSM2 import Matter


def test_1():
    kg = init_kg()
    # console_cmd(kg, 'Romeo loves Juliet')
    # console_cmd(kg, 'you love me')
    # console_cmd(kg, "you aren't loving me")
    # console_cmd(kg, 'you love me')
    rel = 'ACTED_IN'
    results, symbols = find_rel(kg, rel, 100)
    kg_context = kg2swip(results, symbols)
    # rel2 = 'DIRECTED'
    # results, symbols = find_rel(kg, rel2)
    # kg_context += kg2swip(results, symbols)

    # rel_swip = kg_rel2swip_rel(rel)
    # be_rel_swip = rel_be(rel_swip)
    # rel_rel_swip = rel_rel(rel_swip, rel_swip)
    # if rel_in(kg_context, be_rel_swip):
    #     kg_context = append_rule(kg_context, 'rel_be', be_rel_swip)
    # elif rel_in(kg_context, rel_swip):
    #     kg_context = append_rule(kg_context, 'rel_be', rel_swip)
    #     kg_context = append_rule(kg_context, 'rel_rel', [rel_swip, rel_swip])
    # else:
    #     raise ValueError('Neither rel not be_rel can be found in context')
    kg_context = append_rule(
        kg_context,
        'custom',
        'work_with_often(X,Y) :- {}(X,A), {}(Y,A), {}(X,B), {}(Y,B), {}(X,C), {}(Y,C), A\\=B, B\\=C, C\\=A, X\\=Y.'.format(
            'acted_in',
            'acted_in',
            'acted_in',
            'acted_in',
            'acted_in',
            'acted_in'
        )
    )
    kg_context = append_rule(
        kg_context,
        'custom',
        'work_with_twice(X,Y) :- {}(X,A), {}(Y,A), {}(X,B), {}(Y,B), A\\=B, X\\=Y, \\+{}(X,Y), \\+{}(Y,X).'.format(
            'acted_in',
            'acted_in',
            'acted_in',
            'acted_in',
            'work_with_often',
            'work_with_often'
        )
    )
    kg_context = append_rule(
        kg_context,
        'custom',
        'work_with_once(X,Y) :- {}(X,A), {}(Y,A), X\\=Y, \\+{}(X,Y), \\+{}(Y,X), \\+{}(X,Y), \\+{}(Y,X).'.format(
            'acted_in',
            'acted_in',
            'work_with_often',
            'work_with_often',
            'work_with_twice',
            'work_with_twice'
        )
    )
    results1, ids1 = find_all_match(kg_context, 'work_with_often', rel_id=1)
    results2, ids2 = find_all_match(kg_context, 'work_with_twice', rel_id=2)
    results3, ids3 = find_all_match(kg_context, 'work_with_once', rel_id=3)
    results = results1 + results2 + results3
    ids = ids1 + ids2 + ids3
    m3, m2 = get_matrix(results, list(set(ids)), [1, 2, 3])
    for result in results:
        node1, sym1 = id2node(kg, result[0])
        rel_id = result[1]
        node2, sym2 = id2node(kg, result[2])
        print(node1[0][sym1[0]]['name'], '-[{}]->'.format(rel_id), node2[0][sym2[0]]['name'])


def test_2():
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


def test_3():
    greetings.greet("Foo")  # prints "Hello from Hy, Foo"
    print(greetings.this_will_have_underscores)  # prints "See?"


def test_4():
    expr = hy.read_str("(- (/ (+ 1 3 88) 2) 8)")
    hy.eval(expr)


def test_5():
    reg_func()
    res = exe_func()
    print(res)
    lines = None
    with open('Malformation/FUNC_STORAGE.py', 'r') as f:
        lines = f.readlines()
    lines.append("\n")
    lines.append("\n")
    sub1_py_str = """
def sub1(a, b):
    return a - b
"""
    lines.append(sub1_py_str)
    with open('Malformation/FUNC_STORAGE.py', 'w') as f:
        f.writelines(lines)
    reg_func('sub1')
    res = exe_func('sub1')
    print(res)


def test_6():
    results = [
        {'symbol': 'add1', 'param': 2029, 'pcount': 2},
        {'symbol': 'add1', 'param': 10, 'pcount': 2},
        {'symbol': 'sub1', 'param': 'add1', 'pcount': 2},
        {'symbol': 'sub1', 'param': 2021, 'pcount': 2},
    ]
    str2 = get_symbol_str('sub1', results)

    exe_name = reg_func_tree(str2)
    force_reload()
    res = eval('ft.{}()'.format(exe_name))
    print(res)


if __name__ == "__main__":
    test_6()
