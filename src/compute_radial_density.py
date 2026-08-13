"""
This script computes the radial density of Ar atoms inside the MCM nanopore framework. The radial density is defined as the number of particles in the annular region of width 'dr' divided by the volume of the annular region:
    rho(r) = <N(r+dr)-N(r)>/(2*pi*r*dr*Lz)= <N_{bin}(r+dr/2)>/(pi*((r+dr)^2-r^2)*Lz) = <N_{bin}(r_c)>/V_{bin}

Key info:
    1. The radial density is computed in the range of r=[0,21) Angstrom
    2. We keep the width dr=0.15 fixed. Choice of dr is based on the diameter of Ar=1.42 Angstrom.
    3. The current script generates radial density at each mu and for each seed. For multiple seeds one has to average over all of them to obtain the average radial density.
    4. The script parse the Ar-Ar dump file and average of 160 GCMC snapshots

Output: This python script generates the the RD file: radial_rho_vs_r_mu{MUVAL}.txt, where MUVAL is the value of chemical potential.

The output file generates columns: r_c(in A)  rho(r_c)(in A^{-3}) counts_mean
"""

import os
import re
import math
import numpy as np
import argparse
import glob

#Pore center coordinates: (in Angstrom)
x0=42.996
y0=39.413

Lz  = 107.49 
Rmax= 21.0   #max radial distance
dr  = 0.15   #width 

#Parsing the Ar-Ar LAMMPS dump file:
def parse_lammps_frames(path):
    """ Here we parse LAMMPS dump file and return a list of complete frames.
        Each frame begins with the following structure:

            ITEM: TIMESTEP
            200000 (timestep)
            ITEM: NUMBER OF ATOMS
            511 (Ntotal)
            ITEM: BOX BOUNDS ff ff pp
            0.0000000000000000e+00 8.5992000000000004e+01
            0.0000000000000000e+00 7.8825999999999993e+01
            -4.2996000000000002e+01 6.4494000000000000e+01
            ITEM: ATOMS id type x y z

       Each frame provides the following info: (timestep, xyz[N,3])
    """
    frames = []
    with open(path, "r") as f:
        while True:
            """Reading first line"""
            line = f.readline()
            if not line:
                break
            assert line.startswith("ITEM: TIMESTEP")

            """Reading timestep"""
            timestep = int(f.readline().strip())

            """Reading total atoms"""
            line = f.readline()
            assert line.startswith("ITEM: NUMBER OF ATOMS")
            ntotal = int(f.readline().strip())

            """Reading box bounds"""
            line = f.readline()
            assert line.startswith("ITEM: BOX BOUNDS")
            xlo, xhi = map(float, f.readline().split()[:2])
            ylo, yhi = map(float, f.readline().split()[:2])
            zlo, zhi = map(float, f.readline().split()[:2])
            assert abs((zhi-zlo)-Lz) < 1e-6
            #bounds = (xlo, xhi, ylo, yhi, zlo, zhi)

            """Reading LAMMPS dump structure"""
            line = f.readline()
            assert line.startswith("ITEM: ATOMS")
            cols = line.split()[2:]
            col = {name:i for i, name in enumerate(cols)}

            """Storing the coordinates with timesteps as frames"""
            pos = []
            for _ in range(ntotal):
                rows = f.readline().split()
                atype = int(rows[col["type"]])
                if atype !=6:
                    continue
                x = float(rows[col["x"]])
                y = float(rows[col["y"]])
                z = float(rows[col["z"]])
                pos.append((x,y,z))

            xyz = np.asarray(pos, dtype=float)
            #frames.append((timestep, xyz, bounds))
            frames.append((timestep, xyz))

    return frames

def avg_radial_density_over_frames(frames):
    """Here we compute the cylindrical symmetric radial density profile averaged of GCMC snapshots or frames: rho(r_c) = <N_{bin}(r_c)>/V_bin
    """
    nbins = int(math.ceil(Rmax/dr))                #generating all bins
    r_edges = np.linspace(0.0, nbins*dr, nbins+1)  #creating each bin range
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:]) #finding centers of each bin

    #computing bin volume:
    r1 = r_edges[:-1]
    r2 = r_edges[1:]
    bin_volume = math.pi*(r2*r2 - r1*r1)*Lz

    counts_per_frame = []

    for (timestep,xyz) in frames:
        dx = xyz[:,0] - x0
        dy = xyz[:,1] - y0
        r  = np.sqrt(dx*dx + dy*dy)

        #Obtain histogram within r-range [0,Rmax)
        r_sel = r[(r>=0.0) & (r<Rmax)]
        hist,_  = np.histogram(r_sel, bins=r_edges)
        counts_per_frame.append(hist.astype(float))

    counts_per_frame = np.asarray(counts_per_frame) #shape (nframes, nbins)
    nframes = counts_per_frame.shape[0]
    if nframes == 0:
        raise ValueError("No frames found. Check parsing funtion!")

    rho_per_frame = counts_per_frame/bin_volume
    counts_mean = np.mean(counts_per_frame, axis=0)

    rho_mean = np.mean(rho_per_frame, axis=0)
    #rho_std  = np.std(rho_per_frame, axis=0,ddof=1) if nframes > 1 else np.zeros_like(rho_mean)

    return r_centers, rho_mean, counts_mean


def main():
    mu_read = re.compile(r"Ar_mu(-?\d+(?:\.\d+)?)\.lammpstrj$")
    files = glob.glob("Ar_mu*.lammpstrj")
    if len(files) == 0:
        raise RuntimeError("No Ar dump file found in the current directory!")
#    if len(files) >1:
#        raise RuntimeError("Multiple Ar dump file found in the current directory!")

#    filename = files[0]
#    m = mu_read.search(filename)
#    mu = float(m.group(1))

    files = sorted(files,key=lambda f: float(mu_read.search(f).group(1)))
    print(f"Found {len(files)} Ar dump files.")

    for filename in files:
        m = mu_read.search(filename)
        mu = float(m.group(1))

        #Reading Ar positions from frames:
        frames = parse_lammps_frames(filename)
        r, rho_mean, counts_mean = avg_radial_density_over_frames(frames)

        out = f"radial_rho_vs_r_mu{mu:.2f}.dat"
        with open(out, "w") as g:
            g.write(f"#Cylindrical radial density rho(r) in A^-3 at mu={mu:.2f} kJ/mol\n")
            g.write("#r_center(A)  rho_mean(A^-3)  counts_mean\n")
            for ri, rm, cm in zip(r, rho_mean, counts_mean):
                g.write(f"{ri:10.4f}  {rm:14.7e}  {cm:12.6f}\n")

        print(f"Finished writing {out}")
        

if __name__ == "__main__":
    main()
