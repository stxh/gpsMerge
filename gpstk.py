# coding: utf-8
'''
Merger gps information from phone photos to camera's
'''

import tkinter as tk
from tkinter import filedialog

from gpsMerge import getGpx, setGps

root = tk.Tk()
root.withdraw()

gpsFilePath = filedialog.askdirectory(title='Please select your phone photos folder (HAVE GPS exif)')
noGpsFilePath = filedialog.askdirectory(title='Please select your camera photos folder (NO GPS exif)')
gpx = getGpx(gpsFilePath)
setGps(noGpsFilePath, gpx)
