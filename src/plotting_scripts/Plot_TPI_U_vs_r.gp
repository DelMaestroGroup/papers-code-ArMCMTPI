set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set output 'MCM_and_ArMCM_TPI_with_fit_at_4K.tex'

set multiplot
#########################################################
set lmargin at screen 0.145
set rmargin at screen 0.985
set tmargin at screen 0.97
set bmargin at screen 0.15

set key samplen 2 spacing 0.9 at 9.2,90
set xr [0:17.0]
set yr [-80:100]

set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $2$' 2,'\fontsize{8}{8} $4$' 4,'\fontsize{8}{8} $6$' 6,'\fontsize{8}{8} $8$' 8,'\fontsize{8}{8} $10$' 10,'\fontsize{8}{8} $12$' 12,'\fontsize{8}{8} $14$' 14,'\fontsize{8}{8} $16$' 16, '\fontsize{8}{8} $18$' 18,'\fontsize{8}{8} $20$' 20) offset -0.7,0.4

set ytics ('\fontsize{8}{8} $-100$' -100,'\fontsize{8}{8} $-75$' -75, '\fontsize{8}{8} $-50$' -50, '\fontsize{8}{8} $-25$' -25, '\fontsize{8}{8} $0$' 0, '\fontsize{8}{8} $25$' 25, '\fontsize{8}{8} $50$' 50, '\fontsize{8}{8} $75$' 75, '\fontsize{8}{8} $100$' 100) offset 0.45,0

set xlabel '\fontsize{8}{8} $r$ [\AA]' offset 0,1
set ylabel '\fontsize{8}{8} $\,\overline{\!U}(r)/k_B$ [K]' offset 5.5,0

set label 1 '\scalebox{0.8}{$T=4$K}' at 4,25
set xzeroaxis lw 3 lt 1 dt 3 lc rgb 'black'

plot "../../data/lammps/TPI_data/He_TPI_U_vs_r_MCM.dat" u 1:2 w l lw 4 lt 1 lc rgb 'dark-green' ti 'MCM', "../../data/lammps/TPI_data/multisnapseed_data/He_TPI_U_vs_r_avg_werr.dat" u 1:2:4 w yerrorbars ps 0.7 pt 7 lt 1 lw 3 lc rgb 'blue' ti 'Ar+MCM', "../../data/lammps/TPI_data/multisnapseed_data/He_TPI_U_vs_r_avg_werr.dat" u 1:2 w l lw 3 lt 1 lc rgb 'blue' ti '', "../../data/lammps/TPI_data/multisnapseed_data/Ueff_fit_sigma_free_scan.dat" u 1:2 w l lw 4 lt 1 dt 3 lc rgb 'red' ti 'Potential fit'

#############################################################
unset multiplot
