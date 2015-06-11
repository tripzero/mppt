#!/usr/bin/env python

import mraa
import ina219

class Mode:
	Sweeping = 0
	Searching = 1
	Manual = 3

	SweepUp = 0
	SweepDown = 1

class Mppt:


	mode = Mode.Searching

	def __init__(self, mosfetPin, output, inputVoltsPin, targetVolts):

		self.mosfet = mraa.Pwm(mosfetPin)
		self.mosfet.period_us(700)
		self.mosfet.enable(True)

		self.output = output
		self.input = inputVoltsPin
		self.highWatts = 0
		self.prevWatts = 0
		self.maxWatts = 10
		self.pmwInc = 1
		self.targetVolts = targetVolts
		self.inputVoltThreshold = 6
		self.volts = 0
		self.current = 0
		self.sweepMode = Mode.SweepUp
		self.pwmValue = 0

	def begin(self):

		if self.targetVolts == 0:
			print("please set target volts")

		self.output.begin()

	def poll(self):

		amps = self.output.current()
		outputVolts = self.output.busVoltage()
		outputWatts = outputVolts * (amps/1000)
		inputVolts = 7 #TODO: read actual input volts!

		self.volts = outputVolts
		self.current = amps

		if self.mode == Mode.Searching:
			self.search(outputWatts, outputVolts, inputVolts)
			self.pwmValue += (self.pwmInc * 0.01)
		elif self.mode == Mode.Sweeping:
			self.sweep()
			self.pwmValue += (self.pwmInc * 0.01)

		if self.pwmValue > 1.0:
			self.pwmValue = 1.0
		if self.pwmValue < 0:
			self.pwmValue = 0.0

		self.mosfet.write(self.pwmValue)

	def search(self, outputWatts, outputVolts, inputVolts):

		if outputWatts < self.prevWatts:
			self.pwmInc = -1
		elif outputWatts > 0 and outputWatts >= prevWatts:
			self.pwmInc = 1

		self.prevWatts = outputWatts

		if outputWatts > self.highWatts:
			self.highWatts = outputWatts

		if outputVolts > self.targetVolts or outputWatts > self.maxWatts or outputVolts == 0:
			self.pwmInc = -1

		if inputVolts < self.inputVoltThreshold:
			self.pwmInc = -1

	def sweep(self):
		if pwmValue >= 1.0:
			self.sweepMode = Mode.SweepDown
		elif pwmValue <= 0.0:
			self.sweepMode = Mode.SweepUp

		if self.sweepMode == Mode.SweepUp:
			self.pwmInc = 1
		else:
			self.pwmInc = -1



