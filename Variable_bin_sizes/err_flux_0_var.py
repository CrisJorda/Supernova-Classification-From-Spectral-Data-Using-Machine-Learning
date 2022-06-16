# This code finds the maximum value of the error for each file in output_error_0 and initialises the err_value above the maximum.
# Search the matching flux spectrum for each error file's spectrum and replace the 0.0 values in it with err value.

# import external libraries
import os
import numpy
import csv

# directories used
dir_output_error = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/output_error_def/' # directory of the definitive csv files with the spectrum flux error files
dir_output_flux = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/output_flux_0/' # directory of the csv files with the spectrum flux files

# declaration of arrays and lists
x_reg = numpy.linspace(3000, 9000, 601) # new wavelength values array
pos_array = [] # positions of '0.0' in flux spectrum array
new_row = list() # row with the spectrum error
lines = list() # list of spectra error to write in the new file

# go to the directory of the csv files
os.chdir(dir_output_error)

# for each file in the dir_output_flux
for file in os.listdir():
    # set the path of the flux error csv file
    file_path_error = dir_output_error + file
    # open and read the csv spectrum error file
    csv_err_file = open(file_path_error, "r", newline='')
    csv_reader_err = csv.reader(csv_err_file, delimiter=',')

    line_counter_err = 0
    # each row of the csv file in the dir_output_error equals to a spectrum error
    for rows_err in csv_reader_err:
        # set the path of the flux csv file
        file_path_flux = dir_output_flux + 'output' + file[10:]
        # open and read the spectrum file
        csv_file = open(file_path_flux, "r", newline='')
        csv_reader = csv.reader(csv_file, delimiter=',')
        # line_counter_err = 0 -> headers of csv
        if line_counter_err != 0:
            # separate the name of the file from the actual spectrum values
            name_spectrum_err = rows_err[0]
            spect_arr_err = rows_err[1:]
            # convert the spect_arr list to a numpy array
            spect_arr_err = numpy.asarray(spect_arr_err)
            spect_arr_err = spect_arr_err.astype(numpy.float64)
            # find the maximum value of the spectrum error
            max_value = spect_arr_err.max()
            # set err_value as the max_value multiplied by 100
            err_value = max_value * 10000
            line_counter = 0
            # each row of the csv file in the dir_output_flux equals to a spectrum
            for row in csv_reader:
                # line_counter = 0 -> headers of csv
                if line_counter != 0:
                    # separate the name of the file from the actual spectrum values
                    name_spectrum = row[0]
                    # search in the flux csv the line corresponding with the same spectrum in the error csv
                    if name_spectrum == name_spectrum_err:
                        # get the spectrum array of the flux spectrum
                        spect_arr = row[1:]
                        # convert the spect_arr list to a numpy array
                        spect_arr = numpy.asarray(spect_arr)
                        spect_arr = spect_arr.astype(numpy.float64)
                        pos = 0
                        # search in spect_arr the position with '0.0' value and save them in pos_array
                        for value in spect_arr:
                            if value == 0.0: 
                                pos_array.append(pos)
                                pos = pos + 1
                            else: pos = pos + 1
                        # in every position spect_arr has a '0.0' (pos_array) set spect_arr_err at err_value
                        for position in pos_array: spect_arr_err[position] = err_value
                    
                    line_counter = line_counter + 1
                else: 
                    line_counter = line_counter + 1

            # create the row for the new file
            new_row = list(spect_arr_err)
            new_row.insert(0, name_spectrum_err)
            # add the new row to the list of lines
            lines.append(new_row)

            # initialization of arrays and lists for the next spectrum
            pos_array = []
            new_row = list()

            line_counter_err = line_counter_err + 1
        else:
            line_counter_err = line_counter_err + 1
        
        # close the csv file
        csv_file.close()

    # close the csv error file in reading mode
    csv_err_file.close()

    # open the csv file in writing mode
    csv_err_file = open(file_path_error, "w", newline='')
    mywriter = csv.writer(csv_err_file, delimiter=',')
    # write the headers
    csv_err_file.write('Spectrum ascii File,')
    mywriter.writerow(x_reg)
    # write the rows without many '0.0' (the ones saved in lines list)
    mywriter.writerows(lines)
    # close the csv file in writing mode
    csv_err_file.close()

    # initialization of arrays and lists for the new csv
    lines = list()

    print(file)