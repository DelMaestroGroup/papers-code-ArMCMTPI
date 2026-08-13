import numpy as np

#infiles:
rtz_file = "He_TPI_full_rtz_bareMCM.dat"
ur_file  = "He_TPI_U_vs_r_bareMCM.dat"

#outfile
out_file = "bareMCM_RMS_corrugration.dat"

#loading inputs:
#rtz format=[r(A), theta(rad), z(A); U(K)]
# ------------------------------------------------------------------
data = np.loadtxt(rtz_file)

r_all = data[:, 0]
U_all = data[:, 3]

#ur format=[r(A); Ubar(K)]
radial_data = np.loadtxt(ur_file)
r_ref = radial_data[:, 0]
U_ref = radial_data[:, 1]

#identfying unique radial points in rtz file
r_values = np.unique(r_all)

U_mean = []
sigma_corr = []

for r in r_values:
    #all U(r,theta,z) values at this radius
    mask = np.isclose(r_all, r, rtol=0.0, atol=1.0e-10)
    U = U_all[mask]

    #<U(r,theta,z)>_{theta,z}
    Ubar = np.mean(U)

    #sigma_corr(r) = sqrt( < [U(r,theta,z) - <U>]^2 >_{theta,z} )
    sigma = np.sqrt(np.mean((U - Ubar)**2))

    U_mean.append(Ubar)
    sigma_corr.append(sigma)

U_mean = np.array(U_mean)
sigma_corr = np.array(sigma_corr)

max_diff = np.max(np.abs(U_mean - U_ref))
print(f"Maximum difference from supplied U(r): {max_diff:.6e} K")

# r(A), <U>_{theta,z}(K), sigma_corr(K)
output = np.column_stack((r_values, U_mean, sigma_corr))
np.savetxt(out_file,output,header="r_A Umean_K sigma_corr_K",fmt="%.12f")

#radial adsorption minimum
imin = np.argmin(U_mean)

print(f"r_min = {r_values[imin]:.6f} A")
print(f"U(r_min) = {U_mean[imin]:.6f} K")
print(f"sigma_corr(r_min) = {sigma_corr[imin]:.6f} K")

