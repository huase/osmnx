import osmnx as ox
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.cm as cm
from operator import eq, contains
import sys
import logging
import signal
import pickle
import os

ox.config(log_file=False, log_console=False, use_cache=True)
logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(levelname)s %(message)s',
	filename="roadNets.log", #"{:s}_{:s}.log".format(todaysDate, timeNow),
	filemode='w')

class TimeoutException(Exception):
	pass

def timeout_handler(signum, frame):  
	raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)

extenCols =[
'city',
# 'avg_neighbor_degree',
'avg_neighbor_degree_avg',
# 'avg_weighted_neighbor_degree',
'avg_weighted_neighbor_degree_avg',
# 'degree_centrality',
'degree_centrality_avg',
# 'clustering_coefficient',
'clustering_coefficient_avg',
# 'clustering_coefficient_weighted',
'clustering_coefficient_weighted_avg',
# 'pagerank',
'pagerank_max_node',
'pagerank_max',
'pagerank_min_node',
'pagerank_min',
# 'node_connectivity',
'node_connectivity_avg',
'edge_connectivity',
'eccentricity',
'diameter',
'radius',
'center',
'periphery',
# 'closeness_centrality',
'closeness_centrality_avg',
# 'betweenness_centrality',
'betweenness_centrality_avg'
]

def getExtenStats(G): #, areaSqM):
	extenStats = ox.extended_stats(G, connectivity=False, anc=False, ecc=True, bc=False, cc=False)
	# extenStats = pd.Series(extenStats)
	return extenStats

def main():
	import os
	import csv
	import networkx as nx

	output = open("fullneteworkstats.csv", 'w')
	outputWriter = csv.writer(output)

	outputWriter.writerow(extenCols)

	rootdir = 'graphs'

	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			G = nx.read_gpickle(os.path.join(subdir, file))
			try:
				print "Trying...",file
				stats = getExtenStats(G)

				toAdd = [file.split('.gpickle')[0]]
				for stat in basicCols[1:]:
					if stat in stats:
						toAdd.append(str(stats[stat]))
					else:
						toAdd.append('')
				outputWriter.writerow(toAdd)
				print "Success: ",file
			except:
				print "Failed: ",file

if __name__ == "__main__":
	main()
