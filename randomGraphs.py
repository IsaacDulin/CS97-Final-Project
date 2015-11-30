import Graphs
from itertools import combinations
from numpy.random import multinomial, uniform
from random import choice
from subprocess import call
import numpy as np

def emptyGraph(n):
    nodes = ["v"+str(i) for i in range(n)]
    return Graphs.UndirectedGraph(nodes)


def completeGraph(n):
    nodes = ["v"+str(i) for i in range(n)]
    return Graphs.UndirectedGraph(nodes, combinations(nodes, 2))


def erdosRenyi(n, p=0.05):
    """Generates an undirected Erdos-Renyi random graph.
    In an Erdos-Renyi random graph, each edge is included
    with probability p.

    en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model
    
    n: number of nodes
    p: probability that each pair of nodes is connected
    """
    nodes = range(n)
    edges = filter(lambda e: uniform(0,1) < p, combinations(nodes,2))
    return Graphs.UndirectedGraph(nodes, edges)


def barabasiAlbert(n, d):
    """Generates an undirected Barabasi-Albert  random graph.
    A Barabasi-Albert (A.K.A. preferential atachment) random
    graph starts with a clique of d nodes, then adds nodes 
    sequentially. Each new node is connected to d existing,
    chosen with probability proportional to the existing node's
    degree.

    en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model

    n: number of nodes
    d: degree of each new node
    """
    nodes = range(n)
    edges = set()
    degrees = np.zeros(n)
    for node in nodes:
        degrees[node] += 1
        new_edges = set()
        while degrees[node] <= d and degrees[node] <= node:
            neighbor = list(multinomial(1, degrees / degrees.sum())).index(1)
            e = (node, neighbor)
            if (e in new_edges) or (e[0]==e[1]):
                continue
            new_edges.add(e)
            degrees[neighbor] += 1
            degrees[node] += 1
        edges.update(new_edges)
    return Graphs.UndirectedGraph(nodes, edges)


def wattsStrogatzGraph(n, k=4, p=0.1):
    """Generates an undirected Watts-Strogatz raondom graph.
    A Watts-Strogatz random graph starts from a ring-lattice of
    degree k. With probability p, each lattice edge may be re-
    wired. Edges chosen for re-wiring have one end-point switched
    to a uniformly random node.
    worrydream.com/ScientificCommunicationAsSequentialArt
    
    k: number of neighbors in the initial lattice (must be even)
    p: probability that each local connection gets re-wired.
    """
    nodes = range(n)
    local_edges = []
    for i in range(1,k/2+1):
        local_edges.extend(zip(nodes, range(i,n) + range(i)))
    g = Graphs.UndirectedGraph(nodes, local_edges)
    for e in local_edges:
        if uniform() < p:
            g.addEdge(e[0], choice(list(g.nodes - g.edges[e[0]] - {e[0]})))
            g.removeEdge(*e)
    return g


def uniformSpanningTree(n):
    """Uniform spanning tree over the complete graph on n nodes.

    en.wikipedia.org/wiki/Loop-erased_random_walk#The_uniform_spanning_tree
    """
    new_nodes = range(n)
    tree_nodes = set()
    edges = set()
    first_node = new_nodes.pop(choice(new_nodes))
    tree_nodes.add(first_node)
    while len(tree_nodes) < n:
        src_node = choice(new_nodes)
        path = [src_node]
        while src_node in new_nodes:
            tree_nodes.add(src_node)
            new_nodes.pop(new_nodes.index(src_node))
            dst_node = choice(range(n))
            while dst_node in path:
                dst_node = choice(range(n))
            edges.add(Edge(src_node, dst_node))
            path.append(dst_node)
            src_node = dst_node
    return Graphs.UndirectedGraph(tree_nodes, edges)


def balancedBinaryTree(n):
    return Graphs.UndirectedGraph(range(n), [(i, (i-1)/2) for i in range(1,n)])


def lineGraph(n):
    return Graphs.UndirectedGraph(range(n), [(i, i+1) for i in range(n-1)])


def ringGraph(n):
    G = LineGraph(n)
    G.addEdge(n-1, 0)
    return G


def emptyGraph(n):
    return Graphs.UndirectedGraph(range(n))


def completeGraph(n):
    return Graphs.UndirectedGraph(range(n), combinations(range(n), 2))


def randomEdgeDirections(graph):
    edges = []
    for src, dst in set(map(lambda e: tuple(sorted(e)), graph.allEdges())):
        if uniform(0,1) < 0.5:
            edges.append((src, dst))
        else:
            edges.append((dst, src))
    return Graphs.DirectedGraph(graph.nodes, edges)

def paperGraph(n=11):
    edges = []
    for i in range(1, (n/2)+1):
        for j in range(1, (n/2)+1):
            if (i != j):
                edges.append((i,j))
    for i in range((n/2)+1, n):
        for j in range((n/2)+1, n):
            if (i != j):
                edges.append((i,j))

    edges.append((0,1))
    edges.append((0,n/2))
    edges.append((0,n/2+1))
    edges.append((0,n-1))

    return Graphs.UndirectedGraph(range(n), edges)

def coolGraph(n=22, cluster_n=4, p1=.9, p2=0.8):
  #generates a cool graph. There are n nodes, and there
  #are cluster_n number of clusters. The size of each cluster
  #is n/(cluster_n - 1). There is one clusters' worth of nodes that 
  #are reserved to be bridge style nodes. Within clusters there is 
  #a high probability of connection, and every node also has a small
  #probability of connecting with a connector node.
  print n
  print cluster_n
  cluster_size = int(n/cluster_n)
  edges = []
  clusters = [[]]*(cluster_n)
  connectors = range(n)[(cluster_size*cluster_n-1):n]
  for i in range(0, cluster_size*cluster_n):
    clusters[i%cluster_size].append(i)

    for j in range(i,cluster_size*cluster_n):
      if i!=j and i%cluster_size==j%cluster_size:
        if uniform(0,1)<p1:
          edges.append((i,j))

  for connector in connectors:
    for cluster in clusters:
      if uniform(0,1)<p2:
        edges.append((i, choice(cluster)))


  return Graphs.UndirectedGraph(range(n), edges)



def moreConnectedPaperGraph(n=12):
    return Graphs



def addWeights(graph, weight_func=lambda x,y: 1):
    edges = [(e[0], e[1], weight_func(e[0], e[1])) for e in graph.allEdges()]
    return Graphs.WeightedDirectedGraph(graph.nodes, edges)


def graph_gif(graph_sequence, filename="contagion"):
    for i,g in enumerate(graph_sequence):
        fn = filename + "_temp" + str(i).zfill(int(math.log( \
                                   len(graph_sequence), 10)+1))
        g.to_dot(fn)
        call("neato -Tpng "+fn+".dot > "+fn+".png", \
                        shell=True)
        call("rm "+fn+".dot", shell=True)
    call("convert -delay 100 "+filename+"_temp*.png "+ \
                    filename+".gif", shell=True)
    call("rm "+filename+"_temp*.png", shell=True)

