set terminal pdf
set output 'plot.pdf'
set title "Processed Recordings per Week"
set xlabel "Calendar Week"
set ylabel "Amount of Processed Recordings per Week"
plot 'workflow-statistics.dat' w lines notitle lt rgb "red"
