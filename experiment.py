'''
CS97 Final Project 
Jess Jowdy and Isaac Dulin

This is an example of how to use the underlying model to run more
extensive experiments. While the GUI is great for observing trends
and messing around with different parameters, it's not great for 
generating plots or running large tests. This script should be used
for that instead.
'''

from Model import Model
import numpy as np
import matplotlib.pyplot as plt


#Runs a single 'trial' with a specified graph type, size, and model parameters.
#The return value should be changed based on the plot that's desired. Right now,
#it returns the aggregate crime levels at equilibrium (the sume of the equilibrium 
#values).
def run_trial(size=11, graph_type='paper', pi=.5, phi=.5, delta=.5):

  model = Model()
  model.updatePi(pi)
  model.updatePhi(phi)
  model.updateDelta(delta)
  model.updateSize(size)
  typeFunctions = {'ER': model.graphErdosRenyi,
                   'BA': model.graphBarabasiAlbert,
                   'WS': model.graphWattsStrogatz,
                   'paper': model.graphPaperGraph,
                   'cool': model.graphCoolGraph}
  typeFunctions[graph_type]

  return sum(model.calculateEquilibrium()[0])

if __name__ == '__main__':
  #Run the main code
  trials = np.arange(0, .099, .001)
  crime1, crime2 = [], []
  type1 = [(1,0),(0,10),(0,6),(0,5),(5,0),(10,0),(0,1),(6,0)]
  type2 = [(1,5),(10,6),(6,10),(5,1)]
  
  #Runs a set of trials with varying deterrence
  for trial in trials:
    crime1.append(run_trial(size=11, graph_type='BA', phi=.8, delta=.2, pi=trial))
    crime2.append(run_trial(size=11, graph_type='BA', phi=.2, delta=.2, pi=trial))
 
  plt.title('Effect of Increased Deterrence on Aggregate Crime (Barabasi Albert Graph)')
  plt.xlabel('Deterrence Level (pi)')
  plt.ylabel('Aggregate Crime Level')
  handle1, = plt.plot(trials, crime1)
  handle2, = plt.plot(trials, crime2, 'r')
  plt.legend([handle1, handle2], ['High Local Connectivity \n(phi=.8)', 'Low Local Connectivity \n(phi=.2)'], loc=2)
  plt.show()

