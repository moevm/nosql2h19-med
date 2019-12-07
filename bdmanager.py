from create_db import create_db
from py2neo import Graph, Node, Relationship, NodeMatcher


class bdManager:
    def __init__(self, graddr):
        print("I'm dbManager!!")

        self.graph = Graph(graddr)

        # self.resp = self.graph.run("MATCH (s:Symptom) RETURN s.id AS name, size((s)-[:INDICATES]->()) LIMIT 10")
        # self.loadCSV()

        # print(self.resp.to_table())
        #
        # self.diagnosis = "MATCH (d:Diagnosis) RETURN d.name,d.id"
        #
        # self.symptoms = "MATCH (d:Diagnosis) RETURN d.name,d.id"

    def loadCSV(self):
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/dia_t.csv' AS dia_t " \
                " RETURN dia_t.diagnose AS Diagnoses ,dia_t.did AS did "
        resp = self.graph.run(query)
        return resp.data()
