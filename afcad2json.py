#!/usr/bin/python

import json
import re

def dms2dec(dms):
	match = re.search(r'([0-9]+)\.([0-9]+)\.([0-9]+\.[0-9]+)', dms)
	dms_d = float(match.group(1))
	dms_m = float(match.group(2))
	dms_s = float(match.group(3))
	return dms_d + dms_m/60 + dms_s/3600

def print_data(data):
	print """{
  "type": "FeatureCollection",
  "features": ["""

	for polygon in data:
		print """    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          ["""
		for i in range(len(polygon)-1):
			print "            [ {0:10.07f}, {1:10.07f} ],".format(polygon[i][0], polygon[i][1])
		print "            [ {0:10.07f}, {1:10.07f} ]".format(polygon[i + 1][0], polygon[i + 1][1])
		print """          ]
        ]
      }
    },"""

	print """  ]
}"""

def main():
	features = []
	coordinates = []

	with open("test.txt", "r") as read_file:
		for line in read_file:
			match = re.search(r'N([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+);E([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
			if match:
				lat = dms2dec(match.group(1))
				lon = dms2dec(match.group(2))
				coordinates.append([lon, lat])
			else:
				#print features
				coordinates = []
				features.append(coordinates)

	features.append(coordinates)

	print_data(features)

if __name__== "__main__":
	main()