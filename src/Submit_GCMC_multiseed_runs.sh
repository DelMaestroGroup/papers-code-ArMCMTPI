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

	    exe="lmp_mpi"
            input="in.Ar_MCM_GCMC"
	    mcmfile="Data_MCM_2x1x5.data"
	    
            rm -f ${input}
	    rm -f ${mcmfile}

            cp ../../../inputs/${input} .
            cp ../../../data/lammps/${mcmfile} .

            sed -i "s/MUVAL/${mu_val}/g" ${input}
            sed -i "s/SEEDVAL/${rand_seed}/g" ${input}

	    #------------------------------------#
	    sub="GCMC_Runs.slurm"
	    rm -f ${sub}
	    jobname="MU${mu_val}_Seed${seed}"

	    echo "#!/bin/bash -x"                       >>${sub}
	    echo "#SBATCH --account acf-utk0011"        >>${sub}
	    echo "#SBATCH -J ${jobname}"                >>${sub}
	    echo "#SBATCH --nodes=1"                    >>${sub}
	    echo "#SBATCH --ntasks=1"                   >>${sub}
	    echo "#SBATCH --cpus-per-task=${Threads}"   >>${sub}
	    echo "#SBATCH --partition=campus"   	>>${sub}
	    echo "#SBATCH --qos=campus"                 >>${sub}
	    echo "#SBATCH --nodelist=il[1230-1235],clr[0729,0730,0733,0734,0735,0737,0819,0820,0823,0824,0825,0829]"     >>${sub}
	    echo "#SBATCH --time=01-00:00:00"		>>${sub}
            echo "#SBATCH --error=${jobname}.e%J"       >>${sub}
            echo "#SBATCH --output=${jobname}.o%J"      >>${sub}
            echo 'cd $SLURM_SUBMIT_DIR'                 >>${sub}

            echo "module load lammps/29Oct2020_intel"	>>${sub}
            echo "export OMP_NUM_THREADS=${Threads}"	>>${sub}
            echo "export OMP_PLACES=cores"		>>${sub}
            echo "export OMP_PROC_BIND=spread"		>>${sub}

            echo "  "                                   >>${sub}
            echo "date"                                 >>${sub}
            echo "  "                                   >>${sub}
            echo "time srun -n 1 ${exe} -in ${input}"  >>${sub}
            echo "  "                                   >>${sub}

            echo "date"                                 >>${sub}
            sbatch ${sub}
            #------------------------------------#
            echo "mu=${mu_val},seed=${seed} submitted!"
            cd ../
        done
        cd ../
        mu_val=$(echo "${mu_val}-0.05"| bc -l)
done
cd ../
