#!/usr/bin/python

import math

def points_ring(center, radius, num_points):
	points = []
	arc = 2 * math.pi / num_points

	for i in range(num_points):
		angle = arc * i
		x = radius * math.cos(angle) + center[0]
		y = radius * math.sin(angle) + center[1]
		points.append([x, y])
	return points

def main():
	radius = 1
	center = [1, 1]
	num_points = 4

	print points_ring(center, radius, num_points)

if __name__== "__main__":
	main()