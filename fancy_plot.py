import numpy as np
import time
import matplotlib.pyplot as plt
import os
import datetime

# make a fancier history plot using python/numpy/matplotlib.
# runs too slow on the single-thread rpi zero w, so opting
# for gnuplot now instead.

def make():
	log = {'time':np.array([]), 'status':np.array([]), 't':np.array([])}
	with open('station.log', 'r') as f:
		i = 1
		while True:
			data = f.readline().split()
			if len(data) == 5:
				date, _time_, t, p, h = data
				status = 'on'
			elif len(data) == 6:
				date, _time_, status, t, p, h = data
			else:
				break
			i += 1
			_time_ = _time_.split(':')
			time = float(_time_[2]) + float(_time_[1]) * 60 + float(_time_[0]) * 3600
			year, month, day = date.split('-')
			time += float(day) * 24 * 3600
			status = {'on':1, 'off':0, 'safe':0}[status]
			log['time'] = np.append(log['time'], time)
			log['t'] = np.append(log['t'], float(t))
			log['status'] = np.append(log['status'], status)
	log['time'] -= log['time'][0]
	log['time'] /= 3600.

	fig, ax = plt.subplots(figsize=(9, 6))
	ax.plot(log['time'], log['t'], 'k-')
	w = 60 * 12 # 1-hour window assuming cadence of 5s
	ax.plot(log['time'][w-1:], np.convolve(log['t'], np.ones(w), 'valid') / w, '-', color='orange', lw=1)
	ax.set_ylabel('T (°F)')

	if False:
		axr = ax.twinx()
		#axr.plot(log['time'], log['status'], 'b-', lw=1)
		x0 = 0
		for i, (x, y) in enumerate(zip(log['time'], log['status'])):
		    if i == len(log['status']) - 1: break
		    if log['status'][i+1] == log['status'][i] - 1:
		        x1 = i
		        axr.fill_betweenx([0, 1], log['time'][x0], log['time'][x1], color='r', alpha=0.3).set_edgecolor('none')
		    elif log['status'][i+1] == log['status'][i] + 1:
		        x0 = i
		    else:
		        continue
		axr.set_ylim(0, 1)
		axr.yaxis.set_ticks([])

	ax.set_xlabel('time (hours)')
	xs = ax.get_xlim()
	ax.hlines(85., *xs, linestyle='--', lw=1)
	ax.set_xlim(*xs)
	from matplotlib import ticker
	ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
	ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))
	ax.yaxis.set_major_locator(ticker.MaxNLocator(steps=[1,2,10]))
	#axr.yaxis.set_ticks([0, 1])
	#axr.yaxis.set_ticklabels(['off', 'on'])
	#plt.savefig('history.pdf')
	plt.title(str(datetime.datetime.now()))
	plt.savefig('/var/www/html/image/history.png', dpi=300)

	ax.set_xlim(left=log['time'][-1] - 3)
	plt.savefig('/var/www/html/image/history_3h.png', dpi=300)
	plt.close('all')

if __name__ == '__main__':
	make()
