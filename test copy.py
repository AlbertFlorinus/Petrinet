import networkx as nx
import random

global B
B = nx.DiGraph()

class Worker():
    def __init__(self):
        self.hp = random.randint(30,80)


class Pnet():

    @classmethod
    def Stack(cls, e, update = False):
        resource = B.nodes[e]["holdings"][-1]
        if update == True:
            B.nodes[e]["holdings"] = B.nodes[e]["holdings"][:-1]

        return resource

    @classmethod
    def add_road(cls, node_name, start_workers = 0):
        x = node_name
        info = []
        if start_workers > 0:
            info = [Worker() for i in range(start_workers)]
        
        B.add_node(node_name, holdings = info, color = "Road", get = cls.Stack, COLOR = 1.0, bipartite = 0)




Pnet.add_road("r1", start_workers=2)
print(B.nodes["r1"]["holdings"])

res = B.nodes["r1"]["get"]
