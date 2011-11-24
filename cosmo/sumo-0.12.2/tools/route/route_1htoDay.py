#!/usr/bin/env python
"""
@file    route_1htoDay.py
@author  Daniel.Krajzewicz@dlr.de
@date    11.09.2009
@version $Id: route_1htoDay.py 8994 2010-08-26 07:38:25Z behrisch $

Uses "route_departOffset.py" for building 24 route files which describe
 a whole day assuming the given route files describes an hour.

Copyright (C) 2008 DLR/TS, Germany
All rights reserved
"""

import os, sys, route_departOffset

if len(sys.argv) < 2:
    print "Usage: route_1htoDay.py <INPUT_FILE>"
    sys.exit()
for i in range(0, 24):
    out = sys.argv[1]
    out = out[:out.find(".")] + "_" + str(i) + out[out.find("."):]
    print "Building routes for hour " + str(i) + " into '" + out + "'..."
    route_departOffset.main(sys.argv[1], out, i*3600)
