# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

import numpy as np
import time
import os
#with open('station.log', 'w') as f:
#	pass
target_t_f = 85.
import plot
from importlib import reload
cadence = 10 # seconds
while True:
	data = bme280.sample(bus, address, calibration_params)

	t_f = data.temperature * 9. / 5 + 32.
	with open('status', 'r') as f:
		status = f.readline()
	output = '{:30} {:10s} {:5.2f} {:8.2f} {:5.2f}'.format(str(data.timestamp), status, t_f, data.pressure, data.humidity)
	print(output)
	with open('station.log', 'a') as f:
		f.write('{}\n'.format(output))

	if t_f > 95.:
		os.system('./safe')
	elif t_f < target_t_f:
		os.system('./on')
	else:
		os.system('./off')

	reload(plot)
	plot.make()
	time.sleep(cadence)

	#print(data.id)
	#print(data.timestamp)
	#print(data.temperature)
	#print(data.pressure)
	#print(data.humidity)
#print('ok')

#print('testing interface to network smartplug')
#import collector
#sp = collector.smartplug('192.168.2.110')
#print(sp.do('info'))
#print(sp.do('off'))
#print(sp.do('on'))
#print('ok')

