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
#with open('station.log', 'w') as f:
#	pass
target_t_f = 85.
t_safe = 100.
from importlib import reload
cadence = 5 # seconds
last_time_s = None
last_error = None
while True:
	data = bme280.sample(bus, address, calibration_params)

	t_f = data.temperature * 9. / 5 + 32.
	with open('status', 'r') as f:
		status = f.readline()
	output = '{:30} {:10s} {:5.2f} {:8.2f} {:5.2f}'.format(str(data.timestamp), status, t_f, data.pressure, data.humidity)
	with open('station.log', 'a') as f:
		#f.write('{} error={:.3f} dt={:6.3f}s p={:.3f} i={:.3f} d={:.3f} pid={:.3f}'.format(output, error, dt, p, i, d, pid))
		f.write('{}\n'.format(output))
	time_s = tm.mktime(data.timestamp.timetuple())

	if t_f > t_safe:
		print('temperature {:.2f} > safe temperature {:.2f}; safe mode'.format(t_f, t_safe))
		os.system('./safe')
	#elif t_f < target_t_f:
	#	os.system('./on')
	#else:
	#	os.system('./off')
	else:
		error = t_f - target_t_f
		kp = 1
		ki = kp / 300 # 5-minute integration time
		kd = kp * 300 # 5-minute derivative time
		p = kp * error
		if last_time_s:
			dt = time_s - last_time_s
			i += ki * 0.5 * (error + last_error) * dt
			d = kd * (error - last_error) / dt
		else:
			dt = 0
			i = 0
			d = 0
		# now instead of comparing t_f to target_t_f, compare p+i+d to zero
		last_time_s = time_s
		last_error = error

		pid = p + i + d
		full_output = '{} error={:.3f} dt={:6.3f}s p={:.3f} i={:.3f} d={:.3f} pid={:.3f}'.format(output, error, dt, p, i, d, pid)
		print(full_output)
		loginf(full_output)
		if pid > 0:
			try:
				os.system('./off')
			except Exception as e:
				logerr(str(e.args[0]))
				with open('station.e', 'a') as ferr:
					ferr.write('{} {}\n'.format(str(e), full_output))
		elif pid < 0:
			try:
				os.system('./on')
			except Exception as e:
				logerr(str(e.args[0]))
				with open('station.e', 'a') as ferr:
					ferr.write('{} {}\n'.format(str(e), full_output))
		else:
			logerr('error {} not a number'.format(pid))
			raise ValueError('error not a number')

	tm.sleep(cadence)
