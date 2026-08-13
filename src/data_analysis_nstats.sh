Temp=90			
start_step=200000
end_step=1000000

mass_MCM=6.541641e-19	#in grams
mu0=-9.85		#kJ/mol
R=0.008314462618	#kJ/mol/K
NA=6.02214076e23	#Avogadro number

cd data/lammps/Ar_nstats/

for seed in 1 2 3 4 5
do
	outfile1="Navg_uptake_vs_mu_seed${seed}.dat"
	rm -f Seed_${seed}/${outfile1}
	echo "#mu	PbyP0	Navg	Uptake[mmol/g]"	>>Seed_${seed}/${outfile1}

	mu_min=-17.00
	mu_max=-9.00
	mu_val=$(echo "${mu_max}" | bc -l)

	while (( $(echo "${mu_val} >= ${mu_min}" | bc -l) ))
	do
		mu_val=$(printf '%.2f' ${mu_val})
		#------------------------------------#
		infile="Seed_${seed}/Nstats_mu${mu_val}.dat"

		Navg=$(awk -v s="$start_step" -v e="$end_step" '$1 >= s && $1 <= e {sum += $2; n++} END {print sum/n}' "$infile")

		PbyP0=$(awk -v mu="$mu_val" -v mu0="$mu0" -v R="$R" -v T="$Temp" 'BEGIN{printf "%.10e", exp((mu-mu0)/(R*T))}')

		uptake=$(awk -v N="$Navg" -v NA="$NA" -v m="$mass_MCM" 'BEGIN{printf "%.10f", (N/NA)*1000.0/(m/4.0)}')
		
#		Navg=$(awk '$1 >= 400000 && $1 <= 1000000 {sum += $2; n++} END {print sum/n}' "$infile")
		echo "${mu_val}	${PbyP0}	${Navg}	${uptake}" >>Seed_${seed}/${outfile1}
		#------------------------------------#

		mu_val=$(echo "${mu_val}-0.05"| bc -l)
	done
done

cp ../../../src/get_nstats.py
python3 get_nstats.py

cd ../../../
