set terminal pngcairo size 640,480
set output "ALL-Sparse-SPC-By-avg.png"

set xlabel		'Average degree' font "Tahoma,14" offset 0,1
set ylabel		'Specificity' font "Tahoma,14" offset 2.5,0

set xrange [5.5:15.5]
set yrange [0:100]

set xtics rotate by 45 offset -0.8,-0.5 font "Tahoma,14"
set ytics 10 font "Tahoma,14"
set key font "Tahoma,14" out hori right top


set style line 1 lt 1 lc rgb "#A00000" lw 2 pt 0
set style line 2 lt 1 lc rgb "#00A000" lw 2 pt 12
set style line 3 lt 1 lc rgb "#5060D0" lw 2 pt 1
set style line 4 lt 1 lc rgb "#0000A0" lw 2 pt 2
set style line 5 lt 1 lc rgb "#00D0D0" lw 2 pt 8
set style line 6 lt 1 lc rgb "#D0D000" lw 2 pt 3
set style line 7 lt 1 lc rgb "#B200B2" lw 2 pt 10
set style line 8 lt 1 lc rgb "#ffb100" lw 2 pt 4
set style line 9 lt 1 lc rgb "#ff0694" lw 2 pt 5
set style line 10 lt 1 lc rgb "#fafe04" lw 2 pt 6

plot\
"DH-SPC-By-avg.txt"			w lp ls 1 title 'DH', \
"FA2-SPC-By-avg.txt"		w lp ls 2 title 'FA2', \
"KK-W-SPC-By-avg.txt"		w lp ls 9 title 'KK-MS-DS', \
"FDGE-SPC-By-avg.txt"		w lp ls 3 title 'FDGE', \
"FRR-SPC-By-avg.txt"		w lp ls 4 title 'FRR', \
"FR-SPC-By-avg.txt"			w lp ls 5 title 'FR', \
"FRU-SPC-By-avg.txt"		w lp ls 6 title 'FRU', \
"JIGGLE-SPC-By-avg.txt"		w lp ls 7 title 'JIGGLE', \
"KK-SPC-By-avg.txt"			w lp ls 8 title 'KK', \
"LINLOG-SPC-By-avg.txt"	w lp ls 10 title 'LINLOG'
