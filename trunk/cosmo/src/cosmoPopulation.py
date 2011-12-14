import math, random, xml.etree.ElementTree as ET
from cosmoAgent import Agent
from cosmoConstants import COSMO_USE_PERCENT, ROUTE_CHECK_FREQUENCY_VARIATION, BROADCAST_DISTANCE

class Population:

	def __init__(self, routesFile, network):

		self.__agentList = {}
		self.__parsePopulationXML(routesFile, network)
		self.__nextCommunicationId = 0

		self.__routePlansTimes = []

	def __str__(self):

		if self.__agentList == None:
			return 'None'
		else:
			return str(sorted(self.__agentList))


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
					self.__agentList[vehicleId] = Agent(network, routeEdges, eval(ROUTE_CHECK_FREQUENCY_VARIATION))
				else:
					self.__agentList[vehicleId] = Agent(network, routeEdges, -1)
		
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
			self.__agentList[agentId].setDepartureTime(simulationStep)

		for agentId in arrivedAgents:
			self.__agentList[agentId].setArrivalTime(simulationStep)

		# updates agents decisions considering ...
		updatedPositions = False
		for agentId, agent in self.__agentList.iteritems():
                        
			# ... the use of cosmos ...
			routeCheckFrequency = agent.getRouteCheckFrequency()
			if routeCheckFrequency != -1:

				# ... state (during trip) ...
				agentState = agent.getState()
				if agentState == 1:

					# updates agent positioning and speed
					agent.updateAgentLane(controller.getAgentLane(agentId))
					agent.updateAgentSpeed(controller.getAgentSpeed(agentId))
					#print " ::::::::",controller.getAgentPositionLane(agentId)
					#print " ::::::::", controller.getAgent_lengthLane(controller.getAgentLane(agentId))
					agent.updateAgentPosition(controller.getAgentPosition(agentId))
                                        
                                        #print "%-7s %-5s %-7s %.2f %-5s %-7s"% ("AGENT:", agentId," speed: ",agent.getSpeed(),"position",agent.getLane())
                                        #print agentId + agent.getSpeed()      
                                        #print "Agent :"+agentId+ " speed :"+ agent.getSpeed()
					# ... and route check timing
					# if ((simulationStep - agent.getDepartureTime()) / routeCheckFrequency) * routeCheckFrequency > agent.getLastRouteCheck():

                                        #######FALTA ALTERAR ESTE METODO INCUIR A DISTANCIA K ESTA DO PONTO X PARA NAO SPAMAR ALTERACOES DE ROTAS
					#if random.random() < self.__checkRouteProbability(simulationStep, agent.getLastRouteCheck(), agent.getRouteCheckFrequency(), agent.getSpeed(), controller.getLaneMaxSpeed(agent.getLane())):
					if (controller.getAgent_lengthLane(controller.getAgentLane(agentId)) - controller.getAgentPositionLane(agentId) < 10) and (agent.getLastRouteCheck2()== -1) :
						# updates agent perception
						print "ENTRA!!!!! ->alterar rotas"
						agent.updateAgentPerception(controller.getNetworkEdgeWeights())
					
						# optimizes route
						routePlanning = agent.planRoute(agentId)
						if(routePlanning == 1):
							controller.setAgentRoute(agentId, agent.getRoute())

                                                agent.setLastRouteCheck2(1)
                                                
						# sets last route check
						if(routePlanning != -1):
							agent.setLastRouteCheck(simulationStep)
                                        

				# ... state (accident) ...
				elif agentState == 3:
					
					# updates stop time and state
					agent.stopStep()

				# ... state (during trip or accident)
				if agentState == 1 or agentState == 3:
					
						# resolves agent communications
						updatedPositions = self.__resolveCommunications(agentId, agent, simulationStep, updatedPositions, controller)


	# returns the check route probability considering an individual frequency coefficient and the time since the last check
	def __checkRouteProbability(self, simulationStep, agentLastRouteCheck, agentCheckFrequency, agentSpeed, laneMaxSpeed):
		
		# returns probability 1 in case there was no previous check
		if agentLastRouteCheck == -1:
			return 1
		else:
			timeSinceLastCheck = (simulationStep - agentLastRouteCheck)
		
		# check probability ... the time since the last route check
		if timeSinceLastCheck <= agentCheckFrequency/2:
			timeCheckProbability = (2 * math.pow(timeSinceLastCheck, 2)) / math.pow(agentCheckFrequency, 2)
		elif timeSinceLastCheck <= agentCheckFrequency:
			timeCheckProbability = (4 * agentCheckFrequency * timeSinceLastCheck - math.pow(agentCheckFrequency, 2) - 2 * math.pow(timeSinceLastCheck, 2)) / math.pow(agentCheckFrequency, 2)
		else:
			timeCheckProbability = 1
		
		'''
		if x <= max+min/2:
			return (2 * math.pow(min-x, 2)) / math.pow(min-max, 2)
		elif x <= max:
			return (-2 * max * min + 4 * max * x - math.pow(max, 2) + math.pow(min, 2) - 2 * math.pow(x, 2)) / math.pow(min-max, 2)
		else:
			return 1
		'''
		
		# check probability ... the current agent speed
		speedCheckProbability = math.pow(math.cos(math.pi/laneMaxSpeed*agentSpeed), 2)
		
		return (timeCheckProbability * speedCheckProbability)


	def __resolveCommunications(self, agentId, agent, simulationStep, updatedPositions, controller):

		treatedCommunication = 0
		
		# for each pending communication ...
		for i in range(agent.getNPendingCommunications()):

			j = i-treatedCommunication
			communication = agent.getPendingCommunication(j)
			
			# ... if it was not started this precise step ...
			if communication.getReceivedStep() != simulationStep:

				# ... updates agents positions if necessary ...
				if not updatedPositions:
					self.__updateAgentsPositions(controller)
					updatedPositions = True

				# ... and sends the communication to all other agents ...
				for receivingAgent in self.__agentList.itervalues():

					# ... who are also active and use cosmo ...
					if (receivingAgent.getState() == 1 or receivingAgent.getState() == 3) and receivingAgent.getRouteCheckFrequency() != -1:

						# ... and are less than BROADCAST_DISTANCE meters away
						distance = agent.distanceFrom(receivingAgent.getPosition())
						if distance > 0 and distance <= BROADCAST_DISTANCE:
							receivingAgent.receiveCommunication(communication, simulationStep)

				agent.treatedCommunication(j)
				treatedCommunication += 1
		
		return updatedPositions


	def __updateAgentsPositions(self, controller):
		
		for agentId, agent in self.__agentList.iteritems():
			agentState = agent.getState()
			if (agentState == 1 or agentState == 3) and agent.getRouteCheckFrequency() != -1:
				agent.updateAgentPosition(controller.getAgentPosition(agentId))


	# changes agent state and schedules accident communication for cosmo users
	def stop(self, agentId, lane, stopTime, simulationStep):

		self.__nextCommunicationId += self.__agentList[agentId].stopStart(lane, stopTime, simulationStep, self.__nextCommunicationId)
