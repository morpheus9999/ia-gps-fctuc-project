"""
@file    traciconstants.py

This script contains TraCI constant definitions from <SUMO>/src/traci-server/TraCIConstants.h
generated by "rebuildConstants.py" on 2010-11-05 16:15:53.758000.

Copyright (C) 2009 DLR/TS, Germany
All rights reserved
"""



# ****************************************
# COMMANDS
# ****************************************
# command: get version
CMD_GETVERSION = 0x00

# command: simulation step
CMD_SIMSTEP = 0x01

# command: simulation step (new version)
CMD_SIMSTEP2 = 0x02

# command: set maximum speed
CMD_SETMAXSPEED = 0x11

# command: stop node
CMD_STOP = 0x12

# command: set lane
CMD_CHANGELANE = 0x13

# command: slow down
CMD_SLOWDOWN = 0x14

# command: change route
CMD_CHANGEROUTE = 0x30

# command: change target
CMD_CHANGETARGET = 0x31

# command: subscribe lifecycles
CMD_SUBSCRIBELIFECYCLES = 0x61

# command: unsubscribe lifecycles
CMD_UNSUBSCRIBELIFECYCLES = 0x62

# command: object creation
CMD_OBJECTCREATION = 0x63

# command: object destruction
CMD_OBJECTDESTRUCTION = 0x64

# command: object domain subscription
CMD_SUBSCRIBEDOMAIN = 0x65

# command: object domain unsubscription
CMD_UNSUBSCRIBEDOMAIN = 0x66

# command: object update
CMD_UPDATEOBJECT = 0x67

# command: Simulation Parameter
CMD_SIMPARAMETER = 0x70

# command: Position Conversion
CMD_POSITIONCONVERSION = 0x71

# command: Distance Request
CMD_DISTANCEREQUEST = 0x72

# command: Scenario
CMD_SCENARIO = 0x73

# command: add vehicle
CMD_ADDVEHICLE = 0x74

# command: move node
CMD_MOVENODE = 0x80

# command: close sumo
CMD_CLOSE = 0x7F

# command:
CMD_UPDATECALIBRATOR = 0x50

# command: get all traffic light ids
CMD_GETALLTLIDS = 0x40

# command: get traffic light status
CMD_GETTLSTATUS = 0x41

# command: report traffic light id
CMD_TLIDLIST = 0x90

# command: report traffic light status switch
CMD_TLSWITCH = 0x91

# command: get induction loop (e1) variable
CMD_GET_INDUCTIONLOOP_VARIABLE = 0xa0
# response: get induction loop (e1) variable
RESPONSE_GET_INDUCTIONLOOP_VARIABLE = 0xb0
# command: subscribe induction loop (e1) variable
CMD_SUBSCRIBE_INDUCTIONLOOP_VARIABLE = 0xd0
# response: subscribe induction loop (e1) variable
RESPONSE_SUBSCRIBE_INDUCTIONLOOP_VARIABLE = 0xe0

# command: get multi-entry/multi-exit detector (e3) variable
CMD_GET_MULTI_ENTRY_EXIT_DETECTOR_VARIABLE = 0xa1
# response: get areal detector (e3) variable
RESPONSE_GET_MULTI_ENTRY_EXIT_DETECTOR_VARIABLE = 0xb1
# command: subscribe multi-entry/multi-exit detector (e3) variable
CMD_SUBSCRIBE_MULTI_ENTRY_EXIT_DETECTOR_VARIABLE = 0xd1
# response: subscribe areal detector (e3) variable
RESPONSE_SUBSCRIBE_MULTI_ENTRY_EXIT_DETECTOR_VARIABLE = 0xe1

# command: get traffic lights variable
CMD_GET_TL_VARIABLE = 0xa2
# response: get traffic lights variable
RESPONSE_GET_TL_VARIABLE = 0xb2
# command: set traffic lights variable
CMD_SET_TL_VARIABLE = 0xc2
# command: subscribe traffic lights variable
CMD_SUBSCRIBE_TL_VARIABLE = 0xd2
# response: subscribe traffic lights variable
RESPONSE_SUBSCRIBE_TL_VARIABLE = 0xe2

# command: get lane variable
CMD_GET_LANE_VARIABLE = 0xa3
# response: get lane variable
RESPONSE_GET_LANE_VARIABLE = 0xb3
# command: set lane variable
CMD_SET_LANE_VARIABLE = 0xc3
# command: subscribe lane variable
CMD_SUBSCRIBE_LANE_VARIABLE = 0xd3
# response: subscribe lane variable
RESPONSE_SUBSCRIBE_LANE_VARIABLE = 0xe3

# command: get vehicle variable
CMD_GET_VEHICLE_VARIABLE = 0xa4
# response: get vehicle variable
RESPONSE_GET_VEHICLE_VARIABLE = 0xb4
# command: set vehicle variable
CMD_SET_VEHICLE_VARIABLE = 0xc4
# command: subscribe vehicle variable
CMD_SUBSCRIBE_VEHICLE_VARIABLE = 0xd4
# response: subscribe vehicle variable
RESPONSE_SUBSCRIBE_VEHICLE_VARIABLE = 0xe4

# command: get vehicle type variable
CMD_GET_VEHICLETYPE_VARIABLE = 0xa5
# response: get vehicle type variable
RESPONSE_GET_VEHICLETYPE_VARIABLE = 0xb5
# command: set vehicle type variable
CMD_SET_VEHICLETYPE_VARIABLE = 0xc5
# command: subscribe vehicle type variable
CMD_SUBSCRIBE_VEHICLETYPE_VARIABLE = 0xd5
# response: subscribe vehicle type variable
RESPONSE_SUBSCRIBE_VEHICLETYPE_VARIABLE = 0xe5

# command: get route variable
CMD_GET_ROUTE_VARIABLE = 0xa6
# response: get route variable
RESPONSE_GET_ROUTE_VARIABLE = 0xb6
# command: set route variable
CMD_SET_ROUTE_VARIABLE = 0xc6
# command: subscribe route variable
CMD_SUBSCRIBE_ROUTE_VARIABLE = 0xd6
# response: subscribe route variable
RESPONSE_SUBSCRIBE_ROUTE_VARIABLE = 0xe6

# command: get poi variable
CMD_GET_POI_VARIABLE = 0xa7
# response: get poi variable
RESPONSE_GET_POI_VARIABLE = 0xb7
# command: set poi variable
CMD_SET_POI_VARIABLE = 0xc7
# command: subscribe poi variable
CMD_SUBSCRIBE_POI_VARIABLE = 0xd7
# response: subscribe poi variable
RESPONSE_SUBSCRIBE_POI_VARIABLE = 0xe7

# command: get polygon variable
CMD_GET_POLYGON_VARIABLE = 0xa8
# response: get polygon variable
RESPONSE_GET_POLYGON_VARIABLE = 0xb8
# command: set polygon variable
CMD_SET_POLYGON_VARIABLE = 0xc8
# command: subscribe polygon variable
CMD_SUBSCRIBE_POLYGON_VARIABLE = 0xd8
# response: subscribe polygon variable
RESPONSE_SUBSCRIBE_POLYGON_VARIABLE = 0xe8

# command: get junction variable
CMD_GET_JUNCTION_VARIABLE = 0xa9
# response: get junction variable
RESPONSE_GET_JUNCTION_VARIABLE = 0xb9
# command: set junction variable
CMD_SET_JUNCTION_VARIABLE = 0xc9
# command: subscribe junction variable
CMD_SUBSCRIBE_JUNCTION_VARIABLE = 0xd9
# response: subscribe junction variable
RESPONSE_SUBSCRIBE_JUNCTION_VARIABLE = 0xe9

# command: get edge variable
CMD_GET_EDGE_VARIABLE = 0xaa
# response: get edge variable
RESPONSE_GET_EDGE_VARIABLE = 0xba
# command: set edge variable
CMD_SET_EDGE_VARIABLE = 0xca
# command: subscribe edge variable
CMD_SUBSCRIBE_EDGE_VARIABLE = 0xda
# response: subscribe edge variable
RESPONSE_SUBSCRIBE_EDGE_VARIABLE = 0xea

# command: get simulation variable
CMD_GET_SIM_VARIABLE = 0xab
# response: get simulation variable
RESPONSE_GET_SIM_VARIABLE = 0xbb
# command: set simulation variable
CMD_SET_SIM_VARIABLE = 0xcb
# command: subscribe simulation variable
CMD_SUBSCRIBE_SIM_VARIABLE = 0xdb
# response: subscribe simulation variable
RESPONSE_SUBSCRIBE_SIM_VARIABLE = 0xeb

# command: get GUI variable
CMD_GET_GUI_VARIABLE = 0xac
# response: get GUI variable
RESPONSE_GET_GUI_VARIABLE = 0xbc
# command: set GUI variable
CMD_SET_GUI_VARIABLE = 0xcc
# command: subscribe GUI variable
CMD_SUBSCRIBE_GUI_VARIABLE = 0xdc
# response: subscribe GUI variable
RESPONSE_SUBSCRIBE_GUI_VARIABLE = 0xec



# ****************************************
# POSITION REPRESENTATIONS
# ****************************************
# Omit position
POSITION_NONE = 0x00
# 2D cartesian coordinates
POSITION_2D = 0x01
# 2.5D cartesian coordinates
POSITION_2_5D = 0x02
# 3D cartesian coordinates
POSITION_3D = 0x03
# Position on road map
POSITION_ROADMAP = 0x04



# ****************************************
# DATA TYPES
# ****************************************
# Boundary Box
TYPE_BOUNDINGBOX = 0x05
# Polygon
TYPE_POLYGON = 0x06
# unsigned byte
TYPE_UBYTE = 0x07
# signed byte
TYPE_BYTE = 0x08
# 32 bit integer
TYPE_INTEGER = 0x09
# float
TYPE_FLOAT = 0x0A
# double
TYPE_DOUBLE = 0x0B
# 8 bit ASCII string
TYPE_STRING = 0x0C
# list of traffic light phases
TYPE_TLPHASELIST = 0x0D
# list of strings
TYPE_STRINGLIST = 0x0E
# compound object
TYPE_COMPOUND = 0x0F
# color (four ubytes)
TYPE_COLOR = 0x11



# ****************************************
# RESULT TYPES
# ****************************************
# result type: Ok
RTYPE_OK = 0x00
# result type: not implemented
RTYPE_NOTIMPLEMENTED = 0x01
# result type: error
RTYPE_ERR = 0xFF



# ****************************************
# DOMAIN IDs (FOR SCENARIO COMMAND)
# ****************************************
# road map domain
DOM_ROADMAP = 0x00
# vehicle domain
DOM_VEHICLE = 0x01
# traffic lights domain
DOM_TRAFFICLIGHTS = 0x02
# points of interest domain
DOM_POI = 0x03
# polygon domain
DOM_POLYGON = 0x04



# ****************************************
# VARIABLE IDs (FOR SCENARIO COMMAND)
# ****************************************
# count of domain objects
DOMVAR_COUNT = 0x01
# position of a domain object
DOMVAR_POSITION = 0x02
# boundaries of simulation net
DOMVAR_BOUNDINGBOX = 0x03
# speed of a node
DOMVAR_SPEED = 0x04
# actual phase of a traffic light
DOMVAR_CURTLPHASE = 0x05
# next phase of a traffic light
DOMVAR_NEXTTLPHASE = 0x06
# type of a domain object (poi, polygon)
DOMVAR_TYPE = 0x07
# layer a domain object is located at (poi, polygon)
DOMVAR_LAYER = 0x08
# shape of a polygon
DOMVAR_SHAPE = 0x09
# max count of vehicles
DOMVAR_MAXCOUNT = 0x0A
# count of TraCI vehicles
DOMVAR_EQUIPPEDCOUNT = 0x0B
# max count of TraCI vehicles
DOMVAR_EQUIPPEDCOUNTMAX = 0x0C
# id string of a domain object
DOMVAR_NAME = 0x0D
# route, a car plans to drive
DOMVAR_ROUTE = 0x0E
# maximum allowed speed of a node
DOMVAR_ALLOWED_SPEED = 0x0F
# air distance from a certain object to a position
DOMVAR_AIRDISTANCE = 0x10
# driving distance from a certain object to a position
DOMVAR_DRIVINGDISTANCE = 0x11
# external integer id of a certain object
DOMVAR_EXTID = 0x12
# angle of a certain object, in degrees [0..360)
DOMVAR_ANGLE = 0x13
# current simulation time
DOMVAR_SIMTIME = 0x14
# current CO2 emission of a node
DOMVAR_CO2EMISSION = 0x20
# current CO emission of a node
DOMVAR_COEMISSION = 0x21
# current HC emission of a node
DOMVAR_HCEMISSION = 0x22
# current PMx emission of a node
DOMVAR_PMXEMISSION = 0x23
# current NOx emission of a node
DOMVAR_NOXEMISSION = 0x24
# current fuel consumption of a node
DOMVAR_FUELCONSUMPTION = 0x25
# current noise emission of a node
DOMVAR_NOISEEMISSION = 0x26



# ****************************************
# TRAFFIC LIGHT PHASES
# ****************************************
# red phase
TLPHASE_RED = 0x01
# yellow phase
TLPHASE_YELLOW = 0x02
# green phase
TLPHASE_GREEN = 0x03
# tl is blinking
TLPHASE_BLINKING = 0x04
# tl is off and not blinking
TLPHASE_NOSIGNAL = 0x05



# ****************************************
# DIFFERENT DISTANCE REQUESTS
# ****************************************
# air distance
REQUEST_AIRDIST = 0x00
# driving distance
REQUEST_DRIVINGDIST = 0x01



# ****************************************
# VARIABLE TYPES (for CMD_GET_*_VARIABLE)
# ****************************************
# list of instances' ids (get: induction loops, areal detector, traffic lights)
ID_LIST = 0x00

# last step vehicle number (get: induction loops, multi-entry/multi-exit detector, lanes, edges)
LAST_STEP_VEHICLE_NUMBER = 0x10

# last step vehicle number (get: induction loops, multi-entry/multi-exit detector, lanes, edges)
LAST_STEP_MEAN_SPEED = 0x11

# last step vehicle number (get: induction loops, multi-entry/multi-exit detector, lanes, edges)
LAST_STEP_VEHICLE_ID_LIST = 0x12

# last step occupancy (get: induction loops, lanes, edges)
LAST_STEP_OCCUPANCY = 0x13

# last step vehicle halting number (get: multi-entry/multi-exit detector, lanes, edges)
LAST_STEP_VEHICLE_HALTING_NUMBER = 0x14

# last step mean vehicle length (get: induction loops, lanes, edges)
LAST_STEP_LENGTH = 0x15

# last step time since last detection (get: induction loops)
LAST_STEP_TIME_SINCE_DETECTION = 0x16


# traffic light states, encoded as rRgGyYoO tuple (get: traffic lights)
TL_RED_YELLOW_GREEN_STATE = 0x20

# traffic light states, encoded phase, brake, and yellow tuple (get: traffic lights, set: traffic lights)
TL_PHASE_BRAKE_YELLOW_STATE = 0x21

# index of the phase (set: traffic lights)
TL_PHASE_INDEX = 0x22

# traffic light program (set: traffic lights)
TL_PROGRAM = 0x23

# phase duration (set: traffic lights)
TL_PHASE_DURATION = 0x24

# complete definition (get: traffic lights)
TL_COMPLETE_DEFINITION_PBY = 0x25

# controlled lanes (get: traffic lights)
TL_CONTROLLED_LANES = 0x26

# controlled links (get: traffic lights)
TL_CONTROLLED_LINKS = 0x27

# index of the current phase (get: traffic lights)
TL_CURRENT_PHASE = 0x28

# name of the current program (get: traffic lights)
TL_CURRENT_PROGRAM = 0x29

# controlled junctions (get: traffic lights)
TL_CONTROLLED_JUNCTIONS = 0x2a

# complete definition (get: traffic lights)
TL_COMPLETE_DEFINITION_RYG = 0x2b

# complete program (set: traffic lights)
TL_COMPLETE_PROGRAM_RYG = 0x2c

# assumed time to next switch (get: traffic lights)
TL_NEXT_SWITCH = 0x2d



# outgoing link number (get: lanes)
LANE_LINK_NUMBER = 0x30

# id of parent edge (get: lanes)
LANE_EDGE_ID = 0x31

# outgoing link definitions (get: lanes)
LANE_LINKS = 0x33

# list of allowed vehicle classes (get&set: lanes)
LANE_ALLOWED = 0x34

# list of not allowed vehicle classes (get&set: lanes)
LANE_DISALLOWED = 0x35


# speed (get: vehicle)
VAR_SPEED = 0x40

# speed without TraCI influence (get: vehicle)
VAR_SPEED_WITHOUT_TRACI = 0x41

# maximum allowed/possible speed (get: vehicle types, lanes, set: edges, lanes)
VAR_MAXSPEED = 0x41

# position (2D) (get: vehicle, poi, set: poi)
VAR_POSITION = 0x42

# angle (get: vehicle)
VAR_ANGLE = 0x43

# angle (get: vehicle types, lanes, set: lanes)
VAR_LENGTH = 0x44

# color (get: vehicles, vehicle types, polygons, pois)
VAR_COLOR = 0x45

# max. acceleration (get: vehicle types)
VAR_ACCEL = 0x46

# max. deceleration (get: vehicle types)
VAR_DECEL = 0x47

# driver reaction time (get: vehicle types)
VAR_TAU = 0x48

# vehicle class (get: vehicle types)
VAR_VEHICLECLASS = 0x49

# emission class (get: vehicle types)
VAR_EMISSIONCLASS = 0x4a

# shape class (get: vehicle types)
VAR_SHAPECLASS = 0x4b

# offset (brake gap) (get: vehicle types)
VAR_GUIOFFSET = 0x4c

# width (get: vehicle types)
VAR_WIDTH = 0x4d

# shape (get: polygons)
VAR_SHAPE = 0x4e

# type id (get: vehicles, polygons, pois)
VAR_TYPE = 0x4f

# road id (get: vehicles)
VAR_ROAD_ID = 0x50

# lane id (get: vehicles)
VAR_LANE_ID = 0x51

# lane index (get: vehicles)
VAR_LANE_INDEX = 0x52

# route id (get & set: vehicles)
VAR_ROUTE_ID = 0x53

# edges (get: routes)
VAR_EDGES = 0x54

# filled? (get: polygons)
VAR_FILL = 0x55

# position (1D along lane) (get: vehicle)
VAR_LANEPOSITION = 0x56

# route (set: vehicles)
VAR_ROUTE = 0x57

# travel time information (get&set: vehicle)
VAR_EDGE_TRAVELTIME = 0x58

# effort information (get&set: vehicle)
VAR_EDGE_EFFORT = 0x59

# last step travel time (get: edge, lane)
VAR_CURRENT_TRAVELTIME = 0x5a

# signals state (get/set: vehicle)
VAR_SIGNALS = 0x5b

# new lane/position along (set: vehicle)
VAR_MOVE_TO = 0x5c

# driver imperfection (set: vehicle)
VAR_IMPERFECTION = 0x5d

# speed factor (set: vehicle)
VAR_SPEED_FACTOR = 0x5e

# speed deviation (set: vehicle)
VAR_SPEED_DEVIATION = 0x5f

# speed without TraCI influence (get: vehicle)
VAR_SPEED_WITHOUT_TRACI = 0xb1

# best lanes (get: vehicle)
VAR_BEST_LANES = 0xb2




# current CO2 emission of a node (get: vehicle, lane, edge)
VAR_CO2EMISSION = 0x60

# current CO emission of a node (get: vehicle, lane, edge)
VAR_COEMISSION = 0x61

# current HC emission of a node (get: vehicle, lane, edge)
VAR_HCEMISSION = 0x62

# current PMx emission of a node (get: vehicle, lane, edge)
VAR_PMXEMISSION = 0x63

# current NOx emission of a node (get: vehicle, lane, edge)
VAR_NOXEMISSION = 0x64

# current fuel consumption of a node (get: vehicle, lane, edge)
VAR_FUELCONSUMPTION = 0x65

# current noise emission of a node (get: vehicle, lane, edge)
VAR_NOISEEMISSION = 0x66



# current time step (get: simulation)
VAR_TIME_STEP = 0x70

# number of loaded vehicles (get: simulation)
VAR_LOADED_VEHICLES_NUMBER = 0x71

# loaded vehicle ids (get: simulation)
VAR_LOADED_VEHICLES_IDS = 0x72

# number of departed vehicle (get: simulation)
VAR_DEPARTED_VEHICLES_NUMBER = 0x73

# departed vehicle ids (get: simulation)
VAR_DEPARTED_VEHICLES_IDS = 0x74

# number of vehicles starting to teleport (get: simulation)
VAR_TELEPORT_STARTING_VEHICLES_NUMBER = 0x75

# ids of vehicles starting to teleport (get: simulation)
VAR_TELEPORT_STARTING_VEHICLES_IDS = 0x76

# number of vehicles ending to teleport (get: simulation)
VAR_TELEPORT_ENDING_VEHICLES_NUMBER = 0x77

# ids of vehicles ending to teleport (get: simulation)
VAR_TELEPORT_ENDING_VEHICLES_IDS = 0x78

# number of arrived vehicles (get: simulation)
VAR_ARRIVED_VEHICLES_NUMBER = 0x79

# ids of arrived vehicles (get: simulation)
VAR_ARRIVED_VEHICLES_IDS = 0x7a

# delta t (get: simulation)
VAR_DELTA_T = 0x7b

# bounding box (get: simulation)
VAR_NET_BOUNDING_BOX = 0x7c








# add an instance (poi, polygon)
ADD = 0x80

# remove an instance (poi, polygon)
REMOVE = 0x81


# force rerouting based on travel time (vehicles)
CMD_REROUTE_TRAVELTIME = 0x90

# force rerouting based on effort (vehicles)
CMD_REROUTE_EFFORT = 0x91

# validates current route (vehicles)
VAR_ROUTE_VALID = 0x92



# zoom
VAR_VIEW_ZOOM = 0xa0
# view position
VAR_VIEW_OFFSET = 0xa1
# view schema
VAR_VIEW_SCHEMA = 0xa2
# view by boundary
VAR_VIEW_BOUNDARY = 0xa3
# background color
VAR_VIEW_BACKGROUNDCOLOR = 0xa4
# screenshot
VAR_SCREENSHOT = 0xa5
# track vehicle
VAR_TRACK_VEHICLE = 0xa6
# network size (get: )
VAR_NET_SIZE = 0xa7




