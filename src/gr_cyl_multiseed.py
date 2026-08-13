import argparse
from pathlib import Path
import numpy as np

#Pore geometry
X0_DEFAULT = 42.996
Y0_DEFAULT = 39.413
R_DEFAULT  = 21.0


def wrapped_dz(dz, Lz):
    """Minimum-image z separation for z-periodic boundary condition."""
    return dz - Lz*np.rint(dz/Lz)


def parse_lammps_frames_ar_only(path):
    """Parsing Ar-only LAMMPS dump: columns include id type x y z."""
    frames = []

    with open(path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if not line.startswith("ITEM: TIMESTEP"):
                raise RuntimeError(f"Unexpected dump format in {path}: missing TIMESTEP")

            ts = int(f.readline().strip())

            line = f.readline()
            assert line.startswith("ITEM: NUMBER OF ATOMS")
            n = int(f.readline().strip())

            line = f.readline()
            assert line.startswith("ITEM: BOX BOUNDS")
            xlo, xhi = map(float, f.readline().split()[:2])
            ylo, yhi = map(float, f.readline().split()[:2])
            zlo, zhi = map(float, f.readline().split()[:2])

            line = f.readline()
            assert line.startswith("ITEM: ATOMS")
            cols = line.split()[2:]
            col = {name: i for i, name in enumerate(cols)}

            xyz = np.empty((n, 3), float)
            for i in range(n):
                parts = f.readline().split()
                xyz[i, 0] = float(parts[col["x"]])
                xyz[i, 1] = float(parts[col["y"]])
                xyz[i, 2] = float(parts[col["z"]])

            frames.append((ts, xyz, (xlo, xhi, ylo, yhi, zlo, zhi)))

    return frames


def select_in_cylinder(xyz, x0, y0, R):
    if xyz.shape[0] == 0:
        return xyz

    dx = xyz[:, 0] - x0
    dy = xyz[:, 1] - y0
    return xyz[(dx*dx + dy*dy) <= (R*R)]


def pair_histogram(xyz, Lz, r_edges):
    """Histogram all i<j pair distances with periodic wrapping along z only."""
    N = xyz.shape[0]
    if N < 2:
        return np.zeros(len(r_edges)-1, dtype=float)

    iu, ju = np.triu_indices(N, k=1)

    dx = xyz[iu, 0] - xyz[ju, 0]
    dy = xyz[iu, 1] - xyz[ju, 1]
    dz = wrapped_dz(xyz[iu, 2] - xyz[ju, 2], Lz)

    r = np.sqrt(dx*dx + dy*dy + dz*dz)
    hist, _ = np.histogram(r, bins=r_edges)
    return hist.astype(float)


def sample_uniform_cylinder(N, x0, y0, R, zlo, zhi, rng):
    """Generating N ideal-gas reference particles uniformly in the cylinder."""
    u = rng.random(N)
    r = R*np.sqrt(u)
    theta = 2.0*np.pi*rng.random(N)

    x = x0 + r*np.cos(theta)
    y = y0 + r*np.sin(theta)
    z = zlo + (zhi - zlo)*rng.random(N)

    return np.column_stack([x, y, z])


def compute_gr_for_dump(path, x0, y0, R, r_edges, nref, rng):
    """Computing one seed-averaged cylinder-corrected g(r) from one dump file."""
    frames = parse_lammps_frames_ar_only(path)
    if not frames:
        raise RuntimeError(f"No frames found in {path}")

    nbins = len(r_edges) - 1
    H_data = np.zeros(nbins, float)
    H_ref = np.zeros(nbins, float)
    used = 0

    for ts, xyz, bounds in frames:
        xlo, xhi, ylo, yhi, zlo, zhi = bounds
        Lz = zhi - zlo

        # Keep only particles in the cylindrical pore region.
        xyz_in = select_in_cylinder(xyz, x0, y0, R)
        N = xyz_in.shape[0]
        if N < 2:
            continue

        H_data += pair_histogram(xyz_in, Lz, r_edges)

        # Ideal-gas normalization with same N and same cylinder geometry.
        for _ in range(nref):
            xyz_rand = sample_uniform_cylinder(N, x0, y0, R, zlo, zhi, rng)
            H_ref += pair_histogram(xyz_rand, Lz, r_edges)

        used += 1

    if used == 0:
        raise RuntimeError(f"No usable frames with N>=2 in {path}")

    H_data /= used
    H_ref /= (used*nref)

    eps = 1.0e-12
    g = H_data / np.maximum(H_ref, eps)

    return g, H_data, H_ref, used


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, default=-11.45,
                    help="Chemical potential to analyze in kJ/mol. Default: -11.45")
    ap.add_argument("--nseeds", type=int, default=5)
    ap.add_argument("--x0", type=float, default=X0_DEFAULT)
    ap.add_argument("--y0", type=float, default=Y0_DEFAULT)
    ap.add_argument("--R", type=float, default=R_DEFAULT,
                    help="Cylinder radius used for selecting Ar atoms")
    ap.add_argument("--rmax", type=float, default=35.0)
    ap.add_argument("--dr", type=float, default=0.05)
    ap.add_argument("--nref", type=int, default=3,
                    help="Ideal-gas reference draws per frame. Increase for smoother normalization.")
    ap.add_argument("--seed", type=int, default=12345,
                    help="Base random seed for ideal-gas reference sampling")
    ap.add_argument("--root", default=".",
                    help="Directory containing Seed_1, Seed_2, ... folders")
    args = ap.parse_args()

    root = Path(args.root)
    mu_str = f"{args.mu:.2f}"

    r_edges = np.arange(0.0, args.rmax + args.dr, args.dr)
    r_centers = 0.5*(r_edges[:-1] + r_edges[1:])

    g_seed_list = []
    used_frames = []

    for seed in range(1, args.nseeds + 1):
        dump = root / f"Seed_{seed}" / f"Ar_mu{mu_str}.lammpstrj"
        if not dump.exists():
            raise FileNotFoundError(f"Missing dump file: {dump}")

        # Different ideal-reference RNG for each seed, reproducible overall.
        rng = np.random.default_rng(args.seed + 1000*seed)

        g, H_data, H_ref, used = compute_gr_for_dump(
            dump, args.x0, args.y0, args.R, r_edges, args.nref, rng
        )

        g_seed_list.append(g)
        used_frames.append(used)

        out_seed = root / f"Seed_{seed}" / f"gr_cyl_mu{mu_str}_seed{seed}.dat"
        seed_output = np.column_stack([r_centers, g, H_data, H_ref])
        np.savetxt(
            out_seed,
            seed_output,
            header=(
                "Cylinder-corrected RDF for one seed\n"
                f"mu={mu_str} seed={seed} dump={dump}\n"
                f"x0={args.x0} y0={args.y0} R={args.R} dr={args.dr} rmax={args.rmax} "
                f"frames_used={used} nref={args.nref}\n"
                "columns: r  g_seed  H_data  H_ideal"
            ),
            fmt="%.10e"
        )

        print(f"Seed {seed}: wrote {out_seed}  frames_used={used}")

    g_all = np.column_stack(g_seed_list)  # shape: nbins x nseeds
    g_mean = np.mean(g_all, axis=1)
    g_se = np.std(g_all, axis=1, ddof=1) / np.sqrt(args.nseeds)

    final_output = np.column_stack([r_centers, g_mean, g_se, g_all])

    seed_cols = " ".join([f"g_seed{seed}" for seed in range(1, args.nseeds + 1)])
    out_avg = root / f"gr_cyl_mu{mu_str}_seedavg.dat"

    np.savetxt(
        out_avg,
        final_output,
        header=(
            "Multiseed cylinder-corrected RDF\n"
            f"mu={mu_str} x0={args.x0} y0={args.y0} R={args.R} dr={args.dr} rmax={args.rmax} "
            f"nseeds={args.nseeds} nref={args.nref}\n"
            f"frames_used_per_seed={' '.join(map(str, used_frames))}\n"
            f"columns: r  g_mean  g_se  {seed_cols}"
        ),
        fmt="%.10e"
    )

    print(f"Done. Wrote {out_avg}")


if __name__ == "__main__":
    main()
