# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

print('testing interface to bme280 sensor')
calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
import numpy as np
import time
for i in np.arange(10):
	data = bme280.sample(bus, address, calibration_params)
	print(data) # prints a summary as a string
	time.sleep(0.2)

	#print(data.id)
	#print(data.timestamp)
	#print(data.temperature)
	#print(data.pressure)
	#print(data.humidity)
print('ok')

print('testing interface to network smartplug')
import collector
sp = collector.smartplug('192.168.2.110')
print(sp.do('info'))
print(sp.do('off'))
print(sp.do('on'))
print('ok')

