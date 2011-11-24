#!/usr/bin/python
"""
@file    removeSVN.py
@author  Daniel.Krajzewicz@dlr.de
@date    28-08-2008
@version $Id: removeSVN.py 8236 2010-02-10 11:16:41Z behrisch $

Copyright (C) 2008 DLR/TS, Germany
All rights reserved
"""

import os, sys, stat, shutil


path = "./"
if len(sys.argv)>1:
    path = sys.argv[1]

# remove files in ".svn"
for root, dirs, files in os.walk(path):
    if root.find(".svn")>=0:
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IWRITE|stat.S_IREAD)
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IWRITE|stat.S_IREAD)
    
# remove dirs in ".svn"
for root, dirs, files in os.walk(path):
    if ".svn" in dirs:
        dirs.remove(".svn")
        os.chmod(os.path.join(root, ".svn"), stat.S_IWRITE|stat.S_IREAD)
        shutil.rmtree(os.path.join(root, ".svn"))


