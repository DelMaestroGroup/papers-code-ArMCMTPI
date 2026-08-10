Threads=4
Temp=90
mu_val=-11.45

for seed in 1 2 3 4 5
do
	cd Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}

	rand_seed=$((RANDOM + 10000))
	for snap in 800000 1000000
	do
		mkdir -p MD_for_snap${snap}
		cd MD_for_snap${snap}

		exe="lmp_mpi"
		input="in.Ar_MD_Quench_from_restart"
		rm -f ${input}

		cp ../../../../inputs/${input} .
		cp ../restart_mu${mu_val}_${snap} .

		sed -i "s/MUVAL/${mu_val}/g" ${input}
		sed -i "s/SNAPVAL/${snap}/g" ${input}

		#------------------------------------#
		sub="MD_Runs.slurm"
		rm -f ${sub}
		jobname="Seed${seed}_Snap${snap}"

		echo "#!/bin/bash -x"                       >>${sub}
		echo "#SBATCH --account acf-utk0011"        >>${sub}
		echo "#SBATCH -J ${jobname}"                >>${sub}
		echo "#SBATCH --nodes=1"                    >>${sub}
		echo "#SBATCH --ntasks=1"                   >>${sub}
		echo "#SBATCH --cpus-per-task=${Threads}"   >>${sub}
		echo "#SBATCH --partition=campus"           >>${sub}
		echo "#SBATCH --qos=campus"                 >>${sub}
		echo "#SBATCH --nodelist=il[1230-1235],clr[0729,0730,0733,0734,0735,0737,0819,0820,0823,0824,0825,0829]"     >>${sub}
		echo "#SBATCH --time=01-00:00:00"           >>${sub}
		echo "#SBATCH --error=${jobname}.e%J"       >>${sub}
		echo "#SBATCH --output=${jobname}.o%J"      >>${sub}
		echo 'cd $SLURM_SUBMIT_DIR'                 >>${sub}

		echo "module load lammps/29Oct2020_intel"   >>${sub}
		echo "export OMP_NUM_THREADS=${Threads}"    >>${sub}
		echo "export OMP_PLACES=cores"              >>${sub}
		echo "export OMP_PROC_BIND=spread"          >>${sub}

		echo "  "                                   >>${sub}
		echo "date"                                 >>${sub}
		echo "  "                                   >>${sub}
		echo "time srun -n 1 ${exe} -in ${input}"  >>${sub}
		echo "  "                                   >>${sub}

		echo "date"                                 >>${sub}
		sbatch ${sub}
		#------------------------------------#
		cd ../
		echo "snap=${snap} submitted for seed=${seed}!"
	done
	cd ../../../
done
