set terminal epslatex size 2.427,1.5 standalone color colortext 8
set border linewidth 3.25
set output 'N1_N2_vs_mu_with_fits.tex'

set multiplot
#########################################################
set lmargin at screen 0.135
set rmargin at screen 0.97
set tmargin at screen 0.97
set bmargin at screen 0.15

set key samplen 0.7 spacing 0.9 at -14.8,480
set xr [-17:-9.9]
set yr [0:505]

set xtics ('\fontsize{8}{8} $-17$' -17,'\fontsize{8}{8} $-16$' -16,'\fontsize{8}{8} $-15$' -15,'\fontsize{8}{8} $-14$' -14,'\fontsize{8}{8} $-13$' -13,'\fontsize{8}{8} $-12$' -12,'\fontsize{8}{8} $-11$' -11,'\fontsize{8}{8} $-10$' -10,'\fontsize{8}{8} $-9$' -9) offset -0.7,0.4

set ytics ('\fontsize{8}{8} $0$' 0,'\fontsize{8}{8} $100$' 100, '\fontsize{8}{8} $200$' 200, '\fontsize{8}{8} $300$' 300, '\fontsize{8}{8} $400$' 400, '\fontsize{8}{8} $500$' 500) offset 0.45,0

set xlabel '\fontsize{8}{8} $\mu$ [kJ/mol]' offset 0,1
set ylabel '\fontsize{8}{8} $N_l(\mu)$' offset 5.5,0

#set arrow nohead from -11.80,0.00 to -11.50,0.03 lt 1 dt 3 lw 3 lc rgb 'dark-green'
#set label 1 '\scalebox{0.5}{$\mu=-11.50$}' at -12.00,0.021 rotate by 90

# --------------------------------------------------
# Smooth sigmoid fits
# N1(x) = c1 + L1 / (1 + exp[-k1*(x-mu1)])
# N2(x) = c2 + L2 / (1 + exp[-k2*(x-mu2)])
# --------------------------------------------------

c1  = 17.92
L1  = 494.03
k1  = 1.356
mu1 = -12.268

c2  = -0.503
L2  = 340.59
k2  = 1.749
mu2 = -10.987

N1(x) = c1 + L1/(1.0 + exp(-k1*(x - mu1)))
N2(x) = c2 + L2/(1.0 + exp(-k2*(x - mu2)))

plot "../../data/lammps/Ar_dumpfiles/monolayer_analysis.txt" u 1:2 w l lw 4 lt 1 lc rgb 'blue' ti '\fontsize{6}{6} $N_1(\mu)$',"" u 1:3 w l lw 4 lt 1 lc rgb 'red' ti '\fontsize{6}{6} $N_2(\mu)$',N1(x) w l lw 4 dt 3 lc rgb 'black' notitle,N2(x) w l lw 4 dt 3 lc rgb 'black'  notitle

#############################################################
unset multiplot

