from KG_CLIENT2 import init_kg, find_rel
from SWIP_CLIENT2 import find_all_match, rel_be, append_rule, rel_in, rel_rel


def kg_rel2swip_rel(kgStr):
    return kgStr.lower()


def swip_rel2kg_rel(swipStr):
    return swipStr.upper()


def kg_node2swip_node(kgStr):
    return kgStr.lower()


def swip_node2kg_node(swipStr):
    return swipStr.capitalize()


def kg2swip(results, symbols):
    src_context = []
    for result in results:
        a = result[symbols[0]]['name']
        b = type(result[symbols[1]]).__name__
        c = result[symbols[2]]['name']
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
    rel = 'KNOWS'
    results, symbols = find_rel(kg, rel)
    kg_context = kg2swip(results, symbols)
    rel_swip = kg_rel2swip_rel(rel)
    be_rel_swip = rel_be(rel_swip)
    rel_rel_swip = rel_rel(rel_swip, rel_swip)
    if rel_in(kg_context, be_rel_swip):
        kg_context = append_rule(kg_context, 'rel_be', be_rel_swip)
    elif rel_in(kg_context, rel_swip):
        kg_context = append_rule(kg_context, 'rel_be', rel_swip)
        kg_context = append_rule(kg_context, 'rel_rel', [rel_swip, rel_swip])
    else:
        raise ValueError('Neither rel not be_rel can be found in context')
    find_all_match(kg_context, rel_rel_swip)
