from create_db import create_db
from py2neo import Graph, Node, Relationship, NodeMatcher

class bdManager:
    def __init__(self,graddr):
        print("I'm dbManager!!")

        self.graph = Graph(graddr)

        self.resp = self.graph.run("MATCH (s:Symptom) RETURN s.id AS name, size((s)-[:INDICATES]->()) LIMIT 10")

        print(self.resp.to_table())

        self.diagnosis = "MATCH (d:Diagnosis) RETURN d.name,d.id"

        self.symptoms = "MATCH (d:Diagnosis) RETURN d.name,d.id"





