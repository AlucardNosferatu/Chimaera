from KG_CLIENT2 import init_kg, merge_rel, delete_rel, create_node
from NLP_CONSOLE import verify_format, std_rel_str, std_node_str


def kg_rel2swip_rel(kgStr):
    return kgStr.lower()


def swip_rel2kg_rel(swipStr):
    return swipStr.upper()


def kg2swip(results, symbols):
    src_context = []
    for result in results:
        a = str(result[symbols[0]].identity)
        c = str(result[symbols[2]].identity)
        b = type(result[symbols[1]]).__name__
        src_context.append(
            "{}({}, {}).".format(
                kg_rel2swip_rel(b),
                a,
                c
            )
        )
    return src_context


def console_cmd(kg, text):
    valid, a, b, c = verify_format(text)
    if valid is not None:
        if valid == 'MERGE':
            a = std_node_str(a)
            c = std_node_str(c)
            merge_rel(kg, {'key': 'name', 'val': a}, std_rel_str(b).upper(), {'key': 'name', 'val': c})
        elif valid == 'DELETE':
            a = std_node_str(a)
            c = std_node_str(c)
            delete_rel(kg, {'key': 'name', 'val': a}, std_rel_str(b).upper(), {'key': 'name', 'val': c})


def lisp_graph_create_function(kg, func, name, params):
    results = []
    symbols = []
    r, s = create_node(kg, {'name': name, 'func': func}, 'LISP_FUNC')
    results.append(r)
    symbols.append(s)
    for param in params:
        if type(param) is int:
            r, s = create_node(kg, {'val': param}, 'LISP_VAL')
            results.append(r)
            symbols.append(s)
            r, s = merge_rel(kg, {'key': 'val', 'val': param}, 'PARAM_OF', {'key': 'name', 'val': name})
            results.append(r)
            symbols.append(s)
        elif type(param) is list:
            sub_func = param[0]
            sub_name = param[1]
            sub_params = param[2]
            rs, ss = lisp_graph_create_function(kg, sub_func, sub_name, sub_params)
            results += rs
            symbols += ss
            r, s = merge_rel(kg, {'key': 'name', 'val': sub_name}, 'PARAM_OF', {'key': 'name', 'val': name})
            results.append(r)
            symbols.append(s)
    return results, symbols


def fsm_graph_create_state(kg, name, funcs):
    results = []
    symbols = []
    r, s = create_node(kg, {'name': name}, 'FSM_STATE')
    results.append(r)
    symbols.append(s)
    for func in funcs:
        sub_func = func[0]
        sub_name = func[1]
        sub_params = func[2]
        rs, ss = lisp_graph_create_function(kg, sub_func, sub_name, sub_params)
        results += rs
        symbols += ss
        r, s = merge_rel(kg, {'key': 'name', 'val': sub_name}, 'FUNC_OF', {'key': 'name', 'val': name})
        results.append(r)
        symbols.append(s)


def fsm_graph_create_event(kg, from_name, to_name, specify_rel=None):
    if specify_rel is None:
        r, s = merge_rel(kg, {'key': 'name', 'val': from_name}, 'TO_' + to_name, {'key': 'name', 'val': to_name})
    else:
        assert type(specify_rel) is str
        r, s = merge_rel(kg, {'key': 'name', 'val': from_name}, specify_rel, {'key': 'name', 'val': to_name})


if __name__ == "__main__":
    kg = init_kg()
    # lisp_graph_create_function(kg, 'add', 'ADD2', [2029, 1224])
    # funcs = [
    #     ['sub', 'SUB1', [2029, 1224]],
    #     ['sub', 'SUB2', [2029, ['sub', 'SUB1', [2029, 1224]]]]
    # ]
    fsm_graph_create_state(kg, 'STATE_2', [])
    fsm_graph_create_state(kg, 'STATE_3', [])
    fsm_graph_create_event(kg, 'STATE_0', 'STATE_1')
    fsm_graph_create_event(kg, 'STATE_0', 'STATE_1', 'STATE_0_TO_STATE_1')
    fsm_graph_create_event(kg, 'STATE_2', 'STATE_1')
    fsm_graph_create_event(kg, 'STATE_3', 'STATE_1', 'STATE_3_TO_STATE_1')
    print('Done')
