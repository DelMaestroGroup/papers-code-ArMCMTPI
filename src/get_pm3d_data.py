import glob
import re
import numpy as np

# ---- settings ----
infile = "zval_*/data_z*_xyz.dat"
outfile = "He_TPI_xy_pm3d.dat"
ntheta = 144

def zkey(fname):
    m = re.search(r"data_z(\d+)_xyz\.dat$", fname)
    return int(m.group(1)) if m else 10**9

files = sorted(glob.glob(infile), key=zkey)

# read first file as reference
ref = np.loadtxt(files[0], comments="#")
x = ref[:, 0]
y = ref[:, 1]
usum = ref[:, 3].copy()

# accumulate remaining files
for f in files[1:]:
    arr = np.loadtxt(f, comments="#")
    if arr.shape != ref.shape:
        raise RuntimeError(f"Shape mismatch in {f}")

    usum += arr[:, 3]

uavg = usum / len(files)

with open(outfile, "w") as out:
    out.write("# x(A) y(A) Uavgz_K\n")
    for i, (xi, yi, ui) in enumerate(zip(x, y, uavg), start=1):
        out.write(f"{xi:.13f} {yi:.13f} {ui:.15f}\n")
        if i % ntheta == 0:
            out.write("\n")
