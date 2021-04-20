#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
#
# Developer:    StXh <stxh007@gmail.com>
# 
# This application is released under the GPL license version 2
#
# More informations and help can be found here: https://github.com/stxh/gpsMerge
#
################################################################################

"""
Merger gps information from phone photos to camera photos
Free Software tool to geolocalize informations from:
 - phone photos or other photos which have GPS exif

Let camera photos sync latitude/longitude informations in their EXIF GPS section
More informations look at:
https://github.com/stxh/gpsMerge
"""

import sys
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-g", "--gpath", dest="gpsFilePath",
    help="Path to phone photos. (HAVE GPS exif)")
parser.add_option("-c", "--cpath", dest="noGpsFilePath",
    help="Directory containing the pictures. (NO GPS exif)")
parser.add_option("-f", "--force", dest="force", action="store_true", default=False,
    help="Force replace GPS exif")

(options, args)=parser.parse_args()

import tkinter as tk
from tkinter import filedialog

from gpsMerge import getGpx, setGps

root = tk.Tk()
root.withdraw()

gpsFilePath = options.gpsFilePath
if not gpsFilePath:
    gpsFilePath = filedialog.askdirectory(title='Please select your phone photos folder (HAVE GPS exif)')
if not gpsFilePath:
    print("Please told me where to find phone photos")
    sys.exit(1)    

noGpsFilePath = options.noGpsFilePath
if not noGpsFilePath:
    noGpsFilePath = filedialog.askdirectory(title='Please select your camera photos folder (NO GPS exif)')
if not noGpsFilePath:
    print("Nothing to do")
    sys.exit(1)    


gpx = getGpx(gpsFilePath)
setGps(noGpsFilePath, gpx, options.force)

print("Process END")
