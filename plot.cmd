set encoding iso_8859_1
set terminal png large size 600,1000
set output "24hrs_full_features.png"
set multiplot layout 5, 1 
set style fill solid
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set lmargin 4
set rmargin 4
set format x "%H%M"
set xtics 7200

set key horizontal title "Temperature"
set ylabel "°C"
set y2label "%"
set bmargin -1
set yrange [*:*]
set y2range [0: 100]
set ytics nomirror autofreq
set y2tics autofreq
unset grid
set boxwidth 240
plot "plot.dat" using 1:2 axes x1y1 title "Temperature (°C)" smooth unique lc 1 lw 2, \
 "plot.dat" using 1:3 axes x1y1 title "Dew point (°C)" smooth unique lc 3 lw 1, \
 "plot.dat" using 1:4 axes x1y2 title "Humidity (%)" smooth unique lc 2 lw 1

set key horizontal title "Wind speed (knots)"
set ylabel
set y2label
set bmargin -1
set yrange [*:*]
unset y2tics
set ytics mirror autofreq
unset grid
set boxwidth 240
plot "plot.dat" using 1:7 axes x1y1 title "gust" smooth unique lc 4 lw 1, \
 "plot.dat" using 1:5 axes x1y1 title "average" smooth unique lc 3 lw 1

set key horizontal title "Wind direction (°)"
set ylabel
set y2label
set bmargin -1
set yrange [0: 360]
set y2range [0: 360]
set ytics nomirror 45
set y2tics ('N' 0, 'E' 90, 'S' 180, 'W' 270, 'N' 360)
unset grid
set boxwidth 240
plot "plot.dat" using 1:6 axes x1y1 title "" lc 2 lw 2 pt 2 with points

set key horizontal title "Rainfall (mm)"
set ylabel "hourly"
set y2label "total"
set bmargin -1
set yrange [*:*]
unset y2tics; set ytics mirror autofreq
unset grid
set boxwidth 2800
plot "plot.dat" using 1:8 axes x1y1 title "Hourly" smooth unique lc 5 lw 0, \
 "plot.dat" using 1:9 axes x1y2 title "Total" smooth unique lc 3 lw 1

set key horizontal title ""
set ylabel
set y2label
set xlabel "Time (UTC)"
set bmargin -1
set yrange [*:*]
unset y2tics; set ytics mirror autofreq
unset grid
set boxwidth 2800
plot  "plot.dat" using 1:10 axes x1y1 title "Pressure (hPa)" smooth unique lc 2 lw 1
