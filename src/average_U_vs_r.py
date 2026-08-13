import glob
import re
import numpy as np

pattern = "He_TPI_U_vs_r_seed*_snap*.dat"
outfile = "He_TPI_U_vs_r_avg_werr.dat"

def file_key(fname):
    m = re.search(r"seed(\d+)_snap(\d+)", fname)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (10**9, 10**9)

files = sorted(glob.glob(pattern), key=file_key)

if not files:
    raise RuntimeError("No U_vs_r files found.")

data = []
r_ref = None

for f in files:
    arr = np.loadtxt(f, comments="#")
    if arr.shape[1] < 2:
        raise RuntimeError(f"{f} does not have at least 2 columns")

    r = arr[:, 0]
    u = arr[:, 1]

    if r_ref is None:
        r_ref = r.copy()
    else:
        if arr.shape[0] != len(r_ref):
            raise RuntimeError(f"Row count mismatch in {f}")
        if not np.allclose(r, r_ref):
            raise RuntimeError(f"r-grid mismatch in {f}")

    data.append(u)

data = np.array(data)   # shape = (nfiles, nr)
nfiles = data.shape[0]

u_mean = np.mean(data, axis=0)
u_var  = np.var(data, axis=0, ddof=1)
u_se   = np.sqrt(u_var / nfiles)

out = np.column_stack((r_ref, u_mean, u_var, u_se))
header = "r(A) Uavg(K) variance(K^2) stderr(K)"
np.savetxt(outfile, out, header=header)

