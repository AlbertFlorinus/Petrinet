import networkx as nx
B = nx.DiGraph()
B.add_node("r1")
B.add_node("r2")
B.add_node("r4")
B.add_edge("r1", "r2")
B.add_edge("r2", "r4")
B.add_edge("r4", "r1")
B.add_edge("r4", "r2")

x = B.in_edges("r2")
print(type(x))
print(x)