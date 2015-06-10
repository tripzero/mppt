#!/usr/bin/env python
# import pysolar #docs.pysolar.org/en/latest/
import datetime, json
from pysolar.solar import *
from pprint import pprint
from math import tan, radians

curr_time = datetime.datetime.now()

"""A location has time-specific altitude, azimuth values (degrees) as per Pysolar"""
class Location:
	"""Returns a new Location object"""
	def __init__(self, name, lat, lon):
		self.name = name
		self.lat = lat
		self.lon = lon

	def coords(self):
		return (self.lat, self.lon)

	def alt(self, lat, lon):
		a = get_altitude(lat, lon, curr_time)
		return a

	def azimuth(self, lat, lon):
		a = get_azimuth(lat, lon, curr_time)
		return a


"""Print all relevant location Data"""
def printLocationInfo(loc):
	print("location object name: ", loc.name)
	print_coords(loc)
	print_alt(loc)
	print_azimuth(loc)

def print_coords(loc):
	print("Coordinates of " + str(loc.name) + ": (", loc.lat, ",", loc.lon, ")")
def print_alt(loc):
	print(str(loc.name) + " alt: ", loc.alt(loc.lat, loc.lon))
def print_azimuth(loc):
	print(str(loc.name) + " azimuth: ", loc.azimuth(loc.lat, loc.lon))

# a = Actuator height
# o = origin
# H = distance from actuator to the pivot socket = distActuatorToPivot
#         /|  |
#        / |  |
#       /  |  |
#      /   |  | 
#    H/    |  a
#    /     |  | 
#   /      |  |
#  /       |  |
# /S1______|  |
#O<-pivot bolt
# ---------<-distActuatorToOrigin

"""Calculate the most effective height of the actuator based upon the assumption solar panels are most efficent angled 45 degrees to the sun. Dist(a, o) is represented by base. Math: tan(S1) = a / distActuatorToOrigin & S1 = 90 - altitude ==> a = tan(90-altitude) * distActuatorToOrigin"""
def calcActuatorHeight(loc, actuatorOriginDist):
	val = 90 - loc.alt(loc.lat, loc.lon)
	left = tan(radians(val))
	right = actuatorOriginDist
	a = left * right
	print("Calculated (effective) actuator height: ", a, " inches")
	return a





