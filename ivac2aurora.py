#!/usr/bin/python

from xml.dom import minidom
import json
import re

PLG_BEG = """    {{
      "type": "Feature",
      "properties": {{
        "stroke": "#555555",
        "stroke-width": 2,
        "stroke-opacity": 1,
        "fill": "#555555",
        "fill-opacity": 0.5,
        "desc": "{}"
      }},
      "geometry": {{
        "type": "Polygon",
        "coordinates": [
          ["""

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

HDR = """{\n  "type": "FeatureCollection",\n  "features": ["""
TAIL = """  ]\n}"""

def dms2dec(dms):
	match = re.search(r'\w([0-9]{3})([0-9]{2})([0-9]{5})', dms)
	dms_d = float(match.group(1))
	dms_m = float(match.group(2))
	dms_s = float(match.group(3))/1000
	return dms_d + dms_m/60 + dms_s/3600

def print_geojson(elements, types = []):
	print HDR

	for element in elements:
		if element['desc'] not in types and types:
			continue
		if element['type'] == "Polygon":
			print PLG_BEG.format(element['desc'])
		if element['type'] == "LineString":
			print LNE_BEG.format(element['desc'])
		for point in element['coordinates']:
			print "            [ {}, {} ], ".format(dms2dec(point['lon']),
													dms2dec(point['lat']))
		print "            [ {}, {} ] ".format(dms2dec(element['coordinates'][0]['lon']),
												dms2dec(element['coordinates'][0]['lat']))
		if element['type'] == "Polygon":
			print "          ]"
		print ELM_END

	print TAIL

def print_aurora(elements, types = []):
	for element in elements:
		if element['desc'] not in types and types:
			continue
		print "// {} - {}".format(element['desc'], element['type'])
		for point in element['coordinates']:
			print point['lon'], point['lat']

def main():
	f_xml = minidom.parse('ukoo/afcad_UKOO.map')
	paths = f_xml.getElementsByTagName('path')

	elements = []

	for path in paths:
		element = {}
		coordinates = []

		if path.hasAttribute('fill_color'):
			element['type'] = "Polygon"
			element['desc'] = path.attributes['fill_color'].value
		else:
			element['type'] = "LineString"
			element['desc'] = path.attributes['stroke_color'].value
	
		points =  path.getElementsByTagName('point')

		for point in points:
			coordinates.append( {'lon':point.attributes['lon'].value, 'lat':point.attributes['lat'].value } )

		element['coordinates'] = coordinates
		elements.append(element)

	#for element in elements:
	#	print element['desc']
	print_geojson(elements, 'ad_stand')
	#print_aurora(elements)

if __name__== "__main__":
	main()