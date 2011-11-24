import xml.etree.ElementTree as ET, random
from cosmoAgent import Agent
from cosmoConstants import COSMO_USE_PERCENT, ROUTE_CHECK_FREQUENCY_VARIATION, BROADCAST_DISTANCE

class Population:

	def __init__(self, routesFile, network):

		self.__agentList = []
		self.__parsePopulationXML(routesFile, network)
		self.__nextCommunicationId = 0


	def __str__(self):

		if self.__agentList == None:
			return 'None'
		else:
			r = '['
			for agent in self.__agentList:
				r += agent.getAgentId() + ' '
			return r[:-1] + ']'


	# parses the route file to initialize a list of agents
	# with id, route and route check frequency
	def __parsePopulationXML(self, routesFile, network):

		try:
			tree = ET.parse(routesFile).getroot()
			routeSubTrees = tree.findall('route')
			vehicleSubTrees = tree.findall('vehicle')

			for vehicleSubTree in vehicleSubTrees:

				routeId = vehicleSubTree.get('route')
				vehicleId = vehicleSubTree.get('id')
				
				if routeId == None:
					routeEdges = vehicleSubTree.find('route').get('edges').split(' ')
				else:
					for routeSubTree in routeSubTrees:
						if routeSubTree.get('id') == routeId:
							routeEdges = routeSubTree.get('edges').split(' ')

				if random.random() < COSMO_USE_PERCENT:
					self.__agentList.append(Agent(vehicleId, network, routeEdges, eval(ROUTE_CHECK_FREQUENCY_VARIATION)))
				else:
					self.__agentList.append(Agent(vehicleId, network, routeEdges, -1))
		
		except:
			self.__agentList = None


	# checks if population was successfully initialized
	def isValid(self):
		
		if self.__agentList == None:
			return False
		else:
			return True


	def agentActions(self, simulationStep, departedAgents, arrivedAgents, controller):

		# updates agents state for departed and arrived agents
		for agentId in departedAgents:
			for i in range(len(self.__agentList)):
				if agentId == self.__agentList[i].getAgentId():
					self.__agentList[i].setDepartureTime(simulationStep)
					self.__agentList[i].setState(1)

		for agentId in arrivedAgents:
			for i in range(len(self.__agentList)):
				if agentId == self.__agentList[i].getAgentId():
					self.__agentList[i].setArrivalTime(simulationStep)
					self.__agentList[i].setState(2)

		updated = -1
		# updates agents' decisions considering ...
		for agent in self.__agentList:

			# ... the use of cosmos ...
			routeCheckFrequency = agent.getRouteCheckFrequency()
			if routeCheckFrequency != -1:

				# ... state (during trip) ...
				if agent.getState() == 1:

					departureTime = agent.getDepartureTime()
					lastRouteCheck = agent.getLastRouteCheck()

					# ... and route check frequency
					if ((simulationStep - departureTime) / routeCheckFrequency) * routeCheckFrequency > lastRouteCheck:
						position = controller.getAgentsPosition(agent.getAgentId())
						currentEdge = controller.getAgentsCurrentEdge(agent.getAgentId())
						edgeWeights = controller.getNetworkEdgesWeights()

						agent.updateAgentsPositioning(position, currentEdge)
						agent.updateAgentsPerception(edgeWeights)
					
						if(agent.planRoute()):
							controller.setAgentsRoute(agent.getAgentId(), agent.getRoute())

						agent.setLastRouteCheck(simulationStep)

				# on accident ...
				elif agent.getState() == 3:

					# ... updates stop time left and state
					continueTrip = agent.stopStep()
					if continueTrip:
						agent.setState(1)

				# during simulation ...
				if agent.getState() != 0 and agent.getState() != 2:
					updated = self.__resolveCommunications(agent, simulationStep, updated, controller)


	# treats all agents pending communications that were not received this step
	# to all other agents that
	# 	use cosmo
	# 	are active
	# 	are less than BROADCAST_DISTANCE meters away
	# also updates all cosmo users positions in case they were not already this step
	def __resolveCommunications(self, agent, simulationStep, updated, controller):

		treatedCommunication = 0
		for i in range(agent.getNPendingCommunications()):

			j = i-treatedCommunication
			communication = agent.getPendingCommunication(j)
			
			if communication.getReceivedStep() != simulationStep:

				if updated == -1:
					agentId = agent.getAgentId()
					agentsPosition = controller.getAgentsPosition(agentId)
					agentsCurrentEdge = controller.getAgentsCurrentEdge(agentId)
					agent.updateAgentsPositioning(agentsPosition, agentsCurrentEdge)
					updated = 0

				for receivingAgent in self.__agentList:

					routeCheckFrequency = receivingAgent.getRouteCheckFrequency()
					if routeCheckFrequency != -1 and receivingAgent.getState() != 0 and receivingAgent.getState() != 2:

						if updated == 0:
							agentId = receivingAgent.getAgentId()
							agentsPosition = controller.getAgentsPosition(agentId)
							agentsCurrentEdge = controller.getAgentsCurrentEdge(agentId)
							agent.updateAgentsPositioning(agentsPosition, agentsCurrentEdge)

						distance = agent.distanceFrom(receivingAgent.getPosition())
						if distance > 0 and distance <= BROADCAST_DISTANCE:
							print agent.getAgentId(), 'sending communication to', receivingAgent.getAgentId()
							receivingAgent.receiveCommunication(communication, simulationStep)

				agent.treatedCommunication(i-treatedCommunication)
				treatedCommunication += 1
		
		if updated == 0:
			return 1
		else:
			return -1

	# changes agent state and schedules accident communication for cosmo users
	def stop(self, agentId, stopTime, simulationStep, currentEdge):

		for agent in self.__agentList:
			if agent.getAgentId() == agentId:
				agent.setState(3, stopTime)
				if agent.getRouteCheckFrequency() != -1:
					agent.startCommunication(self.__nextCommunicationId, simulationStep, 'broadcast', currentEdge)
					self.__nextCommunicationId += 1
				break
				

	def printPopulationStats(self):
		
		totalTravelTime = 0.0
		for agent in self.__agentList:
			totalTravelTime += agent.getTravelTime()
		print 'Average travel time: ' + str(totalTravelTime/len(self.__agentList))
