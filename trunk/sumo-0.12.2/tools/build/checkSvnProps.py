#!/usr/bin/env python
"""
@file    checkSvnProps.py
@author  Michael.Behrisch@dlr.de
@date    2010
@version $Id: checkSvnProps.py 9256 2010-10-14 09:53:03Z behrisch $

Checks svn property settings for all files.

Copyright (C) 2010 DLR/TS, Germany
All rights reserved
"""

import os, subprocess, sys, xml.sax

_SOURCE_EXT = [".h", ".cpp", ".py", ".pl", ".java", ".am"]
_TESTDATA_EXT = [".xml", ".cfg", ".prog", ".complex", ".dfrouter", ".duarouter", ".jtrrouter", ".netconvert", ".netgen", ".od2trips", ".polyconvert", ".sumo", ".meso", ".tools", ".traci", ".activitygen"]
_VS_EXT = [".vsprops", ".sln", ".vcproj", ".bat", ".props", ".vcxproj", ".filters"]
_KEYWORDS = "HeadURL Id LastChangedBy LastChangedDate LastChangedRevision"

class PropertyReader(xml.sax.handler.ContentHandler):
    """Reads the svn properties of files as written by svn pl -v --xml"""

    def __init__(self, doFix):
        self._fix = doFix
        self._file = ""
        self._property = None
        self._value = ""
        self._hadEOL = False
        self._hadKeywords = False

    def startElement(self, name, attrs):
        if name == 'target':
            self._file = attrs['path']
            seen.add(os.path.join(sumoRoot, self._file))
        if name == 'property':
            self._property = attrs['name']

    def characters(self, content):
        if self._property:
            self._value += content


    def endElement(self, name):
        ext = os.path.splitext(self._file)[1]
        if name == 'property' and self._property == "svn:eol-style":
            self._hadEOL = True
        if name == 'property' and self._property == "svn:keywords":
            self._hadKeywords = True
        if ext in _SOURCE_EXT or ext in _TESTDATA_EXT or ext in _VS_EXT:
            if name == 'property' and self._property == "svn:executable" and ext not in [".py", ".pl", ".bat"]:
                print self._file, self._property, self._value
                if self._fix:
                    subprocess.call(["svn", "pd", "svn:executable", self._file])
            if name == 'property' and self._property == "svn:mime-type":
                print self._file, self._property, self._value
                if self._fix:
                    subprocess.call(["svn", "pd", "svn:mime-type", self._file])
        if ext in _SOURCE_EXT or ext in _TESTDATA_EXT:
            if name == 'property' and self._property == "svn:eol-style" and self._value != "LF"\
               or name == "target" and not self._hadEOL:
                print self._file, "svn:eol-style", self._value
                if self._fix:
                    if os.name == "posix":
                        subprocess.call(["sed", "-i", 's/\r$//', self._file])
                    subprocess.call(["svn", "ps", "svn:eol-style", "LF", self._file])
        if ext in _SOURCE_EXT:
            if name == 'property' and self._property == "svn:keywords" and self._value != _KEYWORDS\
               or name == "target" and not self._hadKeywords:
                print self._file, "svn:keywords", self._value
                if self._fix:
                    subprocess.call(["svn", "ps", "svn:keywords", _KEYWORDS, self._file])
        if ext in _VS_EXT:
            if name == 'property' and self._property == "svn:eol-style" and self._value != "CRLF"\
               or name == "target" and not self._hadEOL:
                print self._file, "svn:eol-style", self._value
                if self._fix:
                    subprocess.call(["svn", "ps", "svn:eol-style", "CRLF", self._file])
        if name == 'property':
            self._value = ""
            self._property = None
        if name == 'target':
            self._hadEOL = False
            self._hadKeywords = False


seen = set()
doFix = len(sys.argv) == 2 and sys.argv[1] in ["-f" , "--fix"]
sumoRoot = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "../../"))
output = subprocess.Popen(["svn", "pl", "-v", "-R", "--xml", sumoRoot], stdout=subprocess.PIPE).communicate()[0]
xml.sax.parseString(output, PropertyReader(doFix))

for root, dirs, files in os.walk(sumoRoot):
    for name in files:
        fullName = os.path.join(root, name)
        if fullName in seen or subprocess.call(["svn", "ls", fullName], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT):
            continue
        ext = os.path.splitext(name)[1]
        if ext in _SOURCE_EXT or ext in _TESTDATA_EXT or ext in _VS_EXT:
            print fullName, "svn:eol-style"
            if doFix:
                if ext in _VS_EXT:
                    subprocess.call(["svn", "ps", "svn:eol-style", "CRLF", fullName])
                else:
                    if os.name == "posix":
                        subprocess.call(["sed", "-i", 's/\r$//', fullName])
                    subprocess.call(["svn", "ps", "svn:eol-style", "LF", fullName])
        if ext in _SOURCE_EXT:
            print fullName, "svn:keywords"
            if doFix:
                subprocess.call(["svn", "ps", "svn:keywords", _KEYWORDS, fullName])
    for ignoreDir in ['.svn', 'foreign', 'mesosim', 'mesogui']:
        if ignoreDir in dirs:
            dirs.remove(ignoreDir)
