from create_db import create_db
from py2neo import Graph, Node, Relationship, NodeMatcher


class bdManager:
    def __init__(self, graddr,loaded):
        print("I'm dbManager!!")

        self.graph = Graph(graddr)
        self.loaded = False


    def load_n_create(self):
        constraint = "CREATE CONSTRAINT ON (m:dia_t) ASSERT m.did IS UNIQUE"
        resp = self.graph.run(constraint)
        print(resp.data())
        constraint = "CREATE CONSTRAINT ON (m:sym_t) ASSERT m.syd IS UNIQUE"
        resp = self.graph.run(constraint)
        print(resp.data())
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/dia_t.csv' AS dia_t " \
                " CREATE (:dia_t { Diagnoses: dia_t.diagnose, did: dia_t.did})"
        resp = self.graph.run(query)
        print(resp.data())
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/sym_t.csv' AS sym_t  " \
                " CREATE (:sym_t { Symptom: sym_t.symptom, syd: sym_t.syd})"
        resp = self.graph.run(query)
        print(resp.data())
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/diffsydiw.csv' AS id2id" \
                " MATCH  (d:dia_t {did: id2id.did}), (s:sym_t {syd: id2id.syd}) " \
                " CREATE (s)-[: `INDICATES`]->(d) "
        resp = self.graph.run(query)
        print(resp.data())

    def drop_db(self):
        print("Drop it!")
        query = "MATCH (n) " \
                "OPTIONAL MATCH (n)-[r]-() " \
                "DELETE n,r"
        resp = self.graph.run(query)
        query = "DROP CONSTRAINT ON (m:sym_t) ASSERT m.syd IS UNIQUE"
        resp = self.graph.run(query)
        query = "DROP CONSTRAINT ON (m:dia_t) ASSERT m.did IS UNIQUE"
        resp = self.graph.run(query)

    def loadCSV_dia_t(self):
        if not self.loaded:
            return 1
        query = " MATCH (dia_t:dia_t) " \
                " RETURN dia_t.diagnose AS Diagnoses ,dia_t.did AS did "
        resp = self.graph.run(query)
        return resp.data()

    def loadCSV_sym_t(self):
        if not self.loaded:
            return 1
        query = " MATCH (dia_t:sym_t)  " \
                " RETURN sym_t.symptom AS Symptom, sym_t.syd AS syd"
        resp = self.graph.run(query)
        return resp.data()

    def loadCSV_dyf(self):
        if not self.loaded:
            return 1
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/diffsydiw.csv' AS id2id " \
                " RETURN id2id.wei as Weight,id2id.did as did ,id2id.syd as syd"
        resp = self.graph.run(query)
        return resp.data()
