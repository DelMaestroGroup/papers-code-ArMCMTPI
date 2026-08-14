import numpy as np

ar_file   = "RMS_ArMCM_5seed_average.dat"
bare_file = "bareMCM_RMS_corrugration.dat"
out_file = "Screening_factor_vs_relative_r.dat"

#interval range of screening:
xmin = -5.0
xmax =  1.0

ar = np.loadtxt(ar_file)    #format: r  Umean   sigma_corr_mean sigma_corr_SD sigma_corr_SEM
r_ar       = ar[:, 0]
U_ar       = ar[:, 1]
sigma_ar   = ar[:, 2]
sigma_sem  = ar[:, 3]

bare = np.loadtxt(bare_file)#format: r  Umean   sigma_corr
r_bare     = bare[:, 0]
U_bare     = bare[:, 1]
sigma_bare = bare[:, 2]

#identifying minimas of both datasets:
i_ar_min   = np.argmin(U_ar)
i_bare_min = np.argmin(U_bare)

rmin_ar   = r_ar[i_ar_min]
rmin_bare = r_bare[i_bare_min]

print(f"Ar/MCM r_min   = {rmin_ar:.10f} A")
print(f"bareMCM r_min = {rmin_bare:.10f} A")

#Relative coordinates:
x_ar   = r_ar   - rmin_ar
x_bare = r_bare - rmin_bare

mask = (x_ar >= xmin) & (x_ar <= xmax)

x = x_ar[mask]

sigma_ar_use  = sigma_ar[mask]
sigma_sem_use = sigma_sem[mask]

sigma_bare_use = np.interp(x, x_bare, sigma_bare)

# calculating the screening factor: S(dr)= 1-sigma_ArMCM(dr)/sigma_bareMCM(dr)
S = 1.0 - sigma_ar_use / sigma_bare_use
S_SEM = sigma_sem_use / sigma_bare_use

output = np.column_stack((x,sigma_ar_use,sigma_bare_use,S,S_SEM))
np.savetxt(out_file,output,header=("delta_r_A sigma_ArMCM sigma_bareMCM Sc Sc_SEM"),fmt="%.10f")
