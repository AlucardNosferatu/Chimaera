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
    return results, symbols


if __name__ == "__main__":
    kg = init_kg()
    lisp_graph_create_function(kg, 'add', 'ADD2', [2029, 1224])
