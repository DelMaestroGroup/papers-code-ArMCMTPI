import os
import numpy as np

seeds = [1, 2, 3, 4, 5]
snapshots = [800000, 1000000]

outdir = "RMS_corrugation_ArMCM"
os.makedirs(outdir, exist_ok=True)

def calculate_rms(rtz_file):
    """
    Calculate: Ubar(r) = <U(r,theta,z)>_{theta,z}
                sigma_corr(r) = sqrt(<[U(r,theta,z)-Ubar(r)]^2>_{theta,z}) at each r
    return:
        r_values, Ubar, sigma_corr, counts
    """

    data = np.loadtxt(rtz_file)

    # Columns: r(A), theta(rad), z(A), U(K)
    r_all = data[:, 0]
    U_all = data[:, 3]

    # Grouping all (theta,z) points that coreesponds to the same radius.
    r_values, inverse = np.unique(r_all, return_inverse=True)

    counts = np.bincount(inverse)
    Ubar = np.bincount(inverse, weights=U_all) / counts

    # RMS = sqrt(<(U-<U>)^2>)
    deviations = U_all - Ubar[inverse]
    sigma_corr = np.sqrt(
        np.bincount(inverse, weights=deviations**2) / counts
    )

    return r_values, Ubar, sigma_corr, counts


# separately calculated RMS for each snapseed file
all_results = {}

for seed in seeds:
    all_results[seed] = {}

    for snap in snapshots:

        rtz_file = f"He_TPI_full_rtz_seed{seed}_snap{snap}.dat"
        ur_file = f"He_TPI_U_vs_r_seed{seed}_snap{snap}.dat"

        print(f"\nProcessing seed {seed}, snapshot {snap}")
        print(f"  {rtz_file}")

        r, Ubar, sigma, counts = calculate_rms(rtz_file)

        # ----------------------------------------------------
        # Optional consistency check against existing U(r)
        # ----------------------------------------------------
        if os.path.exists(ur_file):
            radial_data = np.loadtxt(ur_file)
            r_ref = radial_data[:, 0]
            U_ref = radial_data[:, 1]

            if len(r_ref) != len(r) or not np.allclose(
                r_ref, r, rtol=0.0, atol=1.0e-10
            ):
                raise ValueError(
                    f"Radial grid mismatch between {rtz_file} and {ur_file}"
                )

            max_diff = np.max(np.abs(Ubar - U_ref))
            print(f"  max |Ubar - supplied U(r)| = {max_diff:.6e} K")

        # Save individual snapshot result
        snapshot_out = (f"{outdir}/RMS_seed{seed}_snap{snap}.dat")

        np.savetxt(snapshot_out, np.column_stack((r, Ubar, sigma, counts)),
            header="r_A Umean_K sigma_corr_K N_theta_z", fmt="%.10f")

        imin = np.argmin(Ubar)

        print(f"  r_min              = {r[imin]:.6f} A")
        print(f"  U(r_min)           = {Ubar[imin]:.6f} K")
        print(f"  sigma_corr(r_min)  = {sigma[imin]:.6f} K")
        print(f"  saved              = {snapshot_out}")

        all_results[seed][snap] = {
            "r": r,
            "Ubar": Ubar,
            "sigma": sigma
        }


# Averaging out the two snapshots within each seed
seed_results = {}

for seed in seeds:

    result1 = all_results[seed][snapshots[0]]
    result2 = all_results[seed][snapshots[1]]

    r = result1["r"]

    if not np.allclose(r, result2["r"], rtol=0.0, atol=1.0e-10):
        raise ValueError(f"Radial grids do not match for seed {seed}")

    Ubar_seed = 0.5 * (
        result1["Ubar"] + result2["Ubar"]
    )

    sigma_seed = 0.5 * (
        result1["sigma"] + result2["sigma"]
    )

    seed_out = f"{outdir}/RMS_seed{seed}_snapshot_average.dat"

    np.savetxt(
        seed_out,
        np.column_stack((r, Ubar_seed, sigma_seed)),
        header="r_A Umean_snapshot_avg_K sigma_corr_snapshot_avg_K",
        fmt="%.10f"
    )

    seed_results[seed] = {
        "r": r,
        "Ubar": Ubar_seed,
        "sigma": sigma_seed
    }


# Averaging over the 5 independent seeds
r = seed_results[1]["r"]

Ubar_all_seeds = np.array([
    seed_results[seed]["Ubar"] for seed in seeds
])

sigma_all_seeds = np.array([
    seed_results[seed]["sigma"] for seed in seeds
])

Ubar_mean = np.mean(Ubar_all_seeds, axis=0)

sigma_mean = np.mean(sigma_all_seeds, axis=0)
sigma_std = np.std(sigma_all_seeds, axis=0, ddof=1)
sigma_sem = sigma_std / np.sqrt(len(seeds))

final_out = f"{outdir}/RMS_ArMCM_5seed_average.dat"

np.savetxt(
    final_out,
    np.column_stack((
        r,
        Ubar_mean,
        sigma_mean,
        sigma_std,
        sigma_sem
    )),
    header=(
        "r_A "
        "Umean_K "
        "sigma_corr_mean_K "
        "sigma_corr_SD_K "
        "sigma_corr_SEM_K"
    ),
    fmt="%.10f"
)


# ------------------------------------------------------------
# Print result at minimum of the averaged radial potential
# ------------------------------------------------------------
imin = np.argmin(Ubar_mean)

print("\n==============================================")
print("Final average: 5 seeds x 2 snapshots")
print("==============================================")
print(f"r_min                  = {r[imin]:.6f} A")
print(f"U(r_min)               = {Ubar_mean[imin]:.6f} K")
print(f"<sigma_corr>(r_min)    = {sigma_mean[imin]:.6f} K")
print(f"SD across seeds        = {sigma_std[imin]:.6f} K")
print(f"SEM across seeds       = {sigma_sem[imin]:.6f} K")
print(f"Saved final result     = {final_out}")

