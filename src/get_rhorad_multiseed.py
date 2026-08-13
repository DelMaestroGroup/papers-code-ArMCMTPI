import re
import glob
import numpy as np

nseeds = 5
mu_read = re.compile(r"radial_rho_vs_r_mu(-?\d+(?:\.\d+)?)\.dat$")

def get_mu(fname):
    return float(mu_read.search(fname).group(1))

files = sorted(glob.glob("Seed_1/radial_rho_vs_r_mu*.dat"),key=get_mu)

for file1 in files:
    mu = get_mu(file1)
    data = []
    for seed in range(1,nseeds + 1):
        fname = (f"Seed_{seed}/"f"radial_rho_vs_r_mu{mu:.2f}.dat")
        arr = np.loadtxt(fname,comments="#")
        data.append(arr)


    r = data[0][:, 0]
    rho_all = np.column_stack([data[seed][:, 1] for seed in range(nseeds)])
    counts_all = np.column_stack([data[seed][:, 2] for seed in range(nseeds)])

    rho_mean = np.mean(rho_all,axis=1)
    rho_se = (np.std(rho_all,axis=1,ddof=1)/np.sqrt(nseeds))
    counts_mean = np.mean(counts_all,axis=1)

    avg_output = np.column_stack([r,rho_mean,rho_se,counts_mean])
    outfile = (f"radial_rho_vs_r_mu{mu:.2f}_seedavg.dat")
    header = ("r_center(A) rho_mean(A^-3) rho_se(A^-3) counts_mean")
    
    np.savetxt(outfile,avg_output,header=header,fmt="%.10e")

