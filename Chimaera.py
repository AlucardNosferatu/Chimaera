from KG_CLIENT2 import init_kg, find_rel, id2node
from SWIP_CLIENT2 import find_all_match, rel_be, append_rule, rel_in, rel_rel


def kg_rel2swip_rel(kgStr):
    return kgStr.lower()


def swip_rel2kg_rel(swipStr):
    return swipStr.upper()


def kg_node2swip_node(kgStr):
    return kgStr.replace(' ', '_').lower()


def swip_node2kg_node(swipStr):
    return swipStr.capitalize().replace('_', ' ')


def kg2swip(results, symbols):
# def kg2swip(results, symbols, node_key=None):
    src_context = []
    for result in results:
        # if type(node_key) is dict:
        #     a_label = list(result[symbols[0]].labels)[0]
        #     a = result[symbols[0]][node_key[a_label]]
        #     c_label = list(result[symbols[2]].labels)[0]
        #     c = result[symbols[2]][node_key[c_label]]
        # elif type(node_key) is str:
        #     a = result[symbols[0]][node_key]
        #     c = result[symbols[2]][node_key]
        # else:
        a = str(result[symbols[0]].identity)
        c = str(result[symbols[2]].identity)
        b = type(result[symbols[1]]).__name__
        src_context.append(
            "{}({}, {}).".format(
                kg_rel2swip_rel(b),
                kg_node2swip_node(a),
                kg_node2swip_node(c)
            )
        )
    return src_context


if __name__ == "__main__":
    kg = init_kg()
    rel = 'ACTED_IN'
    results, symbols = find_rel(kg, rel, 12)
    kg_context = kg2swip(results, symbols)
    # rel2 = 'DIRECTED'
    # results, symbols = find_rel(kg, rel2)
    # kg_context += kg2swip(results, symbols)

    rel_swip = kg_rel2swip_rel(rel)
    be_rel_swip = rel_be(rel_swip)
    rel_rel_swip = rel_rel(rel_swip, rel_swip)
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
        'work_with(X,Y) :- {}(X,Z), {}(Y,Z).'.format(
            'acted_in',
            'acted_in'
        )
    )
    results = find_all_match(kg_context, 'work_with')
    for result in results:
        node1, sym1 = id2node(kg, result[0])
        node2, sym2 = id2node(kg, result[1])
        print(node1[0][sym1[0]]['name'], '<-', node2[0][sym2[0]]['name'])
