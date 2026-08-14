import glob
import re
import numpy as np

infile = "zval_*/data_z*_rtz.dat"
outfile = "He_TPI_U_vs_r.dat"
nr = 200
ntheta = 144

def zkey(fname):
    m = re.search(r"data_z(\d+)_rtz\.dat$", fname)
    return int(m.group(1)) if m else 10**9

files = sorted(glob.glob(infile), key=zkey)

# read first file as reference
ref = np.loadtxt(files[0], comments="#")

r_ref = ref[:, 0].reshape(nr, ntheta)
theta_ref = ref[:, 1].reshape(nr, ntheta)
usum = ref[:, 3].reshape(nr, ntheta).copy()

# accumulate remaining files
for f in files[1:]:
    arr = np.loadtxt(f, comments="#")
    if arr.shape != ref.shape:
        raise RuntimeError(f"Shape mismatch in {f}")

    r_arr = arr[:, 0].reshape(nr, ntheta)
    theta_arr = arr[:, 1].reshape(nr, ntheta)
    usum += arr[:, 3].reshape(nr, ntheta)

# average over z
uavg_z = usum / len(files)

# average over theta
ur = np.mean(uavg_z, axis=1)

# representative r for each ring
rvals = np.mean(r_ref, axis=1)

# write output
with open(outfile, "w") as out:
    out.write("# r(A) U(r)_K\n")
    for r, u in zip(rvals, ur):
        out.write(f"{r:.12f} {u:.12f}\n")
