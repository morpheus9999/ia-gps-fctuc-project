import numpy, os, random, subprocess, sys, xml.etree.ElementTree as ET
from cosmoConstants import USUAL_AGENT_COLOR, STOPPED_AGENT_COLOR, CHANGED_ROUTE_AGENT_COLOR, ACCIDENT_PROBABILITY, ACCIDENT_STOP_TIME, GRAPHICAL_INTERFACE
from cosmoNetwork import Network
from cosmoPopulation import Population
sys.path.append(os.path.join('..', '..', 'sumo-0.12.2', 'tools', 'traci'))
from traciControl import initTraCI, cmdSimulationStep, cmdGetSimulationVariable_arrivedIDList, cmdGetSimulationVariable_departedIDList, cmdGetVehicleVariable_idList, cmdGetVehicleVariable_laneID, cmdGetVehicleVariable_position, cmdGetVehicleVariable_speed, cmdChangeVehicleVariable_speed, cmdChangeVehicleVariable_color, cmdChangeVehicleVariable_changeRoute,  cmdGetLaneVariable_speed, cmdClose , cmdGetEdgeVariable_idList, cmdGetEdgeVariable_occupancy, cmdGetEdgeVariable_meanSpeed,cmdGetEdgeVariable_speed, cmdGetVehicleVariable_lanePosition,cmdGetEdgeVariable_LENGTH,cmdGetLaneVariable_length


class Controller:

	def __init__(self):
                print "ESTA AKI!!!!!!!!!!!!!!!!!!!!!!"
		# checks if exactly 1 argument was given (simulationConfigFile)
		nArgs = len(sys.argv)
		if nArgs < 2:
			sys.exit('Missing arguments: python cosmoController.py simulationConfigFile')
		elif nArgs > 2:
			sys.exit('Too many arguments: python cosmoController.py simulationConfigFile')
		else:
			# parses the simulation configuration file
			self.__networkFile, self.__routesFile, self.__port, self.__tripinfoFile, self.__simulationFirstStep, self.__simulationFinalStep = self.__parseSimulation(sys.argv[1])
		
		# calls for the parsing of the network file
		self.__network = Network(self.__networkFile)
		if self.__network.getGraph() == None:
			sys.exit('Can\'t parse the file ' + self.__networkFile + '. Please recheck the file\'s name and syntax')
                print "ESTA AKI!!!!!!!!!!!!!!!!!!!!!!"
		# sets the last network update to never
		# self.__lastNetworkUpdate = -1


	def __parseSimulation(self, configFile):

		# parses the configuration file for ...
		try:
			configDirectory = configFile[:configFile.rfind('/')+1]
			
			tree = ET.parse(configFile).getroot()
			inputSubTree = tree.find('input')
            
			# ... name of the network file ...
			netFile = configDirectory + inputSubTree.find('net-file').get('value')
			# ... name of the route file ...
			routesFile = configDirectory + inputSubTree.find('route-files').get('value')
			# ... traci port number ...
			remotePort = int(tree.find('traci_server').find('remote-port').get('value'))

			# ... name of the tripinfo file
			outputSubTree = tree.find('output')
			tripinfoFile = configDirectory + outputSubTree.find('tripinfo').get('value')

			# ... 1st and final steps of the simulation
			begin = end = None
			timeSubTree = tree.find('time')

			if timeSubTree != None:
				begin = timeSubTree.find('begin')
				end = timeSubTree.find('end')

			if begin == None:
				begin = 0
			else:
				begin = int(begin.get('value'))
				
			if end == None:
				end = 3600
			else:
				end = int(end.get('value'))

			return netFile, routesFile, remotePort, tripinfoFile, begin, end
		
		except:
			sys.exit('Can\'t parse the file ' + configFile + '. Please recheck the file\'s name and syntax')


	def runSimulation(self):
		print "ESTA AKI!!!!!!!!!!!!!!!!!!!!!!"
		f = open('output.txt', 'a')
		f.write('Network = ' + sys.argv[1] + '\nnumpy.average(durations) numpy.average(routeLengths) avgOccupancyAvgs avgDevOccupancyStdDevs)\n')

		# create set of plans
		# os.system('python ../simulations/randomTrips2.py -n ' + self.__networkFile + ' -o trips.xml -r ' + self.__routesFile + ' -e ' + sys.argv[2] + ' -p ' + sys.argv[3] + ' -B ' + sys.argv[4])
                print "ESTA AKI2!!!!!!!!!!!!!!!!!!!!!!"
		# calls for the parsing of the network file
		self.__population = Population(self.__routesFile, self.__network)
		if not self.__population.isValid():
			sys.exit('Can\'t parse the file ' + self.__routesFile + '. Please recheck the file\'s name and syntax')
		GRAPHICAL_INTERFACE =1
		# starts sumo and opens communication with traci (-N para iniciar o sumo-gui em pausa)
		if(GRAPHICAL_INTERFACE):
			subprocess.Popen('%s -c %s -N' % (os.path.join('..', '..', 'sumo-0.12.2', 'bin', 'sumo-gui'), sys.argv[1]), shell=True, stdout=sys.stdout)
		else:
			subprocess.Popen('%s -c %s' % (os.path.join('..', '..', 'sumo-0.12.2', 'bin', 'sumo'), sys.argv[1]), shell=True, stdout=sys.stdout)
		initTraCI(self.__port)
		
		activeAgents = []
		stoppedAgents = []
		
		# runs until simulation time is over and there is no more active agents
		simulationStep = self.__simulationFirstStep
		while not (simulationStep >= self.__simulationFinalStep and activeAgents == []):
			
			# advances 1s in the simulation and checks for active agents
			simulationStep += 1
			activeAgents = cmdSimulationStep(1000)
			if len(activeAgents) == 0:
				continue
			
			# updates status of stopped agents
			self.__accidentTimer(stoppedAgents)
			
			# updates the network weights and statistics and checks agent decisions, providing departed and arrived agents for the simulated step 
			self.__updateEdgeWeights()
			#print self.__network
			self.__network.updateOccupancyStats()
			self.__population.agentActions(simulationStep, cmdGetSimulationVariable_departedIDList(), cmdGetSimulationVariable_arrivedIDList(), self)
			
			# simulates accidents
			if random.random() < ACCIDENT_PROBABILITY:
				self.__simulateAccident(stoppedAgents,simulationStep)

		# closes the communication with traci
		cmdClose()
		
		# adds simulation results to output file and decreases number of scheduled simulations
		self.__printSimulationOutput(f)


	# updates network edge weights
	def __updateEdgeWeights(self):
                P1=0
                P2=0
                P3=0
                
		edgeIdList = cmdGetEdgeVariable_idList()
		edgeWeights = {}
		
		for edgeId in edgeIdList:
			if edgeId[0] != ':':
                                #print edgeId
				#edgeWeights[edgeId] = cmdGetEdgeVariable_occupancy(edgeId)
                                meanSpeed= cmdGetEdgeVariable_meanSpeed(edgeId)
                                #print "MEANSPEED"                                       
                                #print meanSpeed
                                
                                if(meanSpeed==0):
                                      P1=0.0
                                      P2=1.0
                                else:
                                        P1=0.9
                                        P2=0.1
                                #print "maxspeed"       
                                maxspeed= cmdGetLaneVariable_speed(edgeId+"_0")       
                                                                       
                                #print maxspeed
                                #falta o valor minimo
				edgeWeights[edgeId] = 	(P1*meanSpeed+P2*maxspeed)#cmdGetEdgeVariable_LENGTH(edgeId)
				
		self.__network.setEdgeWeights(edgeWeights)


	# stops an agent to simulate an accident
	def __simulateAccident(self, stoppedAgents, simulationStep):
		print 'UI'
		agentIdList = cmdGetVehicleVariable_idList()
		agentId = agentIdList[random.randint(0,len(agentIdList)-1)]
		alreadyStopped = False

		for stoppedAgent in stoppedAgents:
			if agentId == stoppedAgent[0]:
				alreadyStopped = True
				break

		if not alreadyStopped:
			
			cmdChangeVehicleVariable_speed(agentId, 0)
			cmdChangeVehicleVariable_color(agentId, STOPPED_AGENT_COLOR)

			stoppedAgents.append((agentId, ACCIDENT_STOP_TIME))

			currentLane = cmdGetVehicleVariable_laneID(agentId)
			self.__population.stop(agentId, currentLane, ACCIDENT_STOP_TIME, simulationStep)


	# counts time for stopped agents and restarts them when stop time is over
	def __accidentTimer(self, stoppedAgents):
		
		restarted = 0
		for i in range(len(stoppedAgents)):
			j = i - restarted
			if stoppedAgents[j][1] <= 0:
				# -1 for default speed (car-following rules)
				cmdChangeVehicleVariable_speed(stoppedAgents[j][0], -1)
				cmdChangeVehicleVariable_color(stoppedAgents[j][0], USUAL_AGENT_COLOR)
				stoppedAgents.pop(j)
				restarted += 1
			else:
				stoppedAgents[j] = (stoppedAgents[j][0], stoppedAgents[j][1]-1)


	# prints simulation results into specified file
	def __printSimulationOutput(self, f):

		parseBool = False
		
		while parseBool == False:

			try:
				tree = ET.parse(self.__tripinfoFile)
				
				print 
				
				# parses the tripinfo file for trip durations and route lengths
				durations = []
				routeLengths = []
				treepinfos = tree.getroot().findall('tripinfo')
				
				for treepinfo in treepinfos:
					durations.append(float(treepinfo.get('duration')))
					routeLengths.append(float(treepinfo.get('routeLength')))
				
				parseBool = True
	
			except:
				# print 'Can\'t parse the file ' + self.__tripinfoFile + '. Please recheck the file\'s name and syntax'
				pass

		avgOccupancyAvgs, avgDevOccupancyStdDevs = self.__network.returnOccupancyStats()
		
		# f.write(str(n) + '. ')
		f.write(str(numpy.average(durations)) + ' ' + str(numpy.average(routeLengths)) + ' ' + str(avgOccupancyAvgs) + ' ' + str(avgDevOccupancyStdDevs) + '\n')


	# uses traci to access agent current lane
	def getAgentLane(self, agentId):

		laneId = cmdGetVehicleVariable_laneID(agentId)
		return laneId


	# uses traci to access agent position
	def getAgentPosition(self, agentId):

		position = cmdGetVehicleVariable_position(agentId)
		return position


        # uses traci to access agent link number
	def getAgentPositionLane(self, agentId):

		position = cmdGetVehicleVariable_lanePosition(agentId)
		return position

        # uses traci to access agent link number
	def getAgent_lengthLane(self, laneId):

		length = cmdGetLaneVariable_length(laneId)
		return length        
	# uses traci to access agent current speed
	def getAgentSpeed(self, agentId):

		speed = cmdGetVehicleVariable_speed(agentId)
		return speed
	
	
	# uses traci to access lane max speed
	def getLaneMaxSpeed(self, laneId):

		speed = cmdGetLaneVariable_speed(laneId)
		return speed


	'''
	# returns up to date network edge weights
	def getNetworkEdgeWeights(self):

		if self.__lastNetworkUpdate != self.__simulationStep:
			edgeIdList = cmdGetEdgeVariable_idList()
			edgeWeights = {}
			for edgeId in edgeIdList:
				if edgeId[0] != ':':
					edgeWeights[edgeId] = cmdGetEdgeVariable_occupancy(edgeId)
			self.__network.setEdgeWeights(edgeWeights)
			self.__lastNetworkUpdate = self.__simulationStep
		else:
			edgeWeights = self.__network.getEdgeWeights()

		return edgeWeights
	'''
	

	# returns network edge weights
	def getNetworkEdgeWeights(self):

		return self.__network.getEdgeWeights()


	# uses traci to change agent's route
	def setAgentRoute(self, agentId, newRoute):
                print "%-7s %-5s"% ("AGENT:", agentId)
		cmdChangeVehicleVariable_changeRoute(agentId, newRoute)
		cmdChangeVehicleVariable_color(agentId, CHANGED_ROUTE_AGENT_COLOR)
		print "acabou"


# initializes and starts the simulation
controller = Controller()
controller.runSimulation()
