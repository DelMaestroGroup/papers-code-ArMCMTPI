set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set border back
set output 'PC_vs_r.tex'

set multiplot
#########################################################
set lmargin at screen 0.10
set rmargin at screen 0.96
set tmargin at screen 0.96
set bmargin at screen 0.15

set key samplen 1 spacing 0.9 at 20,4.5
set xr [0:35]
set yr [0:5]

set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $5$' 5,'\fontsize{8}{8} $10$' 10,'\fontsize{8}{8} $15$' 15,'\fontsize{8}{8} $20$' 20,'\fontsize{8}{8} $25$' 25,'\fontsize{8}{8} $30$' 30,'\fontsize{8}{8} $35$' 35) offset -0.2,0.4

set ytics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $1$' 1, '\fontsize{8}{8} $2$' 2, '\fontsize{8}{8} $3$' 3, '\fontsize{8}{8} $4$' 4, '\fontsize{8}{8} $5$' 5) offset 0.45,0

set arrow nohead from 1,1 to 34,1 lt 1 dt 3 lw 3 lc rgb 'black'

set xlabel '\fontsize{8}{8} $r$ [\AA]' offset -1,1
set ylabel '\fontsize{8}{8} $g(r)$' offset 5,0

plot "../../data/lammps/Ar_dumpfiles/gr_cyl_mu-11.45_seedavg.dat" u 1:2 w l lw 4 lt 1 lc rgb 'magenta' ti '', "" u 1:2:3 w yerrorbars ps 0.6 pt 6 lw 2 lt 1 lc rgb 'magenta' ti '\scalebox{0.7}{Ar-Ar: Cylindrical}'

#############################################################
unset multiplot

