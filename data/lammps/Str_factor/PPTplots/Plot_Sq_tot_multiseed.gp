set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set output 'Sq_tot_vs_q_exp_ArAr.tex'

set multiplot
#########################################################
set lmargin at screen 0.13
set rmargin at screen 0.98
set tmargin at screen 0.97
set bmargin at screen 0.15

set key samplen 1 spacing 0.9 at 7,2.8
set xr [1:7]
set yr [0:3.0]

set xtics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $1$' 1,'\fontsize{8}{8} $2$' 2,'\fontsize{8}{8} $3$' 3,'\fontsize{8}{8} $4$' 4,'\fontsize{8}{8} $5$' 5,'\fontsize{8}{8} $6$' 6,'\fontsize{8}{8} $7$' 7) offset -0.2,0.4

set ytics ('\fontsize{8}{8} $0.0$' 0.0,'\fontsize{8}{8} $0.5$' 0.5, '\fontsize{8}{8} $1.0$' 1.0, '\fontsize{8}{8} $1.5$' 1.5, '\fontsize{8}{8} $2.0$' 2.0, '\fontsize{8}{8} $2.5$' 2.5, '\fontsize{8}{8} $3.0$' 3.0) offset 0.45,0

set arrow nohead from 1,1 to 7,1 lt 1 dt 3 lw 3 lc rgb 'black'

set xlabel '\fontsize{8}{8} $q$ [\AA$^{-1}$]' offset -1,1
set ylabel '\fontsize{8}{8} $S(q)$' offset 6,0

plot "../Sq_exp_k1.71.txt" u 1:2 w lp ps 0.9 pt 7 lt 1 dt 3 lw 2 lc rgb '#FE9A37' ti '\scalebox{0.7}{Exp. $k_{i}=1.71$\AA$^{-1}$}',"../Sq_exp_k2.5.txt" u 1:2 w lp ps 1.0 pt 5 lt 1 dt 3 lw 2 lc rgb '#2984D1' ti '\scalebox{0.7}{Exp. $k_{i}=2.5$\AA$^{-1}$}', "../Sq_exp_k4.0.txt" u 1:2 w lp ps 1.2 pt 9 lt 1 dt 3 lw 2 lc rgb 'brown' ti '\scalebox{0.7}{Exp. $k_{i}=4.0$\AA$^{-1}$}',"<paste ../New_debye_Sq_vs_q_seed1_symm_avgd_Rc_22.5.txt ../New_debye_Sq_vs_q_seed2_symm_avgd_Rc_22.5.txt ../New_debye_Sq_vs_q_seed3_symm_avgd_Rc_22.5.txt ../New_debye_Sq_vs_q_seed4_symm_avgd_Rc_22.5.txt ../New_debye_Sq_vs_q_seed5_symm_avgd_Rc_22.5.txt" u 1:(0.2*(($10)+($27)+($44)+($61)+($78))) w l lw 4 lt 1 lc rgb 'magenta' ti '\scalebox{0.7}{Ar-Ar}'
#,"../Debye_Sq_vs_q_5seed_average_Rc_22.5.txt" u 1:2 w l lw 3 lt 1 lc rgb 'dark-green' ti '',"" u 1:2:3 w yerrorbars ps 0.4 pt 6 lw 2 lt 1 lc rgb 'dark-green' ti '\scalebox{0.7}{Ar-Ar + Ar-MCM}'


#############################################################
unset multiplot
