outfile="He_TPI_rtz_final.dat"
rm -f ${outfile}

echo "#r(A) theta(rad) z(A) U_K" >> ${outfile}

for iz in $(seq 1 50)
do
    file="zval_${iz}/data_z${iz}_rtz.dat"

    awk '!/^#/ && NF' ${file} >> ${outfile}

    echo "z = $iz appended"
done
