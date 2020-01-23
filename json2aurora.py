#!/usr/bin/python

import json

def dec2dms(dec):
	N_d = int(dec[1])
	N_m = int((dec[1] - N_d) * 60)
	N_s = (dec[1] - N_d - N_m / float(60)) * 3600
	E_d = int(dec[0])
	E_m = int((dec[0] - E_d) * 60)
	E_s = (dec[0] - E_d - E_m / float(60)) * 3600
	return "N{0:03d}.{1:02d}.{2:06.3f};E{3:03d}.{4:02d}.{5:06.3f};".format(N_d, N_m, N_s, E_d, E_m, E_s)

def main():
	with open("ukoo/ukoo.geojson", "r") as read_file:
		data = json.load(read_file)

	for feature in data['features']:
		# Check if feature has key 'desc'
		if feature['properties'].has_key('desc'):
			desc = feature['properties']['desc']
		else:
			desc = "None"
		
		# Print comment line with Name and Type
		print "// {} - {}".format(desc, feature['geometry']['type'])

		# Print coordinates for Polygon without last point
		if feature['geometry']['type'] == "Polygon":
			for coordinates in feature['geometry']['coordinates']:
				for point in coordinates[:-1]:
					print dec2dms(point)
		# Print coordinates for Points
		elif feature['geometry']['type'] == "Point":
			print dec2dms(feature['geometry']['coordinates'])
		# Print coordinates for LineString with doubling second point
		else:
			i = 1
			while i < len(feature['geometry']['coordinates']):
				print "{}{}".format(dec2dms(feature['geometry']['coordinates'][i - 1]),
									dec2dms(feature['geometry']['coordinates'][i]))
				i += 1




if __name__== "__main__":
	main()