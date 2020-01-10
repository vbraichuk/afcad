#!/usr/bin/python

import re
import math

HDR = """{\n  "type": "FeatureCollection",\n  "features": ["""
TAIL = """  ]\n}"""

LNE_BEG = """    {{
      "type": "Feature",
      "properties": {{
        "stroke": "#555555",
        "stroke-width": 2,
        "stroke-opacity": 1,
        "desc": "{}"
      }},
      "geometry": {{
        "type": "LineString",
        "coordinates": ["""

ELM_END = """        ]
      }
    },"""

def dms2dec(dms):
	match = re.search(r'([0-9]+)\.([0-9]+)\.([0-9]+\.[0-9]+)', dms)
	dms_d = float(match.group(1))
	dms_m = float(match.group(2))
	dms_s = float(match.group(3))
	return dms_d + dms_m/60 + dms_s/3600

def dec2dms(dec):
	N_d = int(dec[1])
	N_m = int((dec[1] - N_d) * 60)
	N_s = (dec[1] - N_d - N_m / float(60)) * 3600
	E_d = int(dec[0])
	E_m = int((dec[0] - E_d) * 60)
	E_s = (dec[0] - E_d - E_m / float(60)) * 3600
	return "N{0:03d}.{1:02d}.{2:07.3f};E{3:03d}.{4:02d}.{5:07.3f};".format(N_d, N_m, N_s, E_d, E_m, E_s)

def points_ring(center, radius, num_points):
	points = []
	arc = 2 * math.pi / num_points

	for i in range(num_points):
		angle = arc * i
		x = radius * math.cos(angle) + center[0]
		y = radius * math.sin(angle) + center[1]
		points.append([x, y])
	return points

def print_geojson(elements):
	print HDR

	for element in elements:
		print LNE_BEG.format(element['desc'])
		for point in element['coordinates']:
			print "            [ {}, {} ], ".format(point[1], point[0])
		print "            [ {}, {} ] ".format(element['coordinates'][0][1], element['coordinates'][0][0])
		print ELM_END

	print TAIL

def main():
	elements = []

	with open("ukbb/input/ukbb.gts", "r") as read_file:
		for line in read_file:
			match = re.search(r'^(\w+);\w+;N([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+);E([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+);(\w?)', line)
			if match:
				element = {}
				# match.group(1) - stand
				# match.group(2) - lat
				# match.group(3) - lon
				# match.group(4) - size
				# 
				# create a circle by using 4 points and radius
				# HEAVY  - 0.0003
				# MEDIUM - 0.0002
				# SMALL  - 0.0001
				element['type'] = "LineString"
				element['desc'] = match.group(1)
				radius = 0.0003 if match.group(4) == "H" else 0.0002
				radius = 0.0001 if match.group(4) == "L" else 0.0002

				element['coordinates'] = points_ring( [dms2dec(match.group(2)), dms2dec(match.group(3))], 0.0003, 8)
				elements.append(element)

	print_geojson(elements)

if __name__== "__main__":
	main()