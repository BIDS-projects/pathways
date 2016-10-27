import networkx as nx
import matplotlib.pyplot as plt


G=nx.Graph()
all_graphs = []
current_graph = []

with open("./cluster_paths/all.txt", "r") as read_paths:
	for line in read_paths:
		indents = line.count("\t")
		if not indents:
			current_graph = [line]
			if current_graph:
				all_graphs.append(current_graph)
		else:
			current_graph.append(line)
			G.add_edge(current_graph[indents],current_graph[indents - 1])
		G.add_node(line, course=line)

nx.draw(G)
plt.show()
