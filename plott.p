set terminal pngcairo size 900,600 font "Andale Mono,12"
set output '/var/www/html/image/historyt.png'
set xdata time
set timefmt "%Y-%m-%d_%H:%M:%S"
set key off
set ylabel "T (deg F)"
set xlabel "time"
set format x "%H:%M\n%m/%d"

#plot "station.log" using 1:3 with lines title 'data'

m=5
n = 60
array A[m]
samples_minute(x) = $0 > (m-1) ? m : int($0+1)
mod_minute(x) = int(x) % m
avg_minute(x) = (A[mod_minute($0)+1]=x, (sum [i=1:samples_minute($0)] A[i]) / samples_minute($0))

array B[n]
samples_hour(x) = $0 > (n-1) ? n : int($0+1)
mod_hour(x) = int(x) % n
avg_hour(x) = (B[mod_hour($0)+1]=x, (sum [i=1:samples_hour($0)] B[i]) / samples_hour($0))

plot "station.log" using 1:3 with lines title 'data', \
 "station.log" using 1:(avg_minute($3)) with lines title 'filter' lw 3 lt rgb "red", \
 "station.log" using 1:(avg_hour($3)) with lines title 'filter' lw 2 lt rgb "cyan"
