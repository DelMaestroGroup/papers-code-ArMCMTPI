set terminal epslatex size 4,3.5 standalone color colortext 8
set output 'Combined_radial_density.tex'

set border linewidth 2.75

#########################################################
set xr [0:20]
set yr [0.00:0.032]

set ytics nomirror
set xtics nomirror

set multiplot
#########################################################

set lmargin at screen 0.115
set rmargin at screen 0.54
set bmargin at screen 0.55
set tmargin at screen 0.98

set ylabel rotate by 90 '\scalebox{1.25}{$\rho_{\mathrm{rad}}(r)$ [\AA$^{-3}$]}' offset 6,0
#set ytics ('\fontsize{8}{8} $0.00$' 0.00,'\fontsize{8}{8} $0.01$' 0.01, '\fontsize{8}{8} $0.02$' 0.02, '\fontsize{8}{8} $0.03$' 0.03) offset 0.75,0

set ytics ('\scalebox{1.25}{$0.00$}' 0.0,'\scalebox{1.25}{$0.01$}' 0.01, '\scalebox{1.25}{$0.02$}' 0.02, '\scalebox{1.25}{$0.03$}' 0.03) offset 0.75,0
#set xtics ('' 0,'' 4,'' 8,'' 12,'' 16,'' 20) offset 0.0,0.0
set xtics ('' 0,'' 3,'' 6, '' 9,'' 12,'' 15,'' 18) offset 0.0,0.0

set label 1 '\scalebox{1.2}{(a)}' at 0.5,0.030
set label 2 '\scalebox{1.1}{$\mu=-14.00$ kJ/mol}' at 7,0.030

set key samplen 1 at 20,0.031

plot "../../data/lammps/Ar_dumpfiles/radial_rho_vs_r_mu-15.00_seedavg.dat" u 1:2 w l lw 5 lt 1 lc rgb 'blue' ti '',"" u 1:2:3 w yerrorbars lw 3 ps 0.6 pt 6 lc rgb 'blue' ti ''

unset label 1
unset label 2
unset ylabel 
#########################################################

set lmargin at screen 0.56
set rmargin at screen 0.985
set bmargin at screen 0.55
set tmargin at screen 0.98

set ytics ('' 0.00,'' 0.01, '' 0.02, '' 0.03) offset 0.75,0
set label 1 '\scalebox{1.2}{(b)}' at 0.5,0.030
set label 2 '\scalebox{1.1}{$\mu=-11.45$ kJ/mol}' at 7,0.030

plot "../../data/lammps/Ar_dumpfiles/radial_rho_vs_r_mu-11.45_seedavg.dat" u 1:2 w l lw 5 lt 1 lc rgb 'blue' ti '',"" u 1:2:3 w yerrorbars lw 3 ps 0.6 pt 6 lc rgb 'blue' ti ''

unset label 1
unset label 2
#########################################################

set lmargin at screen 0.115
set rmargin at screen 0.54
set bmargin at screen 0.08
set tmargin at screen 0.51

set ylabel rotate by 90 '\scalebox{1.25}{$\rho_{\mathrm{rad}}(r)$ [\AA$^{-3}$]}' offset 6,0
set xlabel '\scalebox{1.25}{$r$ [\AA]}' offset -0.3,0.75

set ytics ('\scalebox{1.25}{$0.00$}' 0.0,'\scalebox{1.25}{$0.01$}' 0.01, '\scalebox{1.25}{$0.02$}' 0.02, '\scalebox{1.25}{$0.03$}' 0.03) offset 0.75,0
#set xtics ('\scalebox{1.25}{$0$}' 0,'\scalebox{1.25}{$4$}' 4,'\scalebox{1.25}{$8$}' 8,'\scalebox{1.25}{$12$}' 12,'\scalebox{1.25}{$16$}' 16,'\scalebox{1.25}{$20$}' 20, '\scalebox{1.25}{$18$}' 18,'\scalebox{1.25}{$14$}' 14,'\scalebox{1.25}{$10$}' 10,'\scalebox{1.25}{$6$}' 6,'\scalebox{1.25}{$2$}' 2) offset 0,0.1

set xtics ('\scalebox{1.25}{$0$}' 0,'\scalebox{1.25}{$3$}' 3,'\scalebox{1.25}{$6$}' 6,'\scalebox{1.25}{$9$}' 9,'\scalebox{1.25}{$12$}' 12,'\scalebox{1.25}{$15$}' 15,'\scalebox{1.25}{$18$}' 18) offset 0,0.1

set label 1 '\scalebox{1.2}{(c)}' at 0.5,0.030
set label 2 '\scalebox{1.1}{$\mu=-10.00$ kJ/mol}' at 7,0.030

plot "../../data/lammps/Ar_dumpfiles/radial_rho_vs_r_mu-10.00_seedavg.dat" u 1:2 w l lw 5 lt 1 lc rgb 'blue' ti '',"" u 1:2:3 w yerrorbars lw 3 ps 0.6 pt 6 lc rgb 'blue' ti ''


unset label 1
unset label 2
unset ylabel
#########################################################

set lmargin at screen 0.56
set rmargin at screen 0.985
set bmargin at screen 0.08
set tmargin at screen 0.51

set ytics ('' 0.00,'' 0.01, '' 0.02, '' 0.03) offset 0.75,0
set label 1 '\scalebox{1.2}{(d)}' at 0.5,0.030
set label 2 '\scalebox{1.1}{$\mu=-9.50$ kJ/mol}' at 7.7,0.030

plot "../../data/lammps/Ar_dumpfiles/radial_rho_vs_r_mu-9.50_seedavg.dat" u 1:2 w l lw 5 lt 1 lc rgb 'blue' ti '',"" u 1:2:3 w yerrorbars lw 3 ps 0.6 pt 6 lc rgb 'blue' ti ''

unset label 1
unset label 2



unset multiplot
