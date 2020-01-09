#!/usr/bin/python

import json

def dec2dms(dec):
	N_d = int(dec[1])
	N_m = int((dec[1] - N_d) * 60)
	N_s = (dec[1] - N_d - N_m / float(60)) * 3600
	E_d = int(dec[0])
	E_m = int((dec[0] - E_d) * 60)
	E_s = (dec[0] - E_d - E_m / float(60)) * 3600
	print "N{0:03d}.{1:02d}.{2:07.3f};E{3:03d}.{4:02d}.{5:07.3f};".format(N_d, N_m, N_s, E_d, E_m, E_s)

def main():
	with open("ad_grass.geojson", "r") as read_file:
		geo = json.load(read_file)

	for items in geo['features']:
		print items['geometry']['type']
		c_list = items['geometry']['coordinates']
		for coord in c_list:
			if len(coord) > 2:
				for point in coord:
					dec2dms(point)
			else:
				dec2dms(coord)

if __name__== "__main__":
	main()
