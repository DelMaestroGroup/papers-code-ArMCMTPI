Temp=90
mu_val=-11.45

for seed in 1 2 3 4 5
do
	for snap in 800000 1000000
	do
		cd Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}/MD_for_snap${snap}/

		cp ../../../../src/get_Urad_data.py .
		cp ../../../../src/get_pm3d_data.py .
		cp ../../../../src/data_collect_rtz.sh

		python3 get_Urad_data.py
		python3 get_pm3d_data.py
		bash data_collect_rtz.sh

		cp He_TPI_xy_pm3d.dat ../../../../data/lammps/TPI_data/multisnapseed_data/He_TPI_xy_pm3d_seed${seed}_snap${snap}.dat
		cp He_TPI_U_vs_r.dat ../../../../data/lammps/TPI_data/multisnapseed_data/He_TPI_U_vs_r_seed${seed}_snap${snap}.dat
		cp He_TPI_rtz_final.dat ../../../../data/lammps/TPI_data/multisnapseed_data/He_TPI_full_rtz_seed${seed}_snap${snap}.dat


		cd ../../../../
	done
done
