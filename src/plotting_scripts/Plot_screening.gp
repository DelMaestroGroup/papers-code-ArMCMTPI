set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set output 'Screening_plot.tex'

set multiplot
#########################################################
set lmargin at screen 0.155
set rmargin at screen 0.985
set tmargin at screen 0.965
set bmargin at screen 0.15

set key samplen 2 spacing 0.9 at 9.2,90
set xr [-5.0:1.0]
set yr [0:0.35]

set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $1$' 1,'\fontsize{8}{8} $-1$' -1,'\fontsize{8}{8} $-2$' -2,'\fontsize{8}{8} $-3$' -3,'\fontsize{8}{8} $-4$' -4,'\fontsize{8}{8} $-5$' -5,'\fontsize{8}{8} $14$' 14,'\fontsize{8}{8} $16$' 16, '\fontsize{8}{8} $18$' 18,'\fontsize{8}{8} $20$' 20) offset -0.7,0.4

set ytics ('\fontsize{8}{8} $0.00$' 0.00,'\fontsize{8}{8} $0.10$' 0.10, '\fontsize{8}{8} $0.20$' 0.20, '\fontsize{8}{8} $0.30$' 0.30, '\fontsize{8}{8} $0.15$' 0.15, '\fontsize{8}{8} $0.05$' 0.05, '\fontsize{8}{8} $0.25$' 0.25, '\fontsize{8}{8} $0.35$' 0.35) offset 0.45,0

set xlabel '\fontsize{8}{8} $\Delta r$ [\AA]' offset 0,1
set ylabel '\fontsize{8}{8} $\mathcal{S}(\Delta r)$' offset 6,0

#set label 1 '\scalebox{0.8}{$T=4$K}' at 4,25
#set xzeroaxis lw 3 lt 1 dt 3 lc rgb 'black'

plot "Screening_factor_vs_relative_r.dat" u 1:4 w l lw 4 lt 1 lc rgb 'black' ti ''


#plot "He_TPI_U_vs_r_MCM.dat" u 1:2 w l lw 4 lt 1 lc rgb 'dark-green' ti 'MCM', "multisnapseed_data/He_TPI_U_vs_r_avg_werr.dat" u 1:2:4 w yerrorbars ps 0.7 pt 7 lt 1 lw 3 lc rgb 'blue' ti 'Ar+MCM', "multisnapseed_data/He_TPI_U_vs_r_avg_werr.dat" u 1:2 w l lw 3 lt 1 lc rgb 'blue' ti '', "multisnapseed_data/Ueff_fit_sigma_free_scan.dat" u 1:2 w l lw 4 lt 1 dt 3 lc rgb 'red' ti 'Potential fit'

#############################################################
unset multiplot
