#!/usr/bin/python

import json
import re

def main():
	with open("ukbb/ad_grass.geojson", "r") as read_file:
		data = json.load(read_file)

	for feature in data['features']:
		print feature['properties']['desc']
		print feature['geometry']['type']

if __name__== "__main__":
	main()