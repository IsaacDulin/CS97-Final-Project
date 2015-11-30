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
from Model import Model

GUI_FILE = 'GUI.glade'
IMG_FILE = 'cs97-temp-img.png'
MAIN_WINDOW = 'window1'

class Simulation:
  def __init__(self):

    handlers = {
      'on_window1_destroy': Gtk.main_quit,
      'erdosRenyi': self.erdosRenyi,
      'barabasiAlbert': self.barabasiAlbert,
      'wattsStrogatz': self.wattsStrogatz,
      'paperGraph': self.paperGraph,
      'changePi': self.changePi,
      'changePhi': self.changePhi,
      'changeDelta': self.changeDelta,
      'changeSize': self.changeSize,
    }

    #Declare class properties and upload GUI 
    self.builder = Gtk.Builder()
    self.model = Model()
    self.builder.add_from_file(GUI_FILE)
    self.builder.connect_signals(handlers)

  def runSimulation(self):
    window = self.builder.get_object(MAIN_WINDOW)
    window.show_all()
    self._refreshView()
    Gtk.main()

  def _refreshView(self):
    #Write updated model to the img file
    self.model.image.draw(IMG_FILE)
    #Read the updated model from the img file to the GUI
    graph_pic = self.builder.get_object('graph_image')
    graph_pic.set_from_file(IMG_FILE)

    totalCrime = self.builder.get_object('total_crime_label')
    totalCrimeText = 'Total Crime Level: '
    crimeLevels = self.model.calculateEquilibrium()[0]
    print crimeLevels
    totalCrime.set_text(totalCrimeText + "{:.3f}".format(sum(crimeLevels)[0]))
    print crimeLevels

    #Update average crime measure
    averageCrime = self.builder.get_object('average_crime_label')
    averageCrimeText = 'Average Crime Level: ' 
    averageCrime.set_text(averageCrimeText + "{:.3f}".format(sum(crimeLevels)[0]/self.model.size))
    
    #Update Key Player
    keyPlayer = self.builder.get_object('key_player_label')
    keyPlayerText = 'Key Player is Identified as '
    keyPlayerValue = self.model.identifyKeyPlayer()
    keyPlayer.set_text(keyPlayerText + keyPlayerValue[1] + ' with x_i = ' + "{:.3f}".format(crimeLevels[int(keyPlayerValue[1])][0]))

    keyLink = self.builder.get_object('key_link_label')
    keyLinkText = 'Key Link is Identified as '
    keyLinkValue = self.model.calculateMaxLink()
    keyLink.set_text(keyLinkText + str(keyLinkValue))

    return 0
  
  def erdosRenyi(self, button):
    self.model.graphErdosRenyi()
    self._refreshView()
    return 0

  def barabasiAlbert(self, button):
    self.model.graphBarabasiAlbert()
    self._refreshView()
    return 0
  
  def wattsStrogatz(self, button):
    self.model.graphWattsStrogatz()
    self._refreshView()
    return 0

  def paperGraph(self, button):
    self.model.graphPaperGraph()
    self._refreshView()
    return 0

  def changePi(self, button):
    scale = self.builder.get_object("pi_scale")
    value = scale.get_value()
    self.model.updatePi(value)
    self._refreshView()
    return 0

  def changePhi(self, button):
    scale = self.builder.get_object("phi_scale")
    value = scale.get_value()
    self.model.updatePhi(value)
    self._refreshView()
    return 0

  def changeDelta(self, button):
    scale = self.builder.get_object("delta_scale")
    value = scale.get_value()
    self.model.updateDelta(value)
    self._refreshView()
    return 0

  def changeSize(self, button):
    spinner = self.builder.get_object("size_spinner")
    value = int(spinner.get_value())
    self.model.updateSize(value)
    self._refreshView()
    return 0
  