set terminal pngcairo size 900,600 font "Andale Mono,10"
set output '/var/www/html/image/history.png'
set xdata time
set timefmt "%Y-%m-%d_%H:%M:%S"
set key off
set ylabel "T (deg F)"
set xlabel "time"
set format x "%m/%d"

#n = 12*60
#array A[n]
#samples(x) = $0 > (n-1) ? n : int($0+1)
#mod(x) = int(x) % n
#avg_n(x) = (A[mod($0)+1]=x, (sum [i=1:samples($0)] A[i]) / samples($0))

plot "station.log" using 1:3 with lines title 'data', \
  #"station.log" using 1:(avg_n($3)) with lines title 'filter'
