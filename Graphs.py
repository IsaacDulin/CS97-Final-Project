from heapq import heappush, heappop

class PathError(Exception):
    def __init__(self):
        Exception.__init__(self, 'origin and destination are disconnected')

class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = set()
        self.edges = dict()
        for node in nodes:
            self.addNode(node)
        for edge in edges:
            self.addEdge(*edge)
        self.colors = {n:"white" for n in self.nodes}

    def addNode(self, node):
        assert node not in self.nodes, "node " +str(node)+ " already exists"
        self.nodes.add(node)
        self.edges[node] = set()

    def removeNode(self, node):
        del self.edges[node]
        map(lambda s: s.discard(node), self.edges.values())
        self.nodes.remove(node)

    def addEdge(self, *args):
        raise NotImplementedError("use DirectedGraph or UndirectedGraph")

    def removeEdge(self, *args):
        raise NotImplementedError("use DirectedGraph or UndirectedGraph")

    def adjacent(self, n1, n2):
        return n2 in self.edges[n1]

    def degree(self, node):
        return len(self.edges[node])

    def allEdges(self):
        return sum([[(node, neighbor) for neighbor in self.edges[node]] for \
                node in self.nodes], [])

    def numEdges(self):
        return sum(map(len, self.edges.values()))

    def adjacencyMatrix(self):
        adj = [[0]*len(self.nodes) for i in range(len(self.nodes))]
        for node in self.nodes:
            for neighbor in self.edges[node]:
                adj[node][neighbor] = 1
        return adj

    def shortestPath(self, origin, destination, edgeCost=lambda src,dst: 1, \
                heuristic=lambda src,dst: 0):
        """Find the shortest path between origin and destination.
        The shortest path is found by A* search, so the distance heuristic
        should be admissable (never overestimating). With the default values
        for edgeCost and heuristic, the search reduces to BFS.
        The path is returned as a list of nodes.
        If no path exists, a PathError is raised."""
        queue = []
        visited = set()
        pathCosts = {origin:0}
        parents = {origin:None}
        heappush(queue, (0, origin))
        while queue:
            priority, node = heappop(queue)
            if node == destination:
                break
            if node in visited:
                continue
            visited.add(node)
            for neighbor in self.edges[node]:
                if neighbor in visited:
                    continue
                newPathCost = pathCosts[node] + edgeCost(node, neighbor)
                if neighbor in pathCosts:
                    if pathCosts[neighbor] <= newPathCost:
                        continue
                parents[neighbor] = node
                pathCosts[neighbor] = newPathCost
                heappush(queue, (heuristic(neighbor, destination) + \
                        newPathCost, neighbor))
        if node != destination:
            raise PathError()
        path = []
        while node != None:
            path = [node] + path
            node = parents[node]
        return path

    def __repr__(self):
        return self.__class__.__name__ + ': ' + str(len(self.nodes)) + \
                ' nodes, ' + str(self.numEdges()) + ' edges'

    def dot_nodes(self):
        dot = ""
        for n in self.nodes:
            dot += str(n) + " [label=\"\", style=filled, shape=circle, "
            dot += "fillcolor=" + self.colors[n] + "];\n"
        return dot

    def dot_edges(self, edge_type):
        dot = ""
        for e in self.allEdges():
            dot += str(e[0]) + " " + edge_type + " " + str(e[1])
            dot += " [penwidth=2];\n"
        return dot

    def to_dot(self, filename, graph_type, edge_type):
        dot = graph_type + " {\noverlap=scale;\nsep=1;\n" 
        dot += self.dot_nodes() + self.dot_edges(edge_type) + "}"
        if filename != "":
            with open(filename, "w") as f:
                f.write(dot)
        else:
            return dot


class UndirectedGraph(Graph):
    def addEdge(self, n1, n2):
        self.edges[n1].add(n2)
        self.edges[n2].add(n1)

    def removeEdge(self, n1, n2):
        self.edges[n1].remove(n2)
        self.edges[n2].remove(n1)
    
    def numEdges(self):
        return Graph.numEdges(self)/2

    def allEdges(self):
        return sorted(set(map(tuple, map(sorted, Graph.allEdges(self)))))

    def to_dot(self, filename=""):
        return Graph.to_dot(self, filename, "graph", "--")


class DirectedGraph(Graph):
    def addEdge(self, src, dst):
        self.edges[src].add(dst)

    def removeEdge(self, src, dst):
        self.edges[src].remove(dst)

    def to_dot(self, filename=""):
        return Graph.to_dot(self, filename, "digraph", "->")


class WeightedDirectedGraph(DirectedGraph):
    def __init__(self, nodes=[], weightedEdges=[]):
        self.weights = dict()
        DirectedGraph.__init__(self, nodes, weightedEdges)

    def addEdge(self, src, dst, weight):
        DirectedGraph.addEdge(self, src, dst)
        self.weights[(src, dst)] = weight

    def removeNode(self, node):
        for edge in filter(lambda edge: node in edge, self.weights.keys()):
            del self.weights[edge]
        DirectedGraph.removeNode(self, node)

    def removeEdge(self, src, dst):
        DirectedGraph.removeEdge(self, src, dst)
        del self.weights[(src, dst)]

    def allEdges(self):
        return [(src, dst, self.weights[src, dst]) for src, dst in \
                DirectedGraph.allEdges(self)]

    def adjacencyMatrix(self):
        adj = [[0]*len(self.nodes) for i in range(len(self.nodes))]
        for node in self.nodes:
            for neighbor in self.edges[node]:
                adj[node][neighbor] = self.weights[(node, neighbor)]
        return adj

    def dot_edges(self, edge_type):
        dot = ""
        for e in self.allEdges():
            dot += str(e[0]) + " " + edge_type + " " + str(e[1])
            dot += " [penwidth=2, label="+str(e[2])+"];\n"
        return dot
