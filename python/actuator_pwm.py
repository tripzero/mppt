# Pulse width modification is used to move the actuator variably. 
#Documentation:  http://iotdk.intel.com/docs/master/mraa/python/mraa.html#mraa.Pwm
import mraa, time
from tracking import effectiveActuatorHeight

pulse = mraa.Pwm(3)
pulse.enable(True)
pulse.period_us(700) #sets period in microseconds

maxActuatorHeight = 2
percent = effectiveActuatorHeight / maxActuatorHeight
pulse.write(percent) #verify

