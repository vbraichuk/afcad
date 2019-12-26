#!/usr/bin/python

import json

def dec2dms(declist):

	for point in declist:
		N_d = int(point[1])
		N_m = int((point[1] - N_d) * 60)
		N_s = (point[1] - N_d - N_m / float(60)) * 3600
		E_d = int(point[0])
		E_m = int((point[0] - E_d) * 60)
		E_s = (point[0] - E_d - E_m / float(60)) * 3600
		print "N{0:03d}.{1:02d}.{2:07.3f};E{3:03d}.{4:02d}.{5:07.3f};".format(N_d, N_m, N_s, E_d, E_m, E_s)

def main():
  with open("taxi.geojson", "r") as read_file:
    geo = json.load(read_file)

  for items in geo['features']:
    print items['geometry']['type']
    dec2dms(items['geometry']['coordinates'])

	#dec2dms(polygon)

if __name__== "__main__":
	main()
