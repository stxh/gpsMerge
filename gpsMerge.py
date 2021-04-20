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


import os
import piexif
from datetime import datetime

# generator of image files
def getFileList(dir):
    for fileName in sorted(os.listdir ( dir )):
        _, ext = os.path.splitext(fileName)
        if ext.lower() in ['.jpeg', '.jpg', '.tif', '.cr2', '.crw', '.nef', '.pef', '.raw', '.orf', '.dng', '.raf', '.mrw']:
            yield fileName, dir+'/'+fileName

#0th 306 DateTime b'2008:01:10 12:31:30'
def getGpx(dir):
    gpx = {}
    for name, fileName in getFileList(dir):
        exif_dict = piexif.load(fileName)
        dt = exif_dict["0th"][306]
        dt = datetime.strptime(dt.decode('utf-8'), '%Y:%m:%d %H:%M:%S')
        dt = int(dt.timestamp())
        gps = exif_dict["GPS"]
        if gps and dt:
            gpx.update({dt: gps})
        
    return gpx

# insert gps exif
def setGps(dir, gpx, force=False):
    gpxkeys = sorted(gpx)   # for performance
    for name, fileName in getFileList(dir):
        exif_dict = piexif.load(fileName)
        dt = exif_dict["0th"][306]
        dt = datetime.strptime(dt.decode('utf-8'), '%Y:%m:%d %H:%M:%S')
        dt = int(dt.timestamp())
        gps = exif_dict["GPS"]
        if dt and (not gps or force):
            gps = getGpxGps(dt, gpxkeys, gpx)
            exif_dict["GPS"] = gps
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, fileName)
            print("Process GPS exif in {} ok".format(fileName))

# generate gps infomation refer to gpx
def getGpxGps(dt, gpxkeys, gpx):
    t1 = 0
    t2 = 0
    for x in gpxkeys:
        t1 = t2
        if x > dt:
            t2 = x
            break
        else: t2 = x

    # t1 == t2
    if t1 == 0 or dt > t2:
        return gpx[t2]

    # todo find middle gps
    # print(t1, t2, dt, gpx)
    gps1 = gpx[t1]
    lat1 = getDecimalLatLong(gps1[2])
    long1 = getDecimalLatLong(gps1[4])

    gps2 = gpx[t2]
    lat2 = getDecimalLatLong(gps2[2])
    long2 = getDecimalLatLong(gps2[4])

    ratio = (dt - t1) / (t2 - t1)
    lat = lat1 + (lat2 - lat1) * ratio
    long = long1 + (long2 - long1) * ratio

    gps1[2] = getLatLong(lat)
    gps1[4] = getLatLong(long)

    return gps1

# 37.98993055555556 to ((37, 1), (59, 1), (2375, 100))
def getLatLong(De):
    d = int(De)
    m = int((De - d) * 60)
    s = int((De - d - m / 60) * 360000)
    return ((d, 1), (m, 1), (s, 100))

# 2 GPSLatitude ((37, 1), (59, 1), (2375, 100)) to decimal    
def getDecimalLatLong(e):
    return ( e[0][0]/e[0][1] +
            e[1][0]/e[1][1] / 60 +
            e[2][0]/e[2][1] / 3600 ) 
    
# GPS
# 1 GPSLatitudeRef b'N'
# 2 GPSLatitude ((37, 1), (59, 1), (2375, 100))
# 3 GPSLongitudeRef b'E'
# 4 GPSLongitude ((75, 1), (8, 1), (200, 100))
# 5 GPSAltitudeRef 0
# 6 GPSAltitude (867932, 279)
# 12 GPSSpeedRef b'K'
# 13 GPSSpeed (272594, 698959)
# 16 GPSImgDirectionRef b'T'
# 17 GPSImgDirection (1036246, 4737)
# 23 GPSDestBearingRef b'T'
# 24 GPSDestBearing (1036246, 4737)
# 29 GPSDateStamp b'2021:03:29'
# 31 GPSHPositioningError (5, 1)    

if  __name__=="__main__":
    gpsFilePath = "D:\\tmp\\album"
    noGpsFilePath = "D:\\tmp\\noGps"
    gpx = getGpx(gpsFilePath)
    setGps(noGpsFilePath, gpx)


    # exif_dict = piexif.load("D:\\tmp\\album\\1617008266466.jpeg")
    # for ifd in ("0th", "Exif", "GPS", "1st"):
    #     print(ifd)
    #     for tag in exif_dict[ifd]:
    #         print(tag, piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])


