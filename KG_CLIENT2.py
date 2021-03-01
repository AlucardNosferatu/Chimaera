from py2neo import Graph


def init_kg():
    kg = Graph("bolt://localhost:7687", username='neo4j', password='neo4j')
    return kg


def find_rel(kg, rel):
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
    results = kg.run(cypher_query).data()
    return results, symbols
