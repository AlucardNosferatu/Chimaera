from KG_CLIENT2 import init_kg, find_rel, id2node, merge_rel
from SWIP_CLIENT2 import find_all_match, rel_be, append_rule, rel_in, rel_rel
from NLP_CONSOLE import verify_format


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


def merge_via_console(kg, text):
    valid, a, b, c = verify_format(text)
    if valid:
        merge_rel(kg, {'key': 'name', 'val': a}, b.upper(), {'key': 'name', 'val': c})


if __name__ == "__main__":
    kg = init_kg()
    merge_via_console(kg, 'Romeo loves Juliet')
    merge_via_console(kg, 'I loves you')
    rel = 'LOVES'
    results, symbols = find_rel(kg, rel, 100)
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
    # kg_context = append_rule(
    #     kg_context,
    #     'custom',
    #     'work_with(X,Y) :- {}(X,Z), {}(Y,Z).'.format(
    #         'acted_in',
    #         'acted_in'
    #     )
    # )
    # kg_context = append_rule(
    #     kg_context,
    #     'custom',
    #     'work_with_often(X,Y) :- {}(X,A), {}(Y,A), {}(X,B), {}(Y,B), {}(X,C), {}(Y,C), A \\= B, B \\= C, C \\= A, X \\= Y.'.format(
    #         'acted_in',
    #         'acted_in',
    #         'acted_in',
    #         'acted_in',
    #         'acted_in',
    #         'acted_in'
    #     )
    # )
    results = find_all_match(kg_context, 'loves')
    for result in results:
        node1, sym1 = id2node(kg, result[0])
        node2, sym2 = id2node(kg, result[1])
        print(node1[0][sym1[0]]['name'], '<-', node2[0][sym2[0]]['name'])
