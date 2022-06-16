# This code normalises each spectrum from each csv file in the output_flux_0 dividing each flux value by the value of 
# that specific spectrum at 6,100.0 angstroms.

# import external libraries
import os
import numpy
import csv

# directories used
dir_output_flux = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/output_flux_norm/' # directory of the csv files with the spectrum names files

# declaration of arrays and lists
new_row = list() # row with the spectrum normalised
lines = list() # list of spectra normalised to write in the new file
x_reg = numpy.linspace(3000, 9000, 601) # new wavelength values array

# go to the  directory of the csv files
os.chdir(dir_output_flux)

# for each file in the dir_output_flux
for file in os.listdir():
    # set the path of the names txt file
    file_path_flux = dir_output_flux + file
    # open and read the spectrum file
    csv_file = open(file_path_flux, "r", newline='')
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_counter = 0
    # each row of the csv file in the dir_output_flux equals to a spectrum
    for rows in csv_reader:
        # line_counter = 0 -> headers of csv
        if line_counter != 0:
            # separate the name of the file with the actual spectrum values
            name_spectrum = rows[0]
            spect_arr = rows[1:]
            # convert the spect_arr list to a numpy array
            spect_arr = numpy.asarray(spect_arr)
            spect_arr = spect_arr.astype(numpy.float64)
            # get the flux value at 6,100.0 angstroms
            value_6100 = rows[311]
            # convert value_6100 string to a float
            value_6100 = float(value_6100)
            # normalise each flux value by value_6100
            new_row = spect_arr / value_6100
            # create the row for the new file
            new_row = list(new_row)
            new_row.insert(0, name_spectrum)
            # add the new row to the list of lines
            lines.append(new_row)

            line_counter = line_counter + 1
        else:
            line_counter = line_counter + 1
    
    # close the csv file in reading mode
    csv_file.close()

    # open the csv file in writing mode
    csv_file = open(file_path_flux, "w", newline='')
    mywriter = csv.writer(csv_file, delimiter=',')
    # write the headers
    csv_file.write('Spectrum ascii File,')
    mywriter.writerow(x_reg)
    # write the spectra normalized
    mywriter.writerows(lines)
    # close the csv file in writing mode
    csv_file.close()
    print(file)

    # initialization of arrays and lists for the new csv
    new_row = list()
    lines = list()