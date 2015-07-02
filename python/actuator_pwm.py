
import mraa, datetime
from tracking import distAO1, distAO2, myLoc, effectiveActuatorHeight1, effectiveActuatorHeight2, secToWait
import pwm_funcs as pwm
from twisted.internet import task, reactor
import solarserver as s

class Run:
	"""The Run class connects client<-->server, sends tilt data, and moves the actuators."""
	def __init__(self, client_ip, client_port, maxActuatorHeight):

		self.client = s.WSClient(client_ip, client_port)
		self.client.debug = True
		self.minActuatorHeight = 0 
		self.maxActuatorHeight = maxActuatorHeight
		tiltPercent = 0

	def connectToServer(self):
		s.connectWS(self.client)


	def reactorLoop(self):
		loop = task.LoopingCall(self.moveA)
		loop.start(secToWait)
		reactor.run()

	"""Actuator a, tilting the panel up and down to maintain a 45 degree angle with the sun, is called every second by the reactor timer."""
	def moveA(self):
		print(datetime.datetime.now().strftime('%H:%M:%S PST'))
		print(" |", "\n", "V")
		height = myLoc.calcTiltingHeight(distAO1, datetime.datetime.now())
		tiltPercent = effectiveActuatorHeight1 / self.maxActuatorHeight
		self.client.update(tiltPercent)
		# a = pwm.Actuator(3, tiltPercent, 700, True) #comment these two lines out to see realtime values on your machine (ubuntu isn't mraa compatible)
		# a.move(tiltPercent)
	
	"""Actuator b is for panning the panel horizonally according to the azimuth. Currently NOT implemented in the DollHouse."""
	def moveB():
		print(datetime.datetime.now().strftime('%H:%M:%S PST'))
		print(" |", "\n", "V")
		myLoc.calcPanningHeight(distAO2, datetime.datetime.now())
		panPercent = effectiveActuatorHeight2 / maxActuatorHeight
		client.update(tiltPercent2)
		# b = pwm.Actuator(3, panPercent, 700, True) #comment these two lines out if you want to see height change over time on your machine (ubuntu pc is not mraa compatible)
		# b.move(panPercent)

	##instatiate client and tell it connect to local host.
	# def createServer():
	# 	solarServer = s.SolarServer()
	# 	solarServer.debug = False
	# 	#client = s.WSClient("127.0.0.1", "1913")
	# 	print("READ actuator_pwm.py; client is ", self.client)


