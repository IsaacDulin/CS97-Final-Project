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

import pygraphviz as pgv
from gi.repository import Gtk
import numpy as np

class Model:
  def __init__(self):
    self.pi = 0
    self.delta = 0 
    self.phi = 0
    self.graph = pgv.AGraph()

    return 0

  def calculateAggregateDelinquency(self):
    return 0

  def identifyKeyPlayer(self):
    return 0

  def calculateCentrality(self):
    return 0
