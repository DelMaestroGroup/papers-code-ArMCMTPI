"""
This script computes Ar-Ar, Ar-MCM (restricted) coherent neutron scattering intensity I(Q) using the powder average Debye formula from Ar Preplated MCM LAMMPS dump-file at mu=-11.45 kJ/mol.

The powder averaged Debye formula: I(Q) = \sum_{i,j=1}^{N} b_i b_j \sin(Qr_{ij})/(Qr_{ij})
where b_i,b_j are the coherent elastic neutron scattering length of respective atom types.

Key info:
    1. We restrict Ar-MCM correlations to MCM atoms that have large non-zero pair coeffs. Based on our assessment three atom types of the MCM framework are relevant: O(1), Si(2) and O(2) [i.e. type 2, 3 and 4]
    2. Also, we consider MCM atoms that lies inside a restricted cylinder of radius R_MCM=22 Angstrom
    3. For the direct term the structure factor is computed via: S_{Ar-Ar}(Q) = 1 + (2/sum_{i in Ar}b_i^2)*sum_{i<j in Ar}(b_i*b_j)*sin(Qr_ij)/Qr_ij.
    4. For the cross term the structure factor is computed via: S_{Ar-Si/O}(Q) = (2/sum_{i in Ar}b_i^2)*sum_{i in Ar} sum_{j in Si/O}(b_i*b_j)*sin(Qr_ij)/Qr_ij.
    5. Note that the normalization for both S(Q) are taken from the deposited Ar atoms. The current script computes average number of Ar atoms from multiple snapshots. The normalization effectively looks like: ||N||=sum_{i in Ar}(b_i^2) ~= (<N_Ar>_{avg}*b_Ar^2)
    6. One can do separate normalization for the cross term by considering norm ||N||=sqrt{ sum_{i in Ar} sum_{j in Si/O}(b_i*b_j) }.
    7. The system is periodic along the z direction. Thus minimum distance b/w two atoms in this script will consider wrapping around the z-direction


Output: This python script generates the SF file: debye_Sq_vs_q.txt with columns:
    Q, I_ArAr, I_ArO1, I_ArSi2, I_ArO2, S_ArAr, S_ArO1, S_ArSi2, S_ArO2, S_total
"""

import os
import re
import math
import numpy as np
import argparse

symmetricNorm=True

#Defining scattering lengths: (in Angstrom):
b_Ar= 1.909e-5
b_Si= 4.1491e-5
b_O = 5.8030e-5
b_H = -3.7390e-5

#Pore center coordinates: (in Angstrom)
x0= 42.996
y0= 39.413
Lz= 107.49 #Pore length [else check via Lz=(zhi-zlo)]

#Defining momentum grid: (in Angstrom^{-1}):
Qmin= 1.00
Qmax= 7.00
dQ  = 0.01 #(for testing use 1.0)

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

#-----------------------------------------------------#
#helper functions for wrapping and momentum grids:
def wrapped_dz(dz,Lz):
    dzp = dz - Lz*np.rint(dz/Lz)
    return dzp

def make_Q_grid(Qmin,Qmax,dQ):
    n = int(math.floor((Qmax-Qmin)/dQ)) + 1
    return Qmin + dQ * np.arange(n,dtype=float)


#-----------------------------------------------------#
#parsing the MCM raw data file:
def parse_mcm_data_file(path: str):
    """Here we parse the MCM data file once and store positions of relevant atom types names type-3[Si(2)] and type-4[O(2)].
        Note the positions of all the atoms starts after the "Atoms" declaration in the data file and columns are arranged as:
        1-[id]    2-[type]  3-[xcoord]  4-[ycoord]  5-[zcoord] 6,7,8-[just 0's]
        Additionally, we should note that while parsing the atom section is immediately followed by the velocities section (which is not needed!)
    """
    with open(path, "r") as f:
        lines = f.readlines()

    Nmcm = None
    for ln in lines:
        s = ln.strip()
        if s.endswith("atoms"):
            Nmcm = int(s.split()[0])
            break
    if Nmcm is None:
        raise RuntimeError("Could not find '<N> atoms' line in data file.")

    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("Atoms"):
            start = i
            break
    if start is None:
        raise RuntimeError("Could not find 'Atoms' section in data file.")

    i = start + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    pos = []
    types = []
    count = 0

    while i < len(lines) and count < Nmcm:
        ln = lines[i].strip()
        if ln == "":
            break
        if ln[0].isalpha():  #next section header "Velocities"
            break

        parts = ln.split()
        #Columns written as "Atoms # atomic" formats: id type x y z ...
        #Atleast 5 cols are expected from each row
        if len(parts) < 5:
            raise RuntimeError(f"Corrupted row in MCM Data file. Expected 5 elements got: {ln}")

        atype = int(parts[1])
        x = float(parts[2])
        y = float(parts[3])
        z = float(parts[4])

        pos.append((x, y, z))
        types.append(atype)

        count += 1
        i += 1

    return np.asarray(pos, dtype=float), np.asarray(types, dtype=int)

#Atom types from MCM data file:
def b_from_mcm_type(t: int) -> float:
    #MCM data file mapping: 1,3 = Si; 2,4 = O; 5 = H
    if t == 1 or t == 3:
        return b_Si
    if t == 2 or t == 4:
        return b_O
    if t == 5:
        return b_H
    raise ValueError(f"Unexpected MCM atom type: {t}")


#Restricting MCM cylinder and types:
def select_mcm_cylinder(pos_mcm, type_mcm, x0, y0, R, keep_types):
    dx = pos_mcm[:, 0] - x0
    dy = pos_mcm[:, 1] - y0
    dist_r = np.sqrt(dx*dx + dy*dy)
    mask = (dist_r <= R)
    if keep_types is not None:
        keep_types = set(keep_types)
        mask &= np.isin(type_mcm, list(keep_types))
    pos_selected = pos_mcm[mask]
    type_selected = type_mcm[mask]
    b_selected = np.array([b_from_mcm_type(t) for t in type_selected], dtype=float)
    return pos_selected, type_selected, b_selected

def split_by_type(pos_sel, type_sel, b_sel):
    mask_o1  = (type_sel == 2)
    mask_si2 = (type_sel == 3)
    mask_o2  = (type_sel == 4)
    return (pos_sel[mask_o1], b_sel[mask_o1],
            pos_sel[mask_si2], b_sel[mask_si2],
            pos_sel[mask_o2], b_sel[mask_o2])


#-------------------------------------------------#
#Calculating the intensity and structure factor for Ar-Ar in each frame:
def debye_IQ_SQ_ArAr_per_frame(pos_ar, Q):
    pos_ar = np.asarray(pos_ar, float)
    Q = np.asarray(Q, float)

    N = pos_ar.shape[0]
    nQ = Q.size

    #Self term: sum_i b^2 = N*b^2
    self_term = (b_Ar*b_Ar)*(1.0*N)

    #Accumulating distinct pairs contribution:
    #For that: distinct_sum(Q) = sum_{i<j} sinc(Q*r_ij/pi)
    distinct_sum = np.zeros(nQ, dtype=float)

    for i in range(N - 1):
        dr = pos_ar[i+1:] - pos_ar[i]     # (N-i-1,3)
        dr[:, 2] = wrapped_dz(dr[:, 2], Lz)

        rij = np.sqrt(np.sum(dr*dr, axis=1))  # (N-i-1,)

        # sinc(x)=sin(pi*x)/(pi*x) in numpy, => sin(Qr)/(Qr) = sinc(Qr/pi)
        # Broadcasting: (nQ,1) * (1,npairs)
        x = (Q[:, None] * rij[None, :]) / np.pi
        distinct_sum += np.sum(np.sinc(x), axis=1)

    Iq = self_term + 2.0 * (b_Ar*b_Ar) * distinct_sum
    Sq = Iq / (1.0*N*(b_Ar*b_Ar))
    return Iq, Sq

#Averaging I(Q) and S(Q) over all frames:
def average_IQ_SQ_ArAr_over_frames(frames, Q):
    I_acc = np.zeros_like(Q, dtype=float)
    S_acc = np.zeros_like(Q, dtype=float)
    nframes = 0

    for t, pos_ar in frames:
        N = pos_ar.shape[0]
        if N < 2:
            continue
        Iq, Sq = debye_IQ_SQ_ArAr_per_frame(pos_ar, Q)
        I_acc += Iq
        S_acc += Sq
        nframes += 1

    if nframes == 0:
        raise RuntimeError("No frames with >=2 Ar atoms found. Check Ar LAMMPS file parsing function!")

    I_avg = I_acc / nframes
    S_avg = S_acc / nframes
    return I_avg, S_avg, nframes


#-------------------------------------------------#
#Calculating the intensity and structure factor for Ar-MCM in each frame:
def debye_IQ_SQ_ArMCM_per_frame(pos_ar, pos_mcm, b_mcm, Q):
    pos_ar  = np.asarray(pos_ar, float)
    pos_mcm = np.asarray(pos_mcm, float)
    b_mcm   = np.asarray(b_mcm, float)
    Q       = np.asarray(Q, float)

    Nar = pos_ar.shape[0]
    Nm  = pos_mcm.shape[0]
    nQ  = Q.size

    #Accumulating sum_{a,m} b_m * sinc(Q r_am / pi)  (since b_Ar is constant we pull it out)
    acc = np.zeros(nQ, dtype=float)

    #Loop over Ar atoms; vectorize over MCM atoms
    for a in range(Nar):
        dr = pos_mcm - pos_ar[a]     # (Nm,3)
        dr[:, 2] = wrapped_dz(dr[:, 2], Lz)
        r = np.sqrt(np.sum(dr*dr, axis=1))  # (Nm,)

        # Build sinc(Q*r/pi): shape (nQ, Nm)
        x = (Q[:, None] * r[None, :]) / np.pi
        # Weighted by b_mcm
        acc += np.sum(np.sinc(x) * b_mcm[None, :], axis=1)

    I_cross = (2.0*b_Ar) * acc
    if symmetricNorm==True:
        norm = math.sqrt((Nar * b_Ar*b_Ar) * np.sum(b_mcm*b_mcm))
        S_cross = I_cross / norm
    else:
        S_cross = I_cross / (Nar * (b_Ar*b_Ar))

    return I_cross, S_cross


def average_IQ_SQ_ArMCM_over_frames(frames, Q, pos_mcm, b_mcm):
    I_acc = np.zeros_like(Q, dtype=float)
    S_acc = np.zeros_like(Q, dtype=float)
    nframes = 0

    for t, pos_ar in frames:
        Nar = pos_ar.shape[0]
        if Nar == 0:
            continue
        Iq, Sq = debye_IQ_SQ_ArMCM_per_frame(pos_ar, pos_mcm, b_mcm, Q)
        I_acc += Iq
        S_acc += Sq
        nframes += 1

    if nframes == 0:
        raise RuntimeError("No frames with Ar atoms SQ_ArMCM. Check Ar LAMMPS file parsing function!")

    I_avg = I_acc / nframes
    S_avg = S_acc / nframes
    return I_avg, S_avg, nframes


#-------------------------------------------------#
#Calling all the functions in main:
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", default="Ar_mu-11.45.lammpstrj", help="LAMMPS Ar dump file: Ar_mu-11.45.lammpstrj")
    ap.add_argument("--mcm",  default="Data_MCM_2x1x5.data", help="MCM data file: Data_MCM_2x1x5.data")
    ap.add_argument("--R",  type=float, default=22.5, help="Cylinder radius (Angstrom)")
    ap.add_argument("--out", default="debye_Sq_vs_q.txt", help="Output filename")
    args = ap.parse_args()

    Q = make_Q_grid(Qmin, Qmax, dQ)

    #Read frames for Ar positions
    frames = parse_lammps_frames(args.dump)

    #Read MCM once and restrict to cylinder + keep types 2,3,4
    pos_mcm, type_mcm = parse_mcm_data_file(args.mcm)
    pos_sel, type_sel, b_sel = select_mcm_cylinder(pos_mcm, type_mcm, x0, y0, args.R, keep_types=[2,3,4])
    pos_o1, b_o1, pos_si2, b_si2, pos_o2, b_o2 = split_by_type(pos_sel, type_sel, b_sel)

    print(f"Selected: O(1)={pos_o1.shape[0]}, Si(2)={pos_si2.shape[0]}, O(2)={pos_o2.shape[0]} within R={args.R}")

    #Ar-Ar only:
    I_ArAr, S_ArAr, nf1 = average_IQ_SQ_ArAr_over_frames(frames, Q)

    #Ar-MCM only:
    I_ArO1, S_ArO1, nf2 = average_IQ_SQ_ArMCM_over_frames(frames, Q, pos_o1, b_o1)
    I_ArSi2, S_ArSi2, nf3 = average_IQ_SQ_ArMCM_over_frames(frames, Q, pos_si2, b_si2)
    I_ArO2, S_ArO2, nf4 = average_IQ_SQ_ArMCM_over_frames(frames, Q, pos_o2,  b_o2)

    #Total approximate intensity "loaded-empty":
    I_total = I_ArAr + I_ArO1 + I_ArSi2 + I_ArO2
    #I_total is intensity averaged per frame

    #Total structure factor:
    if symmetricNorm==True:
        S_total = S_ArAr + S_ArO1 + S_ArSi2 + S_ArO2
    else:
        Nar_avg = np.mean([pos.shape[0] for _, pos in frames if pos.shape[0] > 0])
        norm_Ar = Nar_avg * (b_Ar*b_Ar)
        S_total = I_total / norm_Ar

    #Generating output:
    header=("# Q  I_ArAr  I_ArO1 I_ArSi2  I_ArO2  S_ArAr S_ArO1  S_ArSi2  S_ArO2  S_total\n")
    out = np.column_stack([Q, I_ArAr, I_ArO1, I_ArSi2, I_ArO2, S_ArAr, S_ArO1, S_ArSi2, S_ArO2, S_total])
    with open(args.out, "w") as f:
        f.write(header)
        np.savetxt(f, out, fmt="%.3f %.10e %.10e %.10e %.10e %.10e %.10e %.10e %.10e %.10e")
    
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
