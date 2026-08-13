r1min=14.9
r2min=13.3
dr=0.15
Lz=107.49


outfile1="N1_N2_vs_mu.txt"
rm -f $outfile1

mu_min=-17.00
mu_max=-9.9
mu_val=$(echo "${mu_max}" | bc -l)

while (( $(echo "${mu_val} >= ${mu_min}" | bc -l) ))
do
	mu_val=$(printf '%.2f' ${mu_val})

#	N1=$(awk -v r1min="$r1min" -v dr="$dr" -v Lz="$Lz" '$0 !~ /^#/ && $1>=r1min {sum += $2 * 2.0 * 3.141592653589793 * $1 * dr * Lz} END {printf "%.4f", sum}' radial_rho_vs_r_mu${mu_val}_seedavg.dat)
#	N2=$(awk -v r2min="$r2min" -v r1min="$r1min" -v dr="$dr" -v Lz="$Lz" '$0 !~ /^#/ && $1>=r2min && $1<r1min {sum += $2 * 2.0 * 3.141592653589793 * $1 * dr * Lz} END {printf "%.4f", sum}' radial_rho_vs_r_mu${mu_val}_seedavg.dat)


	N1=$(awk -v r1min="$r1min" '$1>=r1min && $0 !~ /^#/ {sum += $4} END {printf "%.4f", sum}' radial_rho_vs_r_mu${mu_val}_seedavg.dat)
	N2=$(awk -v r2min="$r2min" -v r1min="$r1min" '$1>=r2min && $1<r1min && $0 !~ /^#/ {sum += $4} END {printf "%.4f", sum}' radial_rho_vs_r_mu${mu_val}_seedavg.dat)
	echo "$mu_val	$N1	$N2" >>${outfile1}

	mu_val=$(echo "${mu_val}-0.05"| bc -l)
done

outfile2="monolayer_analysis.txt"
rm -f $outfile2
echo "#mu	N1	N2	dN1/dmu	 dN2/dmu" > $outfile2

sortedfile="sorted_N1_N2_file.txt"
sort -n -k1,1 "$outfile1" > "$sortedfile"

#Finite difference method:
awk 'BEGIN {OFS="\t"; print "#mu\tN1\tN2\tdN1/dmu\tdN2/dmu"}{ mu[NR]=$1; N1[NR]=$2; N2[NR]=$3; n=NR }
END{ 
for(i=1;i<=n;i++){
	if(i==1){
		dmu = mu[i+1]-mu[i]
		dN1 = (N1[i+1]-N1[i])/dmu
		dN2 = (N2[i+1]-N2[i])/dmu
	} else if(i==n){
		dmu = mu[i]-mu[i-1]
		dN1 = (N1[i]-N1[i-1])/dmu
		dN2 = (N2[i]-N2[i-1])/dmu
	} else{
		dmu = mu[i+1]-mu[i-1]
		dN1 = (N1[i+1]-N1[i-1])/dmu
		dN2 = (N2[i+1]-N2[i-1])/dmu
	}
printf "%.2f\t%.4f\t%.4f\t%.4f\t%.4f\n", mu[i], N1[i], N2[i], dN1, dN2
}
}' "$sortedfile" > "$outfile2"


