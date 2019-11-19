# from py2neo import Graph, Node
#
# graph = Graph("http://localhost:7474/")
# a = Node('Person', name='Alice')
# graph.create(a)
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher

sym = pd.read_csv('data/sym_t.csv')
dia = pd.read_csv('data/dia_t.csv')
rel = pd.read_csv('data/diffsydiw.csv')

sym = sym.dropna()
dia = dia.dropna()
rel = rel.dropna()
# create graph database
graph = Graph("http://localhost:7474/")

# create nodes corresponding to symptoms
for row_idx, row in sym.iterrows():
    node = Node('Symptom', id = row['syd'], name = row['symptom'])
    graph.create(node)

# create nodes corresponding to diagnoses
for row_idx, row in dia.iterrows():
    node = Node('Diagnosis', id = row['did'], name = row['diagnose'])
    graph.create(node)

matcher = NodeMatcher(graph)

sym_set = set(sym['syd'])
dia_set = set(dia['did'])
# create relations between symptoms ans diagnoses
for row_idx, row in rel.iterrows():
    print(row_idx)
    if (row['syd'] in sym_set) and (row['did'] in dia_set):
        sym_node = matcher.match('Symptom', id=row['syd']).first()
        dia_node = matcher.match('Diagnosis', id=row['did']).first()
        relation = Relationship(sym_node, 'INDICATES', dia_node)
        graph.create(relation)
