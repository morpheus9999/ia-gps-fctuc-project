#!/usr/bin/env python
"""
@file    sumonet.py
@author  Daniel.Krajzewicz@dlr.de
@date    2008-03-27
@version $Id: sumonet.py 8836 2010-06-30 10:49:42Z bieker $

This scrip can be used as a content handler for parsing xml files.
These classes represents a sumo network.

Copyright (C) 2008 DLR/TS, Germany
All rights reserved
"""

import os, sys
from xml.sax import saxutils, make_parser, handler
from copy import copy
from itertools import *

class NetLane:
    """ Lanes from a sumo network """

    def __init__(self, edge, speed, length):
        self._edge = edge
        self._speed = speed
        self._length = length
        self._shape = []
        self._outgoing = []
        edge.addLane(self)

    def getSpeed(self):
        return self._speed

    def getLength(self):
        return self._length 

    def setShape(self, shape):
        self._shape = shape

    def getShape(self):
        return self._shape 

    def getID(self):
        return self._edge._id + "_" + str(self._edge._lanes.index(self))

    def getEdge(self):
        return self._edge

    def addOutgoing(self, tolane, tls, tllink):
        self._outgoing.append( [tolane, tls, tllink ] )


class NetEdge:
    """ Edges from a sumo network """

    def __init__(self, id, fromN, toN, prio, function):
        self._id = id
        self._from = fromN
        self._to = toN
        self._priority = prio
        fromN.addOutgoing(self)
        toN.addIncoming(self)
        self._lanes = []
        self._speed = None
        self._length = None
        self._incoming = []
        self._outgoing = {}
        self._shape = None
        self._function = function
        self._tls = None

    def addLane(self, lane):
        self._lanes.append(lane)
        self._speed = lane.getSpeed()
        self._length = lane.getLength()

    def addOutgoing(self, edge, fromlane, tolane, tls, tllink):
        if edge not in self._outgoing:
            self._outgoing[edge] = []
        self._outgoing[edge].append( [fromlane, tolane, tls, tllink ] )
        fromlane.addOutgoing(tolane, tls, tllink)

    def addIncoming(self, edge):
        if edge not in self._incoming:
            self._incoming.append(edge)

    def setShape(self, shape):
        self._shape = shape

    def getID(self):
        return self._id

    def getIncoming(self):
        return self._incoming

    def getOutgoing(self):
        return self._outgoing

    def getShape(self):
        if not self._shape:
            shape = []
            shape.append(self._from._coord)
            shape.append(self._to._coord)
            return shape
        return self._shape

    def getSpeed(self):
        return self._speed

    def getLaneNumber(self):
        return len(self._lanes)

    def rebuildShape(self):
        noShapes = len(self._lanes)
        if noShapes%2 == 1:
            self.setShape(self._lanes[int(noShapes/2)]._shape)
        else:
            shape = []
            minLen = -1
            for l in self._lanes:
                if minLen==-1 or minLen>len(l.getShape()):
                    minLen = len(l._shape)
            for i in range(0, minLen):
                x = 0.
                y = 0.
                for j in range(0, len(self._lanes)):
                    x = x + self._lanes[j]._shape[i][0]
                    y = y + self._lanes[j]._shape[i][1]
                x = x / float(len(self._lanes))
                y = y / float(len(self._lanes))
                shape.append( [ x, y ] )
            self.setShape(shape)

    def getLength(self):
         return self._lanes[0].getLength()

    def setTLS(self, tls):
         self._tls = tls
         

class NetNode:
    """ Nodes from a sumo network """
    def __init__(self, id, coord, incLanes):
        self._id = id
        self._coord = coord
        self._incoming = []
        self._outgoing = []
        self._foes = {}
        self._prohibits = {}
        self._incLanes = incLanes

    def addOutgoing(self, edge):
        self._outgoing.append(edge)

    def addIncoming(self, edge):
        self._incoming.append(edge)

    def setFoes(self, index, foes, prohibits):
        self._foes[index] = foes
        self._prohibits[index] = prohibits

    def getLinkIndex(self, link):
        ret = 0
        for lid in e._incLanes:
            (e, l) = lid.split("_")
            lane = None
            for et in self._incoming:
                for l in et._lanes:
                    if l==link[0]:
                        lane = l
            
            if l[0]==link[0] and l[1]==link[1]:
                return ret
            ret = ret + 1
        return -1

    def forbids(self, possProhibitor, possProhibited):
        print self._incLanes
        possProhibitorIndex = self.getLinkIndex(possProhibitor)
        possProhibitedIndex = self.getLinkIndex(possProhibited)
#        print possProhibitorIndex
#        print possProhibitedIndex
        if possProhibitorIndex<0 or possProhibitedIndex<0:
            return False
        ps = self._prohibits[possProhibitedIndex]
#        print "%s %s %s" % (len(ps), possProhibitorIndex, possProhibitedIndex)
#        print ps
#        print len(ps)-possProhibitorIndex-1
        if ps[len(ps)-possProhibitorIndex-1]:
            print possProhibitorIndex
        return ps[len(ps)-possProhibitorIndex-1]=='1'

class NetTLS:
    """Trafic Light Signal for a sumo network"""
    def __init__(self, id):
        self._id = id
        self._connections = []
        self._maxConnectionNo = -1
        self._programs = {}

    def addConnection(self, inLane, outLane, linkNo):
        self._connections.append( [inLane, outLane, linkNo] )
        if linkNo>self._maxConnectionNo:
            self._maxConnectionNo = linkNo

    def getEdges(self):
        edges = set()
        for c in self._connections:
            edges.add(c[0].getEdge())
        return edges

    def addProgram(self, program):
        self._programs[program._id] = program


class NetTLSProgram:
    def __init__(self, id, offset, type):
        self._id = id
        self._type = type
        self._offset = offset
        self._phases = []

    def addPhase(self, state, duration):
        self._phases.append( (state, duration) )

class NetRoundabout:
    def __init__(self, nodes):
        self._nodes = nodes

    def getNodes(self):
        return self._nodes

class Net:
    """The whole sumo network."""
    def __init__(self):
        self._id2node = {}
        self._id2edge = {}
        self._id2tls = {}
        self._nodes = []
        self._edges = []
        self._tlss = []
        self._ranges = [ [10000, -10000], [10000, -10000] ]
        self._roundabouts = []

    def addNode(self, id, coord=None, incLanes=None):
        if id not in self._id2node:
            node = NetNode(id, coord, incLanes)
            self._nodes.append(node)
            self._id2node[id] = node
        if coord!=None and self._id2node[id]._coord==None:
            self._id2node[id]._coord = coord
            self._ranges[0][0] = min(self._ranges[0][0], coord[0])
            self._ranges[0][1] = max(self._ranges[0][1], coord[0])
            self._ranges[1][0] = min(self._ranges[1][0], coord[1])
            self._ranges[1][1] = max(self._ranges[1][1], coord[1])
        if incLanes!=None and self._id2node[id]._incLanes==None:
            self._id2node[id]._incLanes = incLanes
        return self._id2node[id]

    def addEdge(self, id, fromID, toID, prio, function):
        if id not in self._id2edge:
            fromN = self.addNode(fromID)
            toN = self.addNode(toID)
            edge = NetEdge(id, fromN, toN, prio, function)
            self._edges.append(edge)
            self._id2edge[id] = edge
        return self._id2edge[id]

    def addLane(self, edge, speed, length):
        lane = NetLane(edge, speed, length)
        return lane

    def addRoundabout(self, nodes):
        roundabout = NetRoundabout(nodes)
        self._roundabouts.append(roundabout)
        return roundabout
    
    def getRoundabouts(self):
        return self._roundabouts
        
    def getEdge(self, id):
        return self._id2edge[id]

    def getNode(self, id):
        return self._id2node[id]

    def getTLSSecure(self, tlid):
        if tlid in self._id2tls:
            tls = self._id2tls[tlid]
        else:
            tls = NetTLS(tlid)
            self._id2tls[tlid] = tls
            self._tlss.append(tls)
        return tls

    def addTLS(self, tlid, inLane, outLane, linkNo):
        tls = self.getTLSSecure(tlid)
        tls.addConnection(inLane, outLane, linkNo)
        return tls

    def addTLSProgram(self, tlid, programID, offset, type):
        tls = self.getTLSSecure(tlid)
        program = NetTLSProgram(programID, offset, type)
        tls.addProgram(program)
        return program


    def setFoes(self, junctionID, index, foes, prohibits):
        self._id2node[junctionID].setFoes(index, foes, prohibits)

    def forbids(self, possProhibitor, possProhibited):
        return possProhibitor[0].getEdge()._to.forbids(possProhibitor, possProhibited)

    def getDownstreamEdges(self, edge, distance, stopOnTLS):
        ret = []
        seen = set()
        toProc = []
        toProc.append( [edge, 0, [] ] )
        while not len(toProc)==0:
            ie = toProc.pop()
            if ie[0] in seen:
                continue
            seen.add(ie[0])
            if ie[1] + ie[0].getLength() >= distance:
                ret.append( [ie[0], ie[0].getLength()+ie[1]-distance, ie[2], False] )
                continue
            if len(ie[0]._incoming)==0:
                ret.append( [ie[0], ie[0].getLength()+ie[1], ie[2], True] )
                continue
            mn = []
            hadTLS = False
            for ci in ie[0]._incoming:
                if ci not in seen:
                    prev = copy(ie[2])
                    if stopOnTLS and ci._tls and ci!=edge and not hadTLS:
                        ret.append( [ie[0], ie[1], prev, True ] )
                        hadTLS = True
                    else:
                        prev.append(ie[0])
                        mn.append( [ci, ie[0].getLength()+ie[1], prev ] )
            if not hadTLS:
                toProc.extend(mn)
        return ret

    
class NetReader(handler.ContentHandler):
    """Reads a network, storing the edge geometries, lane numbers and max. speeds"""

    def __init__(self, **others):
        self._net = Net()
        self._currentEdge = None
        self._currentNode = None
        self._currentLane = None
        self._currentShape = ""
        self._withPhases = 'withPrograms' in others.keys() and others['withPrograms']==True

    def startElement(self, name, attrs):
        if name == 'edge':
            if not attrs.has_key('function') or attrs['function'] != 'internal':
                prio = -1
                if attrs.has_key('priority'):
                    prio = int(attrs['priority'])
                self._currentEdge = self._net.addEdge(attrs['id'], attrs['from'], attrs['to'], prio, attrs['function'])
            else:
                self._currentEdge = None
        if name == 'lane' and self._currentEdge!=None:
            self._currentLane = self._net.addLane(self._currentEdge, float(attrs['maxspeed']), float(attrs['length']))
            if attrs.has_key('shape'):
                self._currentShape = attrs['shape'] # deprecated: at some time, this is mandatory
            else:
                self._currentShape = ""
        if name == 'junction':
            if attrs['id'][0]!=':':
                self._currentNode = self._net.addNode(attrs['id'], [ float(attrs['x']), float(attrs['y']) ], attrs['incLanes'].split(" ") )
        if name == 'succ':
            if attrs['edge'][0]!=':':
                self._currentEdge = self._net.getEdge(attrs['edge'])
                self._currentLane = attrs['lane']
                self._currentLane = int(self._currentLane[self._currentLane.rfind('_')+1:])
            else:
                self._currentEdge = None
        if name == 'succlane':
            lid = attrs['lane']
            if lid[0]!=':' and lid!="SUMO_NO_DESTINATION" and self._currentEdge:
                connected = self._net.getEdge(lid[:lid.rfind('_')])
                tolane = int(lid[lid.rfind('_')+1:])
                if attrs.has_key('tl') and attrs['tl']!="":
                    tl = attrs['tl']
                    tllink = int(attrs['linkno'])
                    tlid = attrs['tl']
                    toEdge = self._net.getEdge(lid[:lid.rfind('_')])
                    tolane2 = toEdge._lanes[tolane]
                    tls = self._net.addTLS(tlid, self._currentEdge._lanes[self._currentLane], tolane2, tllink)
                    self._currentEdge.setTLS(tls)
                else:
                    tl = ""
                    tllink = -1
                toEdge = self._net.getEdge(lid[:lid.rfind('_')])
                tolane = toEdge._lanes[tolane]
                self._currentEdge.addOutgoing(connected, self._currentEdge._lanes[self._currentLane], tolane, tl, tllink)
                connected.addIncoming(self._currentEdge)
        if name == 'row-logic':
            self._currentNode = attrs['id']
        if name == 'logicitem':
            self._net.setFoes(self._currentNode, int(attrs['request']), attrs["foes"], attrs["response"])
        if self._withPhases and name=='tl-logic':
            self._currentProgram = self._net.addTLSProgram(attrs['id'], attrs['programID'], int(attrs['offset']), attrs['type'])
        if self._withPhases and name=='phase':
            self._currentProgram.addPhase(attrs['state'], int(attrs['duration']))
        if name == 'roundabout':
            ra= str(attrs['nodes'])
            ra =ra.split(' ')
            self._net.addRoundabout(ra)

    def characters(self, content):
        if self._currentLane!=None:
            self._currentShape = self._currentShape + content


    def endElement(self, name):
        if name == 'lane' and self._currentLane:
            cshape = []
            es = self._currentShape.split(" ")
            for e in es:
                p = e.split(",")
                cshape.append((float(p[0]), float(p[1])))
            self._currentLane.setShape(cshape)
            self._currentLane = None
            self._currentShape = ""
        if name == 'edge' and self._currentEdge:
            self._currentEdge.rebuildShape();
        if name == 'edge':
            self._currentEdge = None
        if name == 'row-logic':
            self._haveROWLogic = False
        if self._withPhases and name=='tl-logic':
            self._currentProgram = None

    def getNet(self):
        return self._net


def readNet(filename, **others):
    parser = make_parser()
    netreader = NetReader(**others)
    parser.setContentHandler(netreader)
    parser.parse(filename)
    return netreader.getNet()
