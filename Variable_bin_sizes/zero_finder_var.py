# For each output_flux csv in the folder output_flux, this code counts the times that a spectrum (row) has the value '0.0'. 
# Then, it creates a new csv file in the folder output_flux_0 with only the rows with less than N '0.0' values.
# In total, this code delates 264 files in the transition from output_flux to output_flux_0.
# It also delates the same files in the output error csv files.

# import external libraries
import os
import numpy
import csv

# directories used
dir_output_flux = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/output_flux_0/' # directory of the csv files with the spectrum flux files
dir_output_error = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/output_error_0/' # directory of the csv files with the spectrum flux error files

# declaration of arrays and lists
name_0 = [] # array with the names of the spectra with more than N '0.0' in them
lines = list() # list of spectra without more than N '0.0' in them
lines_err = list() # list of spectra to be copied in the new output error file
cols = [] # array with the columns of the new csv file without any '0.0' in them
x_reg = numpy.linspace(3000, 9000, 601) # new wavelength values array

# declaration of numbers
N = 313 # number of maximum '0.0' for the new files
total_0 = 0 # sum of the number of spectra delated -> 264

# go to the directory of the csv files
os.chdir(dir_output_flux)

# for each file in the dir_output_flux
for file in os.listdir():
    # set the path of the flux csv file
    file_path_flux = dir_output_flux + file
    # open and read the csv spectrum error file
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
            # count the numer of '0.0' in the spectrum
            num_0 = spect_arr.count('0.0')
            # if the number of '0.0' is bigger than N, add the name of the spectrum in the name_0 array
            if num_0 < N: lines.append(rows)
            else: name_0.append(name_spectrum)

            line_counter = line_counter + 1
        else:
            line_counter = line_counter + 1
    
    # add the total number of spectra with more than N '0.0' to the total
    total_0 = total_0 + len(name_0)

    # close the csv file in reading mode
    csv_file.close()

    # open the csv file in writing mode
    csv_file = open(file_path_flux, "w", newline='')
    mywriter = csv.writer(csv_file, delimiter=',')
    # write the headers
    csv_file.write('Spectrum ascii File,')
    mywriter.writerow(x_reg)
    # write the rows without many '0.0' (the ones saved in lines list)
    mywriter.writerows(lines)
    # close the csv file in writing mode
    csv_file.close()

    # open again the csv file but for reading
    file_csv = open(file_path_flux, "r", newline='')
    mat = numpy.loadtxt(file_csv, delimiter=",", dtype=str)
    # find the columns of the new csv file without any '0.0' in them and save them in cols array
    for col in range(601):
        if '0.0' not in mat[:,col]: cols.append(col+1)
    # close the csv file in reading mode
    file_csv.close()
    # convert the cols array into a numpy array
    cols = numpy.asarray(cols)

    print(file, cols)

    # now, delate the same rows in the corresponding output_err csv file
    # the names of the spectra delated are in the names_0 array

    # set the path of the error csv file
    file_path_error = dir_output_error + 'output_err' + file[6:]
    # open and read the spectrum file
    csv_err_file = open(file_path_error, "r", newline='')
    csv_err_reader = csv.reader(csv_err_file, delimiter=',')

    line_counter_err = 0
    # each row of the csv file in the dir_output_flux equals to a spectrum
    for rows_err in csv_err_reader:
        # line_counter_err = 0 -> headers of csv
        if line_counter_err != 0:
            # separate the name of the file with the actual spectrum error values
            name_spectrum_err = rows_err[0]
            spect_arr_err = rows_err[1:]
            if name_spectrum_err not in name_0: lines_err.append(rows_err)
            line_counter_err = line_counter_err + 1
        else:
            line_counter_err = line_counter_err + 1

    # close the csv file in reading mode
    csv_err_file.close()

    # open the csv error file in writing mode
    csv_err_file = open(file_path_error, "w", newline='')
    mywriter_err = csv.writer(csv_err_file, delimiter=',')
    # write the headers
    csv_err_file.write('Spectrum ascii File,')
    mywriter_err.writerow(x_reg)
    # write the rows without many '0.0' (the ones saved in lines_err list)
    mywriter_err.writerows(lines_err)
    # close the csv file in writing mode
    csv_err_file.close()

    # initialization of arrays and lists for the new csv
    name_0 = []
    lines = list()
    lines_err = list()
    cols = []

print(total_0)

# print(x_reg[310]) -> 6,100.0 angstroms