gnuplot Plot_uptake.gp
pdflatex Avg_uptake_vs_PoverP0.tex
pdftoppm -r 500 -png Avg_uptake_vs_PoverP0.pdf Avg_uptake_vs_PoverP0
mv Avg_uptake_vs_PoverP0-1.png Avg_uptake_vs_PoverP0.png

gnuplot Plot_combined_rho_rad.gp
pdflatex Combined_radial_density.tex
pdftoppm -r 500 -png Combined_radial_density.pdf Combined_radial_density
mv Combined_radial_density-1.png Combined_radial_density.png

gnuplot Plot_gr_vs_r.gp
pdflatex PC_vs_r.tex
pdftoppm -r 500 -png PC_vs_r.pdf PC_vs_r
mv PC_vs_r-1.png PC_vs_r.png

gnuplot Plot_Sq_tot_multiseed.gp
pdflatex Sq_tot_vs_q_symmNorm.tex
pdftoppm -r 500 -png Sq_tot_vs_q_symmNorm.pdf Sq_tot_vs_q_symmNorm
mv Sq_tot_vs_q_symmNorm-1.png Sq_tot_vs_q_symmNorm.png

gnuplot Plot_N1_N2_vs_mu.gp
pdflatex N1_N2_vs_mu_with_fits.tex
pdftoppm -r 500 -png N1_N2_vs_mu_with_fits.pdf N1_N2_vs_mu_with_fits
mv N1_N2_vs_mu_with_fits-1.png N1_N2_vs_mu_with_fits.png

gnuplot Plot_dN1_dN2_vs_mu.gp
pdflatex dN1_dN2_vs_mu.tex
pdftoppm -r 500 -png dN1_dN2_vs_mu.pdf dN1_dN2_vs_mu
mv dN1_dN2_vs_mu-1.png dN1_dN2_vs_mu.png

gnuplot Plot_TPI_heatmap.gp
pdflatex TPI_heatmap_at_4K.tex
pdftoppm -r 800 -png TPI_heatmap_at_4K.pdf TPI_heatmap_at_4K
mv TPI_heatmap_at_4K-1.png TPI_heatmap_at_4K.png

gnuplot Plot_TPI_U_vs_r.gp
pdflatex MCM_and_ArMCM_TPI_with_fit_at_4K.tex
pdftoppm -r 500 -png MCM_and_ArMCM_TPI_with_fit_at_4K.pdf MCM_and_ArMCM_TPI_with_fit_at_4K
mv MCM_and_ArMCM_TPI_with_fit_at_4K-1.png MCM_and_ArMCM_TPI_with_fit_at_4K.png

gnuplot 
pdflatex Screening_plot.tex
pdftoppm -r 500 -png Screening_plot.pdf Screening_plot
mv Screening_plot-1.png Screening_plot.png


rm *.eps
rm *.log
rm *.aux
rm *.tex
rm *.pdf

mv *.png ../../figures/lammps/
