import numpy as np

nseeds = 5
data = []
for seed in range(1, nseeds + 1):
    fname = f"Seed_{seed}/Navg_uptake_vs_mu_seed{seed}.dat"
    arr = np.loadtxt(fname, comments="#")
    data.append(arr)

#fixing mu and P/P0
mu_P = data[0][:, 0:2]

N_all = np.column_stack([data[seed][:, 2] for seed in range(nseeds)])
uptake_all = np.column_stack([data[seed][:, 3] for seed in range(nseeds)])

Nmean = np.mean(N_all, axis=1)
Nse = np.std(N_all, axis=1, ddof=1) / np.sqrt(nseeds)

uptake_mean = np.mean(uptake_all, axis=1)
uptake_se = np.std(uptake_all, axis=1, ddof=1) / np.sqrt(nseeds)

avg_output = np.column_stack([mu_P,Nmean,Nse,uptake_mean,uptake_se])

header_avg = "mu P_by_P0 Nmean Nse uptake_mean uptake_se"
np.savetxt("Navg_uptake_seedavg.dat",avg_output,header=header_avg,fmt="%.10e")
