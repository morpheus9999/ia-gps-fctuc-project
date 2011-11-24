import numpy, random, xml.etree.ElementTree as ET
from priodict import priorityDictionary
from cosmoConstants import OCCUPANCY_LIMIT, WEIGHT_VARIATION

class Network:

	def __init__(self, networkFile):

		self.__graph = self.__parseNetworkXML(networkFile)
		self.__edgeWeights = {}
		self.__occupancyAvgs = []
		self.__occupancyStdDevs = []

	# returns a better display of the network graph
	# with a key (edge) in each line
	# and numbers with a maximum of 2 decimal digits
	def __str__(self):
		
		r = ''
		
		if self.__graph == None:
			r = 'None'
		else:
			for key in self.__graph:
				r += '{\'' + str(key) + '\': {%.2f} {' % self.__edgeWeights.get(key)
				subGraph = self.__graph.get(key)
				for subKey in subGraph:
					r += '\'' + str(subKey) + '\': %.2f, ' % subGraph.get(subKey)
				r = r[:-2] + '}}\n'
			r = r[:-1]
			
		return r

	# parses the network's file
	# to create a graph of the network (dictionary of dictionaries of distances between edges)
	def __parseNetworkXML(self, networkFile):

		try:
			print networkFile
			tree = ET.parse(networkFile)
			print "Entra 16"
			# parses the network normal edge distances
			distances = {}
			edges = tree.getroot().findall('edge')
			print "Entra 10"
			for edge in edges:
				if edge[0] != ':':
					edge.find('lanes').find('lane')
					distances[edge.get('id')] = float(edge.find('lanes').find('lane').get('length'))
			
			# parses the network succeeding edges
			graph = {}
			succs = tree.getroot().findall('succ')
			print "Entra 11"
			for succ in succs:
				edge = succ.get('edge')
			
				if edge[0] != ':':
					graphKey = graph.get(edge)
					if graphKey == None:
						graphKey = graph[edge] = {}
			
					succlanes = succ.findall('succlane')
					for succlane in succlanes:
						succEdge = (succlane.get('lane'))[:-2]
						if succEdge != 'SUMO_NO_DESTINATI':
							if graphKey.get(succEdge) == None:
								graphKey[succEdge] = distances[succEdge]
			print "Entra 13"				
			return graph
		
		except:
			print "Entra nulo"
			return None

	
	# returns the network graph
	def getGraph(self):

		return self.__graph


	# returns the network edge weights
	def getEdgeWeights(self):

		return self.__edgeWeights


	# updates the network edge occupancy given a weight dictionary
	def setEdgeWeights(self, edgeWeights):

		self.__edgeWeights = edgeWeights
			

	# returns the shortest route (list of edges) considering only edge length
	def getRoute(self, startEdge, endEdge, algorithm):

		# if startEdge is internal
		if startEdge[0] == ':':
			return None

		# applies dijkstra's algorithm
		# to find the lightest route (list of edges) between the startEdge to the endEdge
		# in the self.__graph network
		D = {}
		P = {}
		Q = priorityDictionary()
		Q[startEdge] = 0
		
		# alters the edge weights if the error insertion is the chosen algorithm
		alteredEdgeWeights = {}
		if algorithm == 3:
			for edge, weight in self.__edgeWeights.iteritems():
				newWeight = weight * WEIGHT_VARIATION
				alteredEdgeWeights[edge] = weight + random.uniform(-newWeight, newWeight)
				

		for v in Q:
			D[v] = Q[v]
			if v == endEdge:
				break
			for w in self.__graph[v]:
				
				vwValue = 0
				# DistanceDijkstra - algorithm = 0
				if algorithm == 0:
					vwValue = D[v] + self.__graph[v][w]
				# OccupancyDijsktra - algorithm = 1
				elif algorithm == 1:
					vwValue = D[v] + self.__graph[v][w] + pow((self.__graph[v][w] * self.__edgeWeights[w]), 2)
				elif algorithm == 2:
					if(self.__edgeWeights[w]>OCCUPANCY_LIMIT):
						break
					vwValue = D[v] + self.__graph[v][w]
				# ErrorInsertion - algorithm = 3
				elif algorithm == 3:
					vwValue = D[v] + self.__graph[v][w] + pow((self.__graph[v][w] * alteredEdgeWeights[w]), 2)
				
				if w in D:
					if vwValue < D[w]:
						raise ValueError, "Dijkstra: found better path to already-final vertex"
				elif w not in Q or vwValue < Q[w]:
					Q[w] = vwValue
					P[w] = v

		# computes the route from the dictionary with the preceding edges (P)
		try:
			route = []
			toEdge = endEdge
			while endEdge != startEdge:
				endEdge = P[endEdge]
				route.insert(0, toEdge)
				toEdge = endEdge
			route.insert(0, toEdge)
		except:
			print '>>>>>>>>>>>>>>>> safo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <<<<<<<<<<<<<<<<<<<'
			return []

		return route


	# stores the average and standard deviation of current link occupancies 
	def updateOccupancyStats(self):

		sum = numpy.sum(self.__edgeWeights.values())
		
		# if there are cars on the network!!!
		if sum != 0:

			avg = float(sum) / len(self.__edgeWeights)
			stdDev = numpy.std(self.__edgeWeights.values())
			
			self.__occupancyAvgs.append(avg)
			self.__occupancyStdDevs.append(stdDev)


	# returns the average of averages and standard deviation of occupancies
	def returnOccupancyStats(self):
		
		# print self.__occupancyAvgs
		# print numpy.average(self.__occupancyAvgs)
		# print self.__occupancyStdDevs
		# print numpy.average(self.__occupancyStdDevs)
		
		return numpy.average(self.__occupancyAvgs), numpy.average(self.__occupancyStdDevs)