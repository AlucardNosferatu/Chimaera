from KG_CLIENT2 import init_kg, merge_rel, delete_rel, create_node
from NLP_CONSOLE import verify_format, std_rel_str, std_node_str
from NN_MODEL import build_model, parse_model, layers_schema


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
        r, s = merge_rel(kg, {'key': 'name', 'val': from_name}, 'TRANSITION', {'key': 'name', 'val': to_name},
                         rel_dict={'name': 'TO_' + to_name})
    else:
        assert type(specify_rel) is str
        r, s = merge_rel(kg, {'key': 'name', 'val': from_name}, 'TRANSITION', {'key': 'name', 'val': to_name},
                         rel_dict={'name': specify_rel})


def fsm_graph_create_event_bidirectional(kg, name1, name2, specify_rel=None):
    if specify_rel is None:
        specify_rel = {}
    if 'to_name2' in specify_rel:
        r1, s1 = merge_rel(kg, {'key': 'name', 'val': name1}, 'TRANSITION', {'key': 'name', 'val': name2},
                           rel_dict={'name': specify_rel['to_name2']})
    else:
        r1, s1 = merge_rel(kg, {'key': 'name', 'val': name1}, 'TRANSITION', {'key': 'name', 'val': name2},
                           rel_dict={'name': 'TO_' + name2})
    if 'to_name1' in specify_rel:
        r2, s2 = merge_rel(kg, {'key': 'name', 'val': name2}, 'TRANSITION', {'key': 'name', 'val': name1},
                           rel_dict={'name': specify_rel['to_name1']})
    else:
        r2, s2 = merge_rel(kg, {'key': 'name', 'val': name2}, 'TRANSITION', {'key': 'name', 'val': name1},
                           rel_dict={'name': 'TO_' + name1})
    return r1 + r2, s1 + s2


def ann_graph_create_layer(kg, layer_node):
    name = layer_node['name']
    print(name)
    type = layer_node['type']
    print(type)
    kg_prop = {'name': name, 'type': type}
    params = layer_node['params']
    schema = layers_schema[type]
    for key in params:
        dtype = schema[key]
        if dtype in ['str', 'int', 'float']:
            kg_prop[key] = params[key]
        elif dtype == 'tuple':
            kg_prop[key] = str(params[key])
        print(dtype)

    r, s = create_node(kg, kg_prop, 'ANN_LAYER')
    return r, s


def ann_graph_link_layers(kg, rel):
    from_name = rel['from']
    to_name = rel['to']
    r, s = merge_rel(kg, {'key': 'name', 'val': from_name}, 'FLOW_TO', {'key': 'name', 'val': to_name})
    return r, s


def ann_graph_link_all_layers(kg, rels):
    results = []
    symbols = []
    for rel in rels:
        print(rel)
        r, s = ann_graph_link_layers(kg, rel)
        results.append(r)
        symbols.append(s)
    return results, symbols


if __name__ == "__main__":
    kg = init_kg()
    model = build_model()
    nodes, rels = parse_model(model=model)
    # for node in nodes:
    #     ann_graph_create_layer(kg, node)
    #     print()
    #     print()
    ann_graph_link_all_layers(kg, rels)
