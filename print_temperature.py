# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)

t_f = data.temperature * 9. / 5 + 32.
output = '{:30} {:5.2f} {:8.2f} {:5.2f}'.format(str(data.timestamp), t_f, data.pressure, data.humidity)
print(output)
