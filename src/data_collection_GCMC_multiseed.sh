Temp=90
mkdir -p data_files
cd data_files

mkdir -p lammps
cd lammps

mkdir -p Ar_nstats
cd Ar_nstats

for seed in 1 2 3 4 5
do
    mkdir -p Seed_${seed}
    cd Seed_${seed}

    mu_min=-17.00
    mu_max=-9.00
    mu_val=$(echo "${mu_max}" | bc -l)

    while (( $(echo "${mu_val} >= ${mu_min}" | bc -l) ))
    do
        mu_val=$(printf '%.2f' ${mu_val})

        #------------------------------------#
        cp ../../../../Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}/Nstats_mu${mu_val}.dat .
        #------------------------------------#

        mu_val=$(echo "${mu_val}-0.05"| bc -l)
        done
        cd ../
done
cd ../

mkdir -p Ar_dumpfiles
cd Ar_dumpfiles

for seed in 1 2 3 4 5
do
    mkdir -p Seed_${seed}
    cd Seed_${seed}

    mu_min=-17.00
    mu_max=-9.00
    mu_val=$(echo "${mu_max}" | bc -l)

    while (( $(echo "${mu_val} >= ${mu_min}" | bc -l) ))
    do
        mu_val=$(printf '%.2f' ${mu_val})

        #------------------------------------#
        cp ../../../../Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}/Ar_mu${mu_val}.lammpstrj .
        #------------------------------------#

        mu_val=$(echo "${mu_val}-0.05"| bc -l)
        done
        cd ../
done
cd ../

cd ../../
