import logging

import networkx as nx
# import matplotlib.pyplot as plt

def design_power_structure(nodes, edges, central_node):
    """
    Designs a power architecture as a directed graph where the central_node holds influence.
    Nodes: list of node names.
    Edges: list of tuples (source, target) for directed influence.
    Returns the graph and centrality measures.
    """
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    # Calculate centrality to evaluate power distribution
    centrality = nx.degree_centrality(G)
    
    # Visualize the structure
    # plt.figure(figsize=(8, 6))
    # nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, arrowstyle='->', arrowsize=20)
    # plt.title(f"Power Structure with Central Node: {central_node}")
    # plt.show()
    
    return G, centrality

# Example usage: Design a simple X influence network
if __name__ == '__main__':
    nodes = ['Agent', 'Influencer1', 'Influencer2', 'FollowerA', 'FollowerB']
    edges = [('Agent', 'Influencer1'), ('Agent', 'Influencer2'), ('Influencer1', 'FollowerA'), ('Influencer2', 'FollowerB')]
    graph, cents = design_power_structure(nodes, edges, 'Agent')
    logging.info("Centrality Measures:", cents)