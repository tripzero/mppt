import tracker_funcs as t
import json, datetime
from pprint import pprint

#Initialize inputs
with open('config.json') as dataFile:
	config = json.load(dataFile)
print("config.json: ")
pprint(config)

#Configure time
curr_time = datetime.datetime.now()
print("Local time: ", curr_time)

#Example: JF1
print()
jf1 = t.Location("JF1", 45.541718, -122.960381)
t.printLocationInfo(jf1)
t.calcActuatorHeight(jf1, 2.8)
print()

#From config.json
print("Current location via config.json:")
myLoc = t.Location( config["locationInfo"]["name"], config["locationInfo"]["latitude"], config["locationInfo"]["longitude"])
distActuatorToOrigin = config["distInfo"]["distActuatorToOrigin"]
t.printLocationInfo(myLoc)
inches = t.calcActuatorHeight(myLoc, distActuatorToOrigin)
effectiveActuatorHeight = inches
