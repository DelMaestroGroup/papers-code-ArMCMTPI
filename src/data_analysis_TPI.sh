cd data/lammps/TPI_data/

#RMS calculation for bareMCM:
cp  ../../../RMS_corr_bareMCM.py .
python3 RMS_corr_bareMCM.py

#generating TPI heatmap and U_rad data:
cd multisnapseed_data
cp ../../../../src/average_U_vs_r.py .
cp ../../../../src/average_Uxy_pm3d.py .
cp ../../../../src/RMS_corr_ArMCM.py .

python3 average_U_vs_r.py
python3 average_Uxy_pm3d.py
python3 RMS_corr_ArMCM.py

#generating Screening data:
cd RMS_corrugation_ArMCM
cp ../../../../../src/calculate_screening_factor.py .
python3 calculate_screening_factor.py

cd ../../

cd ../../../

