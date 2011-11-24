#!/usr/bin/env python
"""
@file    generateE2TLSDetectors.py 
@author  Daniel.Krajzewicz@dlr.de
@date    2007-10-25
@version $Id: generateTLSE2Detectors.py 8236 2010-02-10 11:16:41Z behrisch $

Copyright (C) 2009 DLR/TS, Germany
All rights reserved
"""
import sys, os
from xml.sax import saxutils, make_parser, handler
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "../lib"))
import sumonet
from optparse import OptionParser

# initialise 
optParser = OptionParser()
optParser.add_option("-n", "--net-file", dest="netfile",
                     help="Net-File to work with", type="string")
optParser.add_option("-l", "--detector-length", dest="detectorLength",
                     help="length of the detector in meters (-1 for maximal length)", type="int", default=250)
optParser.add_option("-d", "--distance-to-TLS", dest="distanceToTLS",
                     help="distance of the detector to the traffic light in meters", type="float", default=.1)
optParser.add_option("-f", "--frequency", dest="frequency",
                     help="frequency", type="int", default=60)
optParser.add_option("-o", "--output", dest="output",
                     help="the name of the file to write the detector definitions into", type="string", default="e2.add.xml")
optParser.add_option("-r", "--results-file", dest="results",
                     help="the name of the file the detectors write their output into", type="string", default="e2output.xml")

optParser.set_usage('\ngenerateTLSE2Detectors.py -n inputs\\pasubio\\pasubio.net.xml -l 250 -d .1 -f 60')
# parse options
(options, args) = optParser.parse_args()
if not options.netfile:
    print "Missing arguments"
    optParser.print_help()
    exit()

netfile = options.netfile
det_length_input = options.detectorLength
distToTLS = options.distanceToTLS
freq = options.frequency

[dirname, filename] = os.path.split(netfile)
prefix = filename.split('.')[0]
dest = os.path.join(dirname, options.output)
detectorFile = open(dest, "w")
print >> detectorFile, "<additional>"

print "Reading net..."
parser = make_parser()
net = sumonet.NetReader()
parser.setContentHandler(net)
parser.parse(netfile)
net = net.getNet()

lanes_ready = {}
for tls in net._tlss:
    for conn in tls._connections:
        lane = conn[0]
        length = lane.getLength()
        id = lane.getID()
        if (not lanes_ready.has_key(id)):
            lanes_ready[id] = True
            if det_length_input == -1:
                det_length = length-distToTLS
            else:
                det_length = min(length-distToTLS, det_length_input)
            pos = max(0,(length-det_length-distToTLS))
            print >> detectorFile, "\t<e2-detector file=\"%s\" freq=\"%d\" friendly_pos=\"x\" id=\"e2det_%s\" lane=\"%s\" pos=\"%f\" length=\"%f\" />" % (options.results, freq, id, id, pos, det_length)

print >> detectorFile, "</additional>"

detectorFile.close()

print "%d e2-detectors generated!" % len(lanes_ready)            
