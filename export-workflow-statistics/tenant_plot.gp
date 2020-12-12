set terminal pdf size 6,4
set output 'tenant_plot.pdf'
set title "Processed Recordings per Week and Tenant"
set xlabel "Calendar Week"
set ylabel "Amount of Processed Recordings per Week"
set key outside

file_names = system("cat filenames.txt")
nr_files = words(file_names)

tenant(file_name)=sprintf("%s",substr(file_name,19,strlen(file_name)-24))

hue(i)=(i*1.0)/nr_files
light(i)=(nr_files-(i*0.5))/nr_files

plot for [i=1:nr_files] word(file_names, i) with lines title tenant(word(file_names, i)) \
#  lc rgbcolor hsv2rgb(hue(i),1.0,light(i))