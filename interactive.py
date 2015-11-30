'''
CS97 Final Project 
Jess Jowdy and Isaac Dulin

Does very little on its own. Simply creates an instance
of the simulation class and then runs it. All of the
actual work is done by the underlying classes.
'''

from Simulation import Simulation

if __name__ == '__main__':
  #Run the main code
  simulation = Simulation()
  simulation.runSimulation()