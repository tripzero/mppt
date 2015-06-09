# Pulse width modification is used to move the actuator variably. 
#Documentation:  http://iotdk.intel.com/docs/master/mraa/python/mraa.html#mraa.Pwm

import mraa, time
from tracker import actuatorHeight

print("Effective actuator height: ", actuatorHeight)
pulse = mraa.Pwm(3)
pulse.enable(True)
pulse.period_us(700) #sets period in microseconds

maxActuatorHeight = 2
percent = actuatorHeight / maxActuatorHeight
val = 0
while val <= percent:
	print(val)
	pulse.write(val)
	time.sleep(0.09) #verify speed is fine
	val = val + 0.01

