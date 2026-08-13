mu=-11.45

for seed in 1 2 3 4 5
do
    cd Temp_${Temp}_MultiSeed_Runs/mu_${mu_val}/Seed_${seed}/

    cp ../../../../src/New_SF_Ar-MCM_restricted.py .
    python3 New_SF_Ar-MCM_restricted.py

    cp debye_Sq_vs_q.txt New_debye_Sq_vs_q_seed${seed}_symm_avgd_Rc_22.5.txt
    cp New_debye_Sq_vs_q_seed${seed}_symm_avgd_Rc_22.5.txt ../../../data/lammps/Str_factor/

    cd ../../../
done

cd data/lammps/Str_factor/

cp ../../../src/get_avgSq.py .
python3 get_avgSq.py

cd ../../../


    

