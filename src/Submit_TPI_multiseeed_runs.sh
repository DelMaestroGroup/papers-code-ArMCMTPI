Threads=4
Temp=90
mu_val=-11.45

for seed in 1 2 3 4 5
do
	cd Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}

	for snap in 800000 1000000
	do
		cd MD_for_snap${snap}

		for iz in $(seq 1 50)
		do
			mkdir -p zval_${iz}
			cd zval_${iz}

			input="in.He_TPI"
			frozenfile="Data_MCM_Ar_frozen_4K.data"

			rm -f ${exe}
			rm -f ${input}
			rm -f ${frozenfile}

			cp ../../../../../inputs/${input} .
			cp ../${frozenfile} .

			sed -i "s/ZVAL/${iz}/g" ${input}
			#------------------------------------#
			sub="TPI_Runs.slurm"
			rm -f ${sub}
			jobname="Seed${seed}Snap${snap}Z${iz}"

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
			echo "z=${iz} submitted for seed=${seed}, snap=${snap}"
		done
		cd ../
	done
	cd ../../../
done
