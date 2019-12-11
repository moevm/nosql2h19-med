from create_db import create_db
from py2neo import Graph, Node, Relationship, NodeMatcher


class bdManager:
    def __init__(self, graddr, loaded):
        print("I'm dbManager!!")

        self.graph = Graph(graddr)
        self.loaded = loaded

    def load_n_create(self):
        if self.loaded:
            self.drop_db()

        constraint = "CREATE CONSTRAINT ON (m:dia_t) ASSERT m.did IS UNIQUE"
        resp = self.graph.run(constraint)
        constraint = "CREATE CONSTRAINT ON (m:sym_t) ASSERT m.syd IS UNIQUE"
        resp = self.graph.run(constraint)
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/dia_t.csv' AS dia_t " \
                " CREATE (:dia_t { Diagnoses: dia_t.diagnose, did: dia_t.did})"
        resp = self.graph.run(query)
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/sym_t.csv' AS sym_t  " \
                " CREATE (:sym_t { Symptom: sym_t.symptom, syd: sym_t.syd})"
        resp = self.graph.run(query)
        query = " LOAD CSV WITH HEADERS FROM 'file:///med/diffsydiw.csv' AS id2id" \
                " MATCH  (d:dia_t {did: id2id.did}), (s:sym_t {syd: id2id.syd}) " \
                " CREATE (s)-[: `INDICATES` {did: id2id.did}]->(d) "
        resp = self.graph.run(query)

        self.loaded = True

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

        self.loaded = False

    def is_ok(self):
        if self.loaded is not True:
            print("BD not loaded!")
            return False
        return True

    def get_BDStat(self):
        query1 = "MATCH (s:sym_t) " \
                 "RETURN s.Symptom AS name, size((s)-[:INDICATES]->()) AS matches " \
                 "LIMIT 10"
        # query2 = ""
        resp1 = self.graph.run(query1)
        # resp2 = self.graph.run(query2)
        # return [resp1.data(), resp2.data()]
        return resp1.data()

    def get_stat_for_plot(self,ids):
        query = "WITH {} as ids " \
                "MATCH (s:sym_t)-[:INDICATES]->(d:dia_t) " \
                "WHERE s.syd in ids " \
                "WITH d,count(*) AS cnt " \
                "ORDER BY cnt DESC " \
                "RETURN d.did As Diagnoses, cnt as freq " \
                "LIMIT 15".format(ids)
        resp = self.graph.run(query)
        return resp.data()

    # def get_sel_diag_stat(self, ids):
    #     return -1

    def get_diag_via_syd(self, syd):
        if not self.is_ok():
            return {}
        query = " MATCH (s:sym_t)-[:INDICATES]->(d) " \
                " WHERE s.syd in {} " \
                " RETURN d.Diagnoses AS Diagnoses," \
                " COLLECT( DISTINCT d.did) AS did ".format(syd)
        # print(query)
        resp = self.graph.run(query)
        return resp.data()

    def get_sym_via_ids(self, ids):
        if not self.is_ok():
            return {}
        query = "MATCH (S:sym_t) " \
                "WHERE S.syd in {} " \
                "RETURN S.Symptom AS Symptom, S.syd AS syd".format(ids)
        resp = self.graph.run(query)
        return resp.data()

    def loadCSV_dia_t(self):
        if not self.is_ok():
            return {}
        query = " MATCH (dia_t:dia_t) " \
                " RETURN dia_t.Diagnoses AS Diagnoses ,dia_t.did AS did"
        resp = self.graph.run(query)
        return resp.data()

    def loadCSV_sym_t(self):
        if not self.is_ok():
            return {}
        query = "MATCH (sym_t:sym_t) " \
                "RETURN sym_t.Symptom AS Symptom, sym_t.syd AS syd"
        resp = self.graph.run(query)
        return resp.data()

    def loadCSV_dyf(self):
        if not self.is_ok():
            return {}
        query = " MATCH l=()-[r:INDICATES]->() " \
                " RETURN nodes(l)[0].syd AS syd, " \
                " nodes(l)[1].did AS did "
        resp = self.graph.run(query)
        return resp.data()
