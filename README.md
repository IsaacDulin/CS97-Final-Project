# CS97-Final-Project

This program simulates a community to model petty crime and the influences of peers and deterence. This project is a replication of the paper "Delinquent Networks" by Coralio Ballester, Anroni Calvo-Armengol, and Yves Zenou.

Running `interactive.py` will create a GUI that lets you play with the different parameters and view the results.

`experiment.py` interacts with the underlying model to allow for custom experiments. It can be used to iterate over different parameter values and plot the results or to just run repeated trials on different randomly generated graphs. For any statistical analysis or data collection, we recommend that you use this file (or variations on it) rather than the GUI.