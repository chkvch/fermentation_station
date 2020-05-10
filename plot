#! /bin/bash
#python3 fancy_plot.py
cd /home/pi/station
date
gnuplot plott.p
date
gnuplot ploth.p
date
gnuplot plotp.p
date
./write_24h
date
gnuplot plott_24h.p
date
gnuplot ploth_24h.p
date
gnuplot plotp_24h.p
date
