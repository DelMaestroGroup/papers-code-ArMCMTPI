set terminal epslatex size 2.2,1.9 standalone color colortext 8
set border linewidth 3.25
set output 'TPI_heatmap_at_4K.tex'

set multiplot
#########################################################
set lmargin at screen 0.10
set rmargin at screen 0.84
set tmargin at screen 0.98
set bmargin at screen 0.14

set key samplen 1 spacing 0.9 at 14,0.025
set xr [-20.1:20.1]
set yr [-20.1:20.1]

#set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $5$' 5,'\fontsize{8}{8} $10$' 10,'\fontsize{8}{8} $15$' 15,'\fontsize{8}{8} $20$' 20,'\fontsize{8}{8} $-5$' -5,'\fontsize{8}{8} $-10$' -10,'\fontsize{8}{8} $-15$' -15,'\fontsize{8}{8} $-20$' -20) offset -0.4,0.4

set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $10$' 10,'\fontsize{8}{8} $20$' 20,'\fontsize{8}{8} $-10$' -10, '\fontsize{8}{8} $-20$' -20) offset -0.4,0.7

set ytics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $-10$' -10,'\fontsize{8}{8} $10$' 10,'\fontsize{8}{8} $-20$' -20, '\fontsize{8}{8} $20$' 20) offset 1.0,-0.2

set xlabel '\fontsize{8}{8} $x$ [\AA]' offset 0,1.15
set ylabel '\fontsize{8}{8} $y$ [\AA]' offset 6.5,0

set pm3d map
set pm3d interpolate 0,0
set cbr [-60:220]
set palette defined (-50 'red', 0 'white', 220 'blue')

set size ratio -1
set colorbox vertical user origin 0.845,0.14 size 0.02,0.84
#set colorbox border linewidth 2.0

set cbtics ('\fontsize{6}{6} -$50$' -50,'\fontsize{6}{6} \phantom{-}$\phantom{0}0$' 0,'\fontsize{6}{6} $\phantom{0}50$' 50,'\fontsize{6}{6} $100$' 100,'\fontsize{6}{6} $150$' 150,'\fontsize{6}{6} $200$' 200) offset -1.5,0

#set label 1 '\fontsize{8}{8} ${}^{4}\mathrm{He}$ Potential [K]' at 27.5,-15 rotate by 90 front
set label 1 '\fontsize{8}{8} $\,\overline{\!U}(r,\theta) / k_B$ [K]' at 27.5,-12 rotate by 90 front

#splot "He_TPI_xy_pm3d.dat" u (($1)-42.996):(($2)-39.413):3 w pm3d ti ''

set parametric
set urange [0:2*pi]
set vrange [0:0]

splot "../../data/lammps/TPI_data/multisnapseed_data/He_TPI_xy_pm3d_avg.dat" u (($1)-42.996):(($2)-39.413):3 w pm3d notitle, 11.66*cos(u), 11.66*sin(u), 200 w l lw 2 lt 1 dt 3 lc rgb "black" ti ''

unset parametric

#############################################################
unset multiplot

