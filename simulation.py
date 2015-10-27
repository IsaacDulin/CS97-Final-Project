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

class Simulation:
  def __init__(self):

    handlers = {
      'test': self.test,
      'on_window1_destroy': Gtk.main_quit
    }
   



    #Initialize the gui  
    builder = Gtk.Builder()
    builder.add_from_file(GUI_FILE)
    builder.connect_signals(handlers)
    window = builder.get_object("window1")
    window.show_all()

    #Run the main loop
    Gtk.main()

  def updateImage():
    pass

  def test(self, button):
    print "NICE!"

  
