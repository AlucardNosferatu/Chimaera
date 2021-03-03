from py2neo import Graph


def init_kg():
    kg = Graph("bolt://localhost:7687", username='neo4j', password='neo4j')
    return kg


def find_rel(kg, rel, limit=None):
    symbols = ['a', 'b', 'c']
    cypher_query = "MATCH ({})-[{}:{}]->({}) RETURN {}, {}, {}".format(
        symbols[0],
        symbols[1],
        rel,
        symbols[2],
        symbols[0],
        symbols[1],
        symbols[2]
    )
    if limit is not None:
        cypher_query += ' LIMIT {}'.format(str(limit))
    results = kg.run(cypher_query).data()
    return results, symbols


def merge_rel(kg, src, rel, dst):
    symbols = ['a', 'b', 'c']
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (symbols[0], src['key'], src['val'], symbols[0]))
    _ = kg.run(init_node).data()
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (symbols[2], dst['key'], dst['val'], symbols[2]))
    _ = kg.run(init_node).data()
    cypher_query = "MATCH ({0}),({2}) WHERE {0}.{3}='{4}' AND {2}.{5}='{6}' MERGE ({0})-[{1}:{7}]->({2}) RETURN {0},{1},{2}".format(
        symbols[0],
        symbols[1],
        symbols[2],
        src['key'],
        src['val'],
        dst['key'],
        dst['val'],
        rel
    )
    results = kg.run(cypher_query).data()
    return results, symbols


def delete_rel(kg, src, rel, dst):
    symbols = ['a', 'b', 'c']
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (symbols[0], src['key'], src['val'], symbols[0]))
    _ = kg.run(init_node).data()
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (symbols[2], dst['key'], dst['val'], symbols[2]))
    _ = kg.run(init_node).data()
    cypher_query = "MATCH ({0})-[{1}]->({2}) WHERE {0}.{3}='{4}' AND {2}.{5}='{6}' AND TYPE({1})='{7}' DELETE {1} RETURN {0},{2}".format(
        symbols[0],
        symbols[1],
        symbols[2],
        src['key'],
        src['val'],
        dst['key'],
        dst['val'],
        rel
    )
    results = kg.run(cypher_query).data()
    return results, symbols


def id2node(kg, id):
    symbols = ['a']
    cypher_query = "MATCH ({}) WHERE id({})={} RETURN {}".format(
        symbols[0],
        symbols[0],
        str(id),
        symbols[0]
    )
    results = kg.run(cypher_query).data()
    return results, symbols
