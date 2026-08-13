cd data/lammps/Ar_dumpfiles/



for seed in 1 2 3 4 5
do
	cd Seed_${seed}/

	cp ../../../../src/compute_radial_density.py .
	python3 compute_radial_density.py

	cd ../
done

cp ../../../src/get_rhorad_multiseed.py .
python3 get_rhorad_multiseed.py

cp ../../../src/gr_cyl_multiseed.py .
python3 gr_cyl_multiseed.py

cp ../../../src/analyze_monolayer_from_radial.sh .
bash analyze_monolayer_from_radial.sh

cd ../../../
