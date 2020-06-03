set terminal pngcairo size 640,480
set output "ALL-Uniform-SPC-By-avg.png"

set xlabel		'Average degree' font "Tahoma,14" offset 0,1
set ylabel		'Specificity' font "Tahoma,14" offset 2.5,0

set xrange [5.5:15.5]
set yrange [0:100]

set xtics rotate by 45 offset -0.8,-0.5 font "Tahoma,14"
set ytics 10 font "Tahoma,14"
set key font "Tahoma,14" out hori right top


set style line 1 lt 1 lc rgb "#A00000" lw 2 pt 0

plot\
"GT-SPC-By-avg.txt"			w lp ls 1 title 'Ground Truth'
