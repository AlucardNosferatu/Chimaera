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
