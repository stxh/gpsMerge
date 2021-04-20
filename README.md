# gpsMerge
Merger gps information from phone photos to camera photos
Free Software tool to geolocalize informations from:
 - phone photos or other photos which have GPS exif

Sync latitude/longitude informations to camera photos in their EXIF GPS section

# Install
Clone this repository or download the source code zip  

## Install piexif
```
pip install piexif
```

# Usage
Run this tool  
```bash
$ python gpstk.py -h

Usage: gpstk.py [options]

Options:
  -h, --help            show this help message and exit
  -g GPSFILEPATH, --gpath=GPSFILEPATH
                        Path to phone photos. (HAVE GPS exif)
  -c NOGPSFILEPATH, --cpath=NOGPSFILEPATH
                        Directory containing the pictures. (NO GPS exif)
  -f, --force           Force replace GPS exif
```

Or just ```$python gpstk.py```

Select source path which take photos with GPS information. Than select target path holding your camera photos.

# ToDo
 - Generate KML file
 - Adjust time
 - Set position manually