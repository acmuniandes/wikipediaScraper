import networkx as nx
import matplotlib.pyplot as plt
plt.use("Agg")
G=nx.Graph()
G.add_node(1)

nx.draw(G)
G=nx.path_graph(4)
cities = {0:"Toronto",1:"London",2:"Berlin",3:"New York"}

H=nx.relabel_nodes(G,cities)

print("Nodes of graph: ")
print(H.nodes())
print("Edges of graph: ")
print(H.edges())
nx.draw(H)
plt.savefig("path_graph_cities.png")
plt.show()
