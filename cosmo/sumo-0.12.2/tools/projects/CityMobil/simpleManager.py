#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file    simpleManager.py
@author  Michael.Behrisch@dlr.de
@date    2008-10-09
@version $Id: simpleManager.py 9175 2010-10-03 19:47:36Z behrisch $

Control the CityMobil parking lot with a simple first come first serve approach.

Copyright (C) 2008 DLR/TS, Germany
All rights reserved
"""
#import vehicleControl
import vehicleControl_new as vehicleControl
import statistics
from constants import *

class SimpleManager(vehicleControl.Manager):

    def __init__(self):
        self.cyberCarLoad = {}
        self.personsWaitingAt = {}

    def personArrived(self, personID, edge, target):
        if not edge in self.personsWaitingAt:
            self.personsWaitingAt[edge] = []
        self.personsWaitingAt[edge].append((personID, target))

    def cyberCarArrived(self, vehicleID, edge):
        step = vehicleControl.getStep()
        footEdge = edge.replace("cyber", "footmain")
        wait = 0
        load = []
        for person, target in self.cyberCarLoad.get(vehicleID, []):
            if target == footEdge:
                statistics.personUnloaded(person, step)
                wait += WAIT_PER_PERSON
            else:
                load.append((person, target))
        while self.personsWaitingAt.get(footEdge, []) and len(load) < vehicleControl.getCapacity():
            person, target = self.personsWaitingAt[footEdge].pop(0)
            vehicleControl.leaveStop(person)
            statistics.personLoaded(person, step)
            load.append((person, target))
            wait += WAIT_PER_PERSON
        vehicleControl.leaveStop(vehicleID, delay=wait)
        if edge == "cyberout" or edge == "cyberin":
            row = -1
        else:
            row = int(edge[5])
        if row < DOUBLE_ROWS-1:
            vehicleControl.stopAt(vehicleID, "cyber%sto%s" % (row+1, row+2))
        else:
            vehicleControl.stopAt(vehicleID, "cyberout")
        self.cyberCarLoad[vehicleID] = load

if __name__ == "__main__":
    vehicleControl.init(SimpleManager())
