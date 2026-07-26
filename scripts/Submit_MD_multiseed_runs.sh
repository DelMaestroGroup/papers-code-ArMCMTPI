Threads=4
Temp=90

mkdir -p Temp_${Temp}_MultiSeed_Runs
cd Temp_${Temp}_MultiSeed_Runs

mu_min=-11.45
mu_max=-11.45

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

            for snap in 800000 1000000
            do
                mkdir -p MD_for_snap${snap}
                cd MD_for_snap${snap}

                input="in.Ar_MD_Quench_from_restart"
                rm -f ${input}

                cp ../../../../inputs/${input} .
                cp ../restart_mu${mu_val}_${snap} .

                sed -i "s/MUVAL/${mu_val}/g" ${input}
                sed -i "s/SNAPVAL/${snap}/g" ${input}

                #------------------------------------#
                time lmp_mpi -in ${input}
                #------------------------------------#

                cd ../
                echo "run for snap=${snap}, seed=${seed} finished!"
            done
            cd ../
        done
        cd ../
        mu_val=$(echo "${mu_val}-0.05"| bc -l)
done
cd ../

