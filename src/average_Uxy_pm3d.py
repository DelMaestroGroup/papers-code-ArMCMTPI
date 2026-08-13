import glob
import re
import numpy as np

pattern = "He_TPI_xy_pm3d_seed*_snap*.dat"
outfile_mean = "He_TPI_xy_pm3d_avg.dat"
outfile_err  = "He_TPI_xy_pm3d_var_stderr.dat"
ntheta = 145   # change if needed

def file_key(fname):
    m = re.search(r"seed(\d+)_snap(\d+)", fname)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (10**9, 10**9)

files = sorted(glob.glob(pattern), key=file_key)

if not files:
    raise RuntimeError("No pm3d files found.")

data = []
x_ref = None
y_ref = None

for f in files:
    arr = np.loadtxt(f, comments="#")
    if arr.shape[1] < 3:
        raise RuntimeError(f"{f} does not have at least 3 columns")

    x = arr[:, 0]
    y = arr[:, 1]
    u = arr[:, 2]

    if x_ref is None:
        x_ref = x.copy()
        y_ref = y.copy()
    else:
        if arr.shape[0] != len(x_ref):
            raise RuntimeError(f"Row count mismatch in {f}")
        if not (np.allclose(x, x_ref) and np.allclose(y, y_ref)):
            raise RuntimeError(f"(x,y) grid mismatch in {f}")

    data.append(u)

data = np.array(data)   # shape = (nfiles, npts)
nfiles = data.shape[0]

u_mean = np.mean(data, axis=0)
u_var  = np.var(data, axis=0, ddof=1)
u_se   = np.sqrt(u_var / nfiles)

# ---- mean file for pm3d plotting ----
with open(outfile_mean, "w") as out:
    out.write("# x(A) y(A) Uavgz(K)\n")
    for i, (x, y, u) in enumerate(zip(x_ref, y_ref, u_mean), start=1):
        out.write(f"{x:.10f} {y:.10f} {u:.10f}\n")
        if i % ntheta == 0:
            out.write("\n")

# ---- separate variance + stderr file ----
with open(outfile_err, "w") as out:
    out.write("# x(A) y(A) variance(K^2) stderr(K)\n")
    for i, (x, y, v, s) in enumerate(zip(x_ref, y_ref, u_var, u_se), start=1):
        out.write(f"{x:.10f} {y:.10f} {v:.10f} {s:.10f}\n")
        if i % ntheta == 0:
            out.write("\n")

print(f"Wrote {outfile_mean} using {nfiles} files.")
print(f"Wrote {outfile_err} using {nfiles} files.")
