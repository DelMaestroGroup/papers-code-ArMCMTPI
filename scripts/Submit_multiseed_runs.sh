Threads=4
Temp=90

mkdir -p Temp_${Temp}_MultiSeed_Runs
cd Temp_${Temp}_MultiSeed_Runs

mu_min=-17.00
mu_max=-9.00

mu_val=$(echo "${mu_max}" | bc -l)

while (( $(echo "${mu_val} >= ${mu_min}" | bc -l) ))
do
        mu_val=$(printf '%.2f' ${mu_val})
        mkdir -p mu_${mu_val}
        cd mu_${mu_val}

        for seed in 1 2 3 4 5
        do
            mkdir -p Seed_${seed}
            cd Seed_${seed}

            rand_seed=$((RANDOM + 10000))

            input="in.Ar_MCM_GCMC"
            rm -f ${input}
            cp ../../../inputs/${input} .
            cp ../../../data_files/Data_MCM_2x1x5.data .

            sed -i "s/MUVAL/${mu_val}/g" ${input}
            sed -i "s/SEEDVAL/${rand_seed}/g" ${input}

	    #------------------------------------#
            time lmp_mpi -in ${input}
            #------------------------------------#

            echo "run for mu=${mu_val},seed=${seed} finished!"
            cd ../
        done
        cd ../
        mu_val=$(echo "${mu_val}-0.05"| bc -l)
done
cd ../
