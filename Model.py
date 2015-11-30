'''
CS97 Final Project 
Jess Jowdy and Isaac Dulin
Model Class

Defines the class that stores the internal representation of the 
model. This includes a representation of the graph (stored as an
AGraph from pygraphviz) along with current variable values including 
pi, delta, and phi. This class also contains functions to generate
information about the graph including identifying the key player, 
calculating aggregate crime levels, and finding the centrality 
measurement.
'''

#Some questions:
# 1) What is rho, spectral radius? Suspicion: Eigenvalues Centrality.
# 2) Can we snipe your graph creation code?
# 3) How to generate initial involvement (random)? 
# 4) Condition for intercentrality 

IMG_FILE = 'cs97-temp-img.png'

import pygraphviz as pgv
from gi.repository import Gtk
import numpy as np
import randomGraphs as rg
import random

class Model:
  def __init__(self):
    self.pi = .5
    self.delta = .5 
    self.phi = .5
    
    self.size = 11
    self.image = pgv.AGraph() #Use pygraphviz to generate the img
    self.graph = rg.completeGraph(self.size)
    self.refreshImage()
  
  def updatePi(self, newPi):
    self.pi = newPi
    return 0

  def updateDelta(self, newDelta):
    self.delta = newDelta
    return 0

  def updatePhi(self, newPhi):
    self.phi = newPhi
    return 0

  def updateSize(self, newSize):
    self.size = newSize
    self.involvement = dict()
    for i in range(0, self.size):
      self.involvement[i] = random.random()
    self.graphErdosRenyi()
    self.refreshImage()
    return 0

  def refreshImage(self):
    edges = self.graph.allEdges()
    self.image = pgv.AGraph() #Create a new graph
    for i in range(0, self.size):
      self.image.add_node(str(i))
    for edge in edges:
      self.image.add_edge(edge)
    self.image.layout()
    self.image.draw(IMG_FILE)
    return 0

  def calculateIndividualPayoff(self, node):
    #Calculates the payoff, u, for an individual node in the graph
    u = 0
    x_i = self.involvement[node]
    
    u += (1 - self.pi) * x_i - self.delta* x_i**2 
    
    for j in range(0, self.size):
      if (neighbors[j] != node):
        u -= self.delta * x_i * self.involvement[str(j)]
      if self.graph.has_neighbor(node, str(j)):
        u += self.pi * self.phi * x_i * self.involvement[str(j)]

    return u


  def calculateRho(self):
    adj_mat = self._generateAdjacencyMatrix()
    w, v = np.linalg.eig(adj_mat)
    rho = max(abs(w))
    return rho


  def identifyKeyPlayer(self):
    x_star_best = np.inf
    best_i = None
    for i in range(0, self.size):
      x_star_i = float(sum(self.calculateEquilibrium(i)[0]))
      if x_star_i < x_star_best:
        x_star_best = x_star_i
        best_i = str(i)

    return x_star_best, best_i

  def calculateMaxLink(self):
    max_link = None
    max_value = -np.inf
    for i in range(0, self.size):
      for j in range(0, self.size):
        value = self.calculateLinkContribution(i, j)
        #print (i,j) , value
        if value > max_value:
          max_link = (i, j)
          max_value = value

    return max_link

  def calculateLinkContribution(self, node1, node2):
    theta = (self.pi*self.phi)/self.delta
    _, b_vec, M = self.calculateEquilibrium()
    adj_mat = self._generateAdjacencyMatrix()
    if adj_mat[node1][node2] == 0:
      return 0 
    contribution  = 2 * b_vec[node1] * b_vec[node2] * (1+theta*M[node1][node2])
    contribution -= theta * (((b_vec[node1]**2) * M[node2][node2]) + ((b_vec[node2]**2) * M[node1][node1]))
    contribution /= (((1 + theta*M[node1][node2])**2) - ((theta**2) * M[node1][node1] * M[node2][node2]))

    return theta*contribution[0]

  def calculateEquilibrium(self, excluded_node=-1):
    #Calculates the Katz-Bonacich centrality measure
    G = self._generateAdjacencyMatrix(excluded_node)
    
    if (excluded_node>=0):
      I = np.identity(self.size-1)
      ones = np.ones((self.size-1, 1))
    else:
      I = np.identity(self.size)
      ones = np.ones((self.size, 1))

    theta = (self.pi*self.phi)/float(self.delta)

    M = np.linalg.inv(I - theta * G)
    b_vec = np.dot(M, ones)
    b_scalar = sum(b_vec)
    x_star = ((1-self.pi)/(self.delta*(1+b_scalar)))*b_vec

    return x_star, b_vec, M

  def _generateAdjacencyMatrix(self, excluded_node=-1):
    adj_mat = np.zeros((self.size, self.size))
    edges = self.graph.allEdges()
    for edge in edges:
      adj_mat[edge[0],edge[1]] = 1
      adj_mat[edge[1],edge[0]] = 1

    if (excluded_node >= 0):
      adj_mat = np.delete(adj_mat, excluded_node, 0)
      adj_mat = np.delete(adj_mat, excluded_node, 1)
    return adj_mat

  def graphErdosRenyi(self, p=.4):
    self.graph = rg.erdosRenyi(self.size, p)
    self.refreshImage()
    return 0

  def graphBarabasiAlbert(self, d=4):
    self.graph = rg.barabasiAlbert(self.size, d)
    self.refreshImage()
    return 0

  def graphWattsStrogatz(self):
    self.graph = rg.wattsStrogatzGraph(self.size)
    self.refreshImage()
    return 0

  def graphPaperGraph(self, n=11):
    self.size = n
    self.graph = rg.paperGraph(n)
    self.refreshImage()
    return 0

  def graphCoolGraph(self, n1=20, n2=5):
    self.size = n1
    self.graph = rg.coolGraph(n=n1, cluster_n=n2)
    self.refreshImage()
    return 0


  def moreConnectedPaperGraph(self):
    self.size = 12
    self.graph = rg.moreConnectedPaperGraph()
    self.refreshImage()
    return 0