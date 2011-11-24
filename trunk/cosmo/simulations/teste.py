s = '../simulations/lattice/lattice.net.xml'
print s[s.rfind('/')+1:s.find('.n')]

'''
currentLane = '16527312_1_0'
print currentLane[:currentLane.rfind('_')]
'''
'''
import math

def __checkRouteProbability(max, x):

    if x <= max/2:
        return (2 * math.pow(x, 2)) / math.pow(max, 2)
    elif x <= max:
        return (4 * max * x - math.pow(max, 2) - 2 * math.pow(x, 2)) / math.pow(max, 2)
    else:
        return 1
'''
'''
import numpy

edgeWeights = {'1': 0.5, '2': 1.2, '3': 2.8, '4': 3.4, '5': 5.9}

sum = numpy.sum(edgeWeights.values())
        
if sum != 0:
    print 'sum', sum
    print 'avg(sum/len)', (float(sum) / len(edgeWeights))
    print 'avg(numpy)', (numpy.average(edgeWeights.values()))
    print 'stdDev', (numpy.std(edgeWeights.values()))
'''
'''
try:            
    tree = ET.parse('../simulations/square/square.out.tripinfo.xml')
    
    # parses the tripinfo file for trip durations and route lengths
    durations = []
    routeLengths = []
    treepinfos = tree.getroot().findall('tripinfo')

    for treepinfo in treepinfos:
        durations.append(float(treepinfo.get('duration')))
        routeLengths.append(float(treepinfo.get('routeLength')))        
    
    print 'avgDuration', numpy.average(durations)
    print 'avgRouteLength', numpy.average(routeLengths)

except:
    print 'Can\'t parse the file square.out.tripinfo.xml. Please recheck the file\'s name and syntax'

'''

'''

tree = ET.parse('../square.simulation/square.net.xml')
# tree = ET.parse('../square2.simulation/square2.net.xml')

# parses the network normal edge distances
distances = {}
edges = tree.getroot().findall('edge')

for edge in edges:
    if edge.get('function') == 'normal':
        edge.find('lanes').find('lane')
        distances[edge.get('id')] = float(edge.find('lanes').find('lane').get('length'))

# parses the network edges to create 2 graphs of normal and internal edges
graph = {}
internalEdges = {}

junctions = tree.getroot().findall('junction')

for junction in junctions:
    junctionId = junction.get('id')
    
    # parses internal junctions
    if junctionId[0] == ':':
        
        juntion.get('incLanes')

succs = tree.getroot().findall('succ')

for succ in succs:
    edge = succ.get('edge')

    # parses the network normal edges
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
                    
                viaEdge = succlane.get('via')[:-2]
                internalEdges[viaEdge] = edge

    # parses the network internal edges
    else:
        # assuming there is no road with more than 10 lanes (2 digit index)
        try:
            internalEdges[edge] = (internalEdges[edge],succ.find('succlane').get('lane')[:-2])
        except:
            internalEdges[edge] = ('',succ.find('succlane').get('lane')[:-2])           

for i, j in sorted(internalEdges.iteritems()):
    print i, j
            
# parses the network normal edge distances
distances = {}
edges = tree.getroot().findall('edge')

for edge in edges:
    if edge[0] != ':':
        edge.find('lanes').find('lane')
        distances[edge.get('id')] = float(edge.find('lanes').find('lane').get('length'))

# parses the network succeeding edges
graph = {}
succs = tree.getroot().findall('succ')

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

r = ''              
for key in graph:
    r += '{\'' + str(key) + '\': {'
    subGraph = graph.get(key)
    for subKey in subGraph:
        r += '\'' + str(subKey) + '\': %.2f, ' % subGraph.get(subKey)
    r = r[:-2] + '}\n'
r = r[:-1]
print r
'''