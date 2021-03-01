from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine
from py2neo import Graph

rel = 'KNOWS'
kg = Graph("bolt://localhost:7687", username='neo4j', password='neo4j')
cypher_query = "MATCH (a:Person)-[b:{}]->(c:Person) RETURN a, b, c".format(rel)
results = kg.run(cypher_query).data()

src_context = ''
for result in results:
    a = result['a']['name'].lower()
    b = type(result['b']).__name__.lower()
    c = result['c']['name'].lower()
    src_context += "{}({}, {}).".format(b, a, c)
    src_context += '\n'
