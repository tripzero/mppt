#!/usr/bin/env python

import mraa
import time

class i2c:
	INA219_ADDRESS = 0x40     #// 1000000 (A0+A1=GND)
	INA219_READ = 0x01

class Registers:
	INA219_REG_CONFIG = 0x00
	INA219_CONFIG_RESET = 0x8000# Reset Bit

	INA219_CONFIG_BVOLTAGERANGE_MASK = 0x2000 # Bus Voltage Range Mask
	INA219_CONFIG_BVOLTAGERANGE_16V = 0x0000 # 0-16V Range
	INA219_CONFIG_BVOLTAGERANGE_32V = 0x2000 # 0-32V Range

	INA219_CONFIG_GAIN_MASK = 0x1800 # Gain Mask
	INA219_CONFIG_GAIN_1_40MV = 0x0000 # Gain 1, 40mV Range
	INA219_CONFIG_GAIN_2_80MV = 0x0800 # Gain 2, 80mV Range
	INA219_CONFIG_GAIN_4_160MV = 0x1000 # Gain 4, 160mV Range
	INA219_CONFIG_GAIN_8_320MV = 0x1800 # Gain 8, 320mV Range

	INA219_CONFIG_BADCRES_MASK = 0x0780 # Bus ADC Resolution Mask
	INA219_CONFIG_BADCRES_9BIT = 0x0080 # 9-bit bus res = 0..511
	INA219_CONFIG_BADCRES_10BIT = 0x0100 # 10-bit bus res = 0..1023
	INA219_CONFIG_BADCRES_11BIT = 0x0200 # 11-bit bus res = 0..2047
	INA219_CONFIG_BADCRES_12BIT = 0x0400 # 12-bit bus res = 0..4097

	INA219_CONFIG_SADCRES_MASK = 0x0078 # Shunt ADC Resolution and Averaging Mask
	INA219_CONFIG_SADCRES_9BIT_1S_84US = 0x0000 # 1 x 9-bit shunt sample
	INA219_CONFIG_SADCRES_10BIT_1S_148US = 0x0008 # 1 x 10-bit shunt sample
	INA219_CONFIG_SADCRES_11BIT_1S_276US = 0x0010 # 1 x 11-bit shunt sample
	INA219_CONFIG_SADCRES_12BIT_1S_532US = 0x0018 # 1 x 12-bit shunt sample
	INA219_CONFIG_SADCRES_12BIT_2S_1060US = 0x0048 	 # 2 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_4S_2130US = 0x0050 # 4 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_8S_4260US = 0x0058 # 8 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_16S_8510US = 0x0060 # 16 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_32S_17MS = 0x0068 # 32 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_64S_34MS = 0x0070 # 64 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_128S_69MS = 0x0078 # 128 x 12-bit shunt samples averaged together

	INA219_CONFIG_MODE_MASK = 0x0007 # Operating Mode Mask
	INA219_CONFIG_MODE_POWERDOWN = 0x0000
	INA219_CONFIG_MODE_SVOLT_TRIGGERED = 0x0001
	INA219_CONFIG_MODE_BVOLT_TRIGGERED = 0x0002
	INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED = 0x0003
	INA219_CONFIG_MODE_ADCOFF = 0x0004
	INA219_CONFIG_MODE_SVOLT_CONTINUOUS = 0x0005
	INA219_CONFIG_MODE_BVOLT_CONTINUOUS = 0x0006
	INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS = 0x0007

	#SHUNT VOLTAGE REGISTER (R)
	INA219_REG_SHUNTVOLTAGE = 0x01

	#BUS VOLTAGE REGISTER (R)
	INA219_REG_BUSVOLTAGE = 0x02

	#POWER REGISTER (R)
	INA219_REG_POWER = 0x03

	#CURRENT REGISTER (R)
	INA219_REG_CURRENT = 0x04

	#CALIBRATION REGISTER (R/W)
	INA219_REG_CALIBRATION = 0x05

class Ina219:

	def __init__(self, addr = i2c.INA219_ADDRESS):
		self.address = addr
		self.currentDivider_mA = 0
		self.powerDivider_mW = 0

	def begin(self):
		self.i2c = mraa.I2c(1)
		self.i2c.address(self.address)

		#calibrate to 32V 2A
		self.calValue = 4096
		self.currentDivider_mA = 10
		self.powerDivider_mW = 2
		config = (Registers.INA219_CONFIG_BVOLTAGERANGE_32V |
			Registers.INA219_CONFIG_GAIN_8_320MV |
			Registers.INA219_CONFIG_BADCRES_12BIT |
			Registers.INA219_CONFIG_SADCRES_12BIT_1S_532US |
			Registers.INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS)
		self.writeRegister(Registers.INA219_REG_CONFIG, config);

	def readRegister(self, reg):
		self.i2c.address(self.address)
		byte1 = self.i2c.readReg(reg)
		byte2 = self.i2c.readReg(reg)
		print ("byte1:", byte1)
		print ("byte2:", byte2)
		value = (( byte1 << 8) | byte2)
		return value

	def writeRegister(self, reg, value):
		self.i2c.address(self.address)
		self.i2c.writeReg(reg, (value >> 8) & 0xFF) #upper 8-bits
		self.i2c.writeReg(reg, value & 0xFF) # lower 8-bits

	def current(self):
		self.i2c.address(self.address)
		self.writeRegister(Registers.INA219_REG_CALIBRATION, self.calValue)
		valueRaw = self.readRegister(Registers.INA219_REG_CURRENT)
		valueDec = valueRaw / self.currentDivider_mA
		return valueDec

	def busVoltage(self):
		value = self.readRegister(Registers.INA219_REG_BUSVOLTAGE)
		return ((value >> 3) * 4) * 0.001
