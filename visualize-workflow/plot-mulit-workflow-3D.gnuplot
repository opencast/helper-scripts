# Opencast Visualize Workflow Help utilities
# This is a Demo of 3D plotting multiple instances of workflows with the same set of operations
# Requires gnuplot 5.5+ for 3D charting
# Based on 3D bar chart demo from http://gnuplot.sourceforge.net/demo_5.3/boxes3d.6.gnu
# One of many future TODOs:
# Conditionally label large operation times (aka '' using 0:3:5 with labels offset 0,0.5 notitle)

set terminal svg size 1600,900 font "arial,10" fontscale 1.5 #size 1600, 800
set output 'workflows-3D.svg'

set boxwidth 0.5
set boxdepth 0.3
set style fill  solid 1.00 border
set grid nopolar

set grid xtics nomxtics ytics nomytics ztics nomztics nortics nomrtics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics

set style fill solid 1.0 border -1
set xlabel "Wf Ops" offset -5, -3
set ylabel "Workflows"
set zlabel "Op Time [s]" offset -6,1

# Expects workflow data files to be named "workflow<n>.dat", incremented 1-N

WF_COUNT = 3
file(n) = sprintf("workflow%d.dat",n)

# Limit one label-key for each workflow file (not one for each wf-op block)
getTitle(col,f) = col == 1 ? file(f) : ""

set xtics offset 0, -0.5
set ytics offset 0, -0.5
set grid vertical layerdefault   lt 0 linecolor 0 linewidth 1.000,  lt 0 linecolor 0 linewidth 1.000
set wall z0  fc  rgb "slategrey"  fillstyle  transparent solid 0.50 border lt -1
set view 50, 72, 1.1, 1 # rotated to prevent long wf operation names from overlapping
set style data lines
set xyplane at 0
set title "Workflow Operation Times"
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set yrange [0: WF_COUNT + 1]
set y2range [ * : * ] noreverse writeback
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback
set pm3d depthorder base
set pm3d interpolate 1,1 flush begin noftriangles border linewidth 1.000 dashtype solid corners2color mean
set pm3d lighting primary 0.5 specular 0.2 spec2 0
NO_ANIMATION = 1

# Plot expects first column of input to be wf-op names, third column to be time in seconds of the operation
splot for [f=1:WF_COUNT] for [col=1:3] file(f) using 0:(f):3:xticlabels(1) with boxes lt f+1 title getTitle(col,f),

