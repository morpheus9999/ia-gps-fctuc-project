import math, random
from cosmoCommunication import Communication
from cosmoConstants import ACCEPT_NEW_ROUTE_PROB, ROUTING_ALGORITHM

class Agent:

	def __init__(self, network, route, routeCheckFrequency):

		self.__departureTime = -1
		self.__arrivalTime = -1
		self.__stopTime = -1
		self.__state = 0
		self.__position = (0,0)
		self.__currentLane = ''
		self.__currentSpeed = 0
		self.__network = network
		self.__route = route
		self.__routeCheckFrequency = routeCheckFrequency
		self.__lastRouteCheck = -1
		self.__pendingCommunications = []
		self.__ignoringCommunications = []


	def __str__(self):

		return '[Agent]' + \
			'\n\tDepartureTime: ' + str(self.__departureTime) + \
			'\n\tArrivalTime: ' + str(self.__arrivalTime) + \
			'\n\tStopTime: ' + str(self.__stopTime) + \
			'\n\tState: ' + str(self.__state) + \
			'\n\tPosition: ' + str(self.__position) + \
			'\n\tLane: ' + self.__Lane + \
			'\n\tSpeed: ' + self.__Speed + \
			'\n\tNetworkEdgeWeights: ' + str(self.__network.getEdgeWeights()) + \
			'\n\tRoute: ' + str(self.__route) + \
			'\n\tRouteCheckFrequency: ' + str(self.__routeCheckFrequency) + \
			'\n\tLastRouteCheck: ' + str(self.__lastRouteCheck) + \
			'\n\tPendingCommunications: ' + str(self.__pendingCommunications) + \
			'\n\tIgnoringCommunications: ' + str(self.__ignoringCommunications)


	def getDepartureTime(self):

		return self.__departureTime


	def setDepartureTime(self, departureTime):

		self.__departureTime = departureTime
		self.__state = 1


	def setArrivalTime(self, arrivalTime):

		self.__arrivalTime = arrivalTime
		self.__state = 2


	def stopStart(self, lane, stopTime, simulationStep, commId):

		self.__stopTime = stopTime
		self.__state = 3
		
		if self.__routeCheckFrequency != -1:
			self.__startCommunication(commId, simulationStep, 'broadcast', lane)
			return 1
				
		return 0


	def stopStep(self):

		self.__stopTime -= 1
		if self.__stopTime <= 0:
			self.__state = 1


	# get agent state (0.before trip, 1.during trip, 2.after trip, 3.accident)
	def getState(self):

		return self.__state


	def getPosition(self):

		return self.__position


	def updateAgentPosition(self, position):
		
		self.__position = position


	def getLane(self):
		
		return self.__lane


	def updateAgentLane(self, lane):
		
		self.__lane = lane


	def getSpeed(self):

		return self.__speed
		
		
	def updateAgentSpeed(self, speed):
		
		self.__speed = speed


	# return distance in meters from received agent
	def distanceFrom(self, position):

		return math.sqrt(pow(self.__position[0]-position[0], 2) + pow(self.__position[1]-position[1], 2))


	def updateAgentPerception(self, edgeWeights):

		self.__network.setEdgeWeights(edgeWeights)


	def getRoute(self):

		return self.__route


	# returns
	# -1 - current edge is internal
	#  0 - the routing algorithm found no valid path
	#      the new route is the same as the current one
	#      the agent decided to reject the new route
	#  1 - a new route is accepted
	def planRoute(self, agentId):

		# computes new route based on agents perception and received information
		newRoute = self.__network.getRoute(self.__lane[:self.__lane.rfind('_')], self.__route[-1], ROUTING_ALGORITHM)

		if(newRoute == None):
			return -1
		
		if(len(newRoute) == 0):
			return 0
		
		# updates current route to start at current edge
		oldRoute = self.__route[self.__route.index(newRoute[0]):]

		# checks if newly computed route is different than the current one
		if(newRoute != oldRoute):
			# checks if agent is interested in following the new route
			if random.random() < ACCEPT_NEW_ROUTE_PROB:
				self.__route = newRoute
				return 1

		return 0


	def getRouteCheckFrequency(self):

		return self.__routeCheckFrequency


	def getLastRouteCheck(self):

		return self.__lastRouteCheck


	def setLastRouteCheck(self, simulationStep):

		self.__lastRouteCheck = simulationStep


	def getNPendingCommunications(self):

		return len(self.__pendingCommunications)


	def getPendingCommunication(self, i):

		return self.__pendingCommunications[i]


	def __startCommunication(self, communicationId, receivedStep, communicationType, lane):

		newCommunication = Communication(communicationId, receivedStep, communicationType, ('Accident on ' + lane))
		self.__pendingCommunications.append(newCommunication)
		self.__ignoringCommunications.append(newCommunication.getCommunicationId())


	def receiveCommunication(self, communication, simulationStep):

		# Ignores already received communications
		try:
			commId = communication.getCommunicationId()
			self.__ignoringCommunications.index(commId)
		except:
			commType = communication.getType()
			newCommunication = Communication(commId, simulationStep, commType, communication.getMessage())
			self.__ignoringCommunications.append(commId)
			if commType == 'broadcast':
				self.__pendingCommunications.append(newCommunication)


	def treatedCommunication(self, i):

		self.__pendingCommunications.pop(i)
