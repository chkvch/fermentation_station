# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

import syslog
import threading
def logmsg(level, msg):
    syslog.syslog(level, 'station: {}: {}'.format(threading.currentThread().getName(), msg))

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

import numpy as np
import time as tm
import os
from importlib import reload
cadence = 60 # seconds
last_time_s = None
last_error = None
while True:
	data = bme280.sample(bus, address, calibration_params)

	t_f = data.temperature * 9. / 5 + 32.
	with open('status', 'r') as f:
		status = f.readline()
	output = '{:30} {:10s} {:5.2f} {:8.2f} {:5.2f}'.format(str(data.timestamp).replace(' ','_'), status, t_f, data.pressure, data.humidity)
	with open('station.log', 'a') as f:
		f.write('{}\n'.format(output))
	time_s = tm.mktime(data.timestamp.timetuple())
	tm.sleep(cadence)
