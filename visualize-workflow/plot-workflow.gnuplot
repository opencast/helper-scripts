# Plot individual Workflow Operation Charts
# Change WF_COUNT to the number of workflows to process
# Expects workflow data files to be named "workflow<n>.dat", incremented 1-N

WF_COUNT = 1
file(n) = sprintf("workflow%d.dat",n)

set terminal svg size 1600,WF_COUNT * 900 font "Sans bold, 20" background rgb 'white'
set output 'workflow.svg'


set multiplot layout WF_COUNT, 1

set boxwidth 0.8
set style fill solid 1.0 border -1
set xtics rotate
set ylabel "Time [s]"

do for [f=1:WF_COUNT] {
  set title "Workflow Operation Times from ".file(f)
  plot file(f) using 3:xticlabels(1) with boxes lt rgb "#000000" notitle,\
    '' using 0:3:5 with labels offset 0,0.5 notitle
  # Use "using 0:3:4" for percentages of the overall time
}

unset multiplot
