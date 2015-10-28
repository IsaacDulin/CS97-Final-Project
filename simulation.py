'''
CS97 Final Project 
Jess Jowdy and Isaac Dulin
Simulation Class

Defines the class that maintains the GUI and communicates the
model's internal representation with the user interface. Most of 
the functions in this class are linked to events in the GUI.
'''

import pygraphviz as pgv
from gi.repository import Gtk
import numpy as np
from model import Model

GUI_FILE = 'GUI.glade'
IMG_FILE = 'cs97-temp-img.png'

class Simulation:
  def __init__(self):

    handlers = {
      'test': self.test,
      'on_window1_destroy': Gtk.main_quit
    }

    #Declare class properties  
    self.builder = Gtk.Builder()
    self.model = Model()

    #initialize the gui
    self.builder.add_from_file(GUI_FILE)
    self.builder.connect_signals(handlers)
    window = self.builder.get_object("window1")
    window.show_all()

    #Run the main loop
    Gtk.main()

  def updateImage(self):
    #Write updated model to the img file
    self.model.graph.layout()
    self.model.graph.draw(IMG_FILE)

    #Read the updated model from the img file to the GUI
    graph_pic = self.builder.get_object("graph_image")
    graph_pic.set_from_file(IMG_FILE)
    
    #return
    return 0

  def test(self, button):
    scale = self.builder.get_object("pi_scale")
    value = scale.get_value()
    self.model.addNode(str(value))
    self.updateImage()
    print value
    return 0     
  
