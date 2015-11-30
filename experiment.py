'''
CS97 Final Project 
Jess Jowdy and Isaac Dulin
'''


from Model import Model
import numpy as np
import matplotlib.pyplot as plt


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
  #model.calculateMaxLink()
  #rho = model.calculateRho()
  #if rho*((pi*phi)/delta) > 1:
  #  print pi, phi, delta, "Centrality May Not be Well Defined"

  return sum(model.calculateEquilibrium()[0])

if __name__ == '__main__':
  #Run the main code
  trials = np.arange(0, .099, .001)
  crime1, crime2 = [], []
  type1 = [(1,0),(0,10),(0,6),(0,5),(5,0),(10,0),(0,1),(6,0)]
  type2 = [(1,5),(10,6),(6,10),(5,1)]
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

