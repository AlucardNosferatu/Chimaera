from py2neo import Graph

kg = Graph("bolt://localhost:7687")
result = kg.run("MATCH (p:Person) WHERE p.name = 'David'  RETURN p.name AS name")
print(result.keys())
print(result)
