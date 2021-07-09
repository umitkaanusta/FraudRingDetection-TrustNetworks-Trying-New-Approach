import networkx as nx


def fairness_goodness(G: nx.DiGraph):
    # Fairness between [0, 1], goodness between [-1, 1]
    fairness = {}
    goodness = {}
    nodes = G.nodes()
    for node in nodes:
        fairness[node] = 1
        goodness[node] = 0
    epsilon = 0.001
    i = 0
    while i < 100:
        flag_f = False
        flag_g = False
        # Goodness
        for node in nodes:
            in_edges_ = G.in_edges(node, data="weight")
            if len(in_edges_) > 0:
                curr_g = 0
                for e in in_edges_:
                    curr_g += fairness[e[0]] * (e[2] / 10)
                curr_g /= len(in_edges_)
                if not flag_g and abs(curr_g - goodness[node]) < epsilon:
                    flag_g = True
                goodness[node] = curr_g
        # Fairness
        for node in nodes:
            out_edges_ = G.out_edges(node, data="weight")
            if len(out_edges_) > 0:
                curr_f = 0
                for e in out_edges_:
                    curr_f += abs((e[2] / 10) - goodness[e[1]])
                curr_f /= (2 * len(out_edges_))
                curr_f = 1 - curr_f
                if not flag_f and abs(curr_f - goodness[node]) < epsilon:
                    flag_f = True
                fairness[node] = curr_f
        if flag_f and flag_g:
            break
        i += 1
    return fairness, goodness


def naive_goodness(goodness):
    naive_g = {}
    for node, g in goodness.items():
        naive_g[node] = int(g >= 0)
    return naive_g


def naive_node_assortativity(G: nx.DiGraph, goodness):
    naive_goodness_ = naive_goodness(goodness)
    assort = {}
    for node in G.nodes():
        degree = G.in_degree(node) + G.out_degree(node)
        if degree == 0:
            disass[node] = 0
            continue
        same = 0
        node_goodness = naive_goodness_[node]
        for neighbor in G.predecessors(node):
            same += int(naive_goodness_[neighbor] == node_goodness)
        for neighbor in G.successors(node):
            same += int(naive_goodness_[neighbor] == node_goodness)
        assort[node] = same / degree
    return assort


def naive_node_assortativity_pos_neg(G, goodness, pos=True):
    nna = naive_node_assortativity(G, goodness)
    ng = naive_goodness(goodness)
    data = {}
    if pos:
        for node, g in ng.items():
            if g:
                data[node] = nna[node]
    else:
        for node, g in ng.items():
            if not g:
                data[node] = nna[node]
    return data
