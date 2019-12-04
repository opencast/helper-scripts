#set terminal svg size 1600,900
set terminal svg size 1600,900 standalone fname 'Sans bold' fsize 20 background rgb 'white'
set boxwidth 0.8
set style fill solid 1.0 border -1
set xtics rotate
set ylabel "Time [s]"
set output 'workflow.svg'
plot 'workflow.dat' using 3:xticlabels(1) with boxes lt rgb "#000000" notitle,\
  '' using 0:3:5 with labels offset 0,0.5 notitle
# Use "using 0:3:4" for percentages of the overall time
