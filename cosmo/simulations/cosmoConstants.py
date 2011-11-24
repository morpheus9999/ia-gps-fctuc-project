# -------------------- #
# Controller --------- #
# -------------------- #

# Usual agents color (yellow)
USUAL_AGENT_COLOR = (255,255,0,255)

# Temporarily stopped agents color (red)
STOPPED_AGENT_COLOR = (255,0,0,255)

# Color for agents that changed the initial route (green)
CHANGED_ROUTE_AGENT_COLOR = (0,255,0,255)

# Accident probability each step (e.g. 0.001)
ACCIDENT_PROBABILITY = 0

# Time agents will be stopped after an accident
ACCIDENT_STOP_TIME = 300

# Simulation use of the graphical interface
GRAPHICAL_INTERFACE = False

# -------------------- #
# Population --------- #
# -------------------- #

# Percentage of agents that use cosmos (e.g. 0.5)
COSMO_USE_PERCENT = 1

# Variation of agents route check frequency (random.random(), random.uniform(a, b), random.triangular(low, high, mode), random.betavariate(alpha, beta), random.expovariate(lambd), random.gammavariate(alpha, beta), random.gauss(mu, sigma), random.lognormvariate(mu, sigma), random.normalvariate(mu, sigma), random.vonmisesvariate(mu, kappa), random.paretovariate(alpha), random.weibullvariate(alpha, beta))
# ROUTE_CHECK_FREQUENCY_VARIATION = 'max(int(random.gauss(300,75)),60)'
ROUTE_CHECK_FREQUENCY_VARIATION = 'max(int(random.gauss(3600,600)),1800)'

# Maximum broadcast communication distance between agents in meters
BROADCAST_DISTANCE = 100

# -------------------- #
# Agent -------------- #
# -------------------- #

# Probability of an agent accepting a newly computed route
ACCEPT_NEW_ROUTE_PROB = 1

# Algorithm used for traffic flow optimization
ROUTING_ALGORITHM = 2

# -------------------- #
# Network ------------ #
# -------------------- #

# Occupancy limit for the occupied road blocker algorithm
OCCUPANCY_LIMIT = 0.25

# Percentage of the variation of the communicated weights in the error insertion algorithm
WEIGHT_VARIATION = 0.5