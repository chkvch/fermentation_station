set terminal pngcairo size 900,600 font "Andale Mono,12"
set output '/var/www/html/image/historyh_24h.png'
set xdata time
set timefmt "%Y-%m-%d_%H:%M:%S"
set key off
set ylabel "Relative humidity (%)"
set xlabel "time"
set format x "%H:%M\n%m/%d"

#plot "station.log" using 1:5 with lines title 'data'
#plot "station.log" using 1:(avg_n($5)) with lines title 'filter'

#m = 12 # one minute at 5s cadence
#n = 12*60 # one hour at 5s cadence
m=5
n = 60 # one hour at one minute cadence
array A[m]
samples_minute(x) = $0 > (m-1) ? m : int($0+1)
mod_minute(x) = int(x) % m
avg_minute(x) = (A[mod_minute($0)+1]=x, (sum [i=1:samples_minute($0)] A[i]) / samples_minute($0))

array B[n]
samples_hour(x) = $0 > (n-1) ? n : int($0+1)
mod_hour(x) = int(x) % n
avg_hour(x) = (B[mod_hour($0)+1]=x, (sum [i=1:samples_hour($0)] B[i]) / samples_hour($0))

plot "station_24h.log" using 1:5 with lines title 'data',\
 "station_24h.log" using 1:(avg_minute($5)) with lines title 'filter' lw 3 lt rgb "red", \
 "station_24h.log" using 1:(avg_hour($5)) with lines title 'filter' lw 2 lt rgb "cyan"
