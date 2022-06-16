# This code applies the external program SNID to produce a output txt file with the information of every 
# spectra file in 'names.txt'

# Open file 'names.txt', which contains the file name and redshift value of each spectrum
file=$(< TFG/snid-5.0/dataset/names.txt)

cd TFG/snid-5.0/dataset/
rows=$(echo $file | tr "\n" "\n")
# For each row, divide the file's name and redshift value
for row in $rows; do
    name=$(echo $row | cut -f1 -d ";")
    echo $name
    redshift=$(echo $row | cut -f2 -d ";")
    # Apply SNID program
    $(snid aband=0 plot=0 iquery=0 inter=0 verbose=0 forcez=$redshift $name)
done