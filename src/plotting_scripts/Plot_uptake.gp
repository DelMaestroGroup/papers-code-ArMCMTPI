set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set output 'Avg_uptake_vs_PoverP0.tex'

set multiplot
#########################################################
set lmargin at screen 0.12
set rmargin at screen 0.98
set tmargin at screen 0.97
set bmargin at screen 0.15

set key samplen 1 spacing 0.9 at 1.0,30
set xr [0:1.05]
set yr [0:*]

set xtics ('\fontsize{8}{8} $0.0$' 0.0,'\fontsize{8}{8} $0.2$' 0.2,'\fontsize{8}{8} $0.4$' 0.4,'\fontsize{8}{8} $0.6$' 0.6,'\fontsize{8}{8} $0.8$' 0.8,'\fontsize{8}{8} $1.0$' 1.0) offset -0.2,0.4

set ytics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $5$' 5, '\fontsize{8}{8} $10$' 10, '\fontsize{8}{8} $15$' 15, '\fontsize{8}{8} $20$' 20, '\fontsize{8}{8} $25$' 25, '\fontsize{8}{8} $30$' 30) offset 0.4,0

set xlabel '\fontsize{8}{8} $P/P_0$' offset 0,1
set ylabel '\fontsize{8}{8} Uptake [mmol/g]' offset 5.2,0

set label 1 '\scalebox{0.7}{uptake=$\frac{\langle N \rangle/N_A}{m_\mathrm{\scalebox{0.5}{pore}}}$}' at 0.05,27
#set label 2 '\scalebox{0.7}{$P_0=2.6$ bar}' at 0.05,24

plot "../../data/lammps/Ar_nstats/Navg_uptake_seedavg.dat" u ($2/2.6):5:6 w yerrorbars lw 2 ps 0.6 pt 6 lc rgb 'red' ti '\scalebox{0.7}{GCMC}',"" u ($2/2.6):5 w l lw 4 lc rgb 'red' noti,"../../data/lammps/Nexp_data_MCM-41_Ar.txt" u 2:1 w p ps 0.9 pt 7 lc rgb 'dark-green' ti '\scalebox{0.7}{Experiment}'



#############################################################
unset multiplot
