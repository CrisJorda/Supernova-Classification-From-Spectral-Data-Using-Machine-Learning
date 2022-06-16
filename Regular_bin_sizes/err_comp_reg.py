# This code generates two matrices from the spectra including error numbers, one of flux values and another of flux error values.
# Then compares the corrected spectrum of the files in the final matrix against spectra of the new generated matrix with the euclidean distance
# and writes the error of the most similar ones to the final matrix error.

# import external libraries
import os
import numpy
import csv
from scipy import interpolate
from scipy.spatial import distance

# directories used
dir_err_spectrum = 'C:/Users/Cristina/Documents/uni/4B/TFG/dataset/err_dataset/' # directory of the spectrum files with error
dir_outputs = 'C:/Users/Cristina/Documents/uni/4B/TFG/Regular_bin_sizes/output_flux/' # directory of the spectrum matrices

# number of values of the interpoleted spectrum
N = 601  # one value for each 10 angstroms
#N = 401 # one value for each 15 angstroms
#N = 301 # one value for each 20 angstroms
#N = 201 # one value for each 25 angstroms
#N = 241 # one value for each 30 angstroms

# declaration of arrays
x = []  # wavelength values array
y = []  # flux values array
z = [] # flux error values array
x_reg = numpy.linspace(3000, 9000, N) # new wavelength values array
y_interp1d = []  # resampled flux values array resulting from interpolate.interp1d() method
z_interp1d = []  # resampled flux error values array resulting from interpolate.interp1d() method
distances = [] # euclidean distances array

# create an output csv file for the new flux values
output_file_y = "output_y.csv"
# open in writing mode the ouptut csv file
file_csv_y = open(output_file_y, "w", newline='')
mywriter_y = csv.writer(file_csv_y, delimiter=',')
# write the headers
file_csv_y.write('Spectrum ascii File,')
mywriter_y.writerow(x_reg)

# create an output csv file for the new flux error values
output_file_z = "output_z.csv"
# open in writing mode the ouptut csv file
file_csv_z = open(output_file_z, "w", newline='')
mywriter_z = csv.writer(file_csv_z, delimiter=',')
# write the headers
file_csv_z.write('Spectrum ascii File,')
mywriter_z.writerow(x_reg)

# go to the  directory of the spectrum files with error
os.chdir(dir_err_spectrum)

# for each file in the dir_err_spectrum
for file in os.listdir():
    # set the path of the names txt file
    file_path_err = dir_err_spectrum + file
    # open and read the spectrum file
    f = open(file_path_err)
    content = f.readlines()

    # open and read the spectrum file with error
    for line in content:
        line = " ".join(line.split())
        # add new value to the wavelentgh array, must convert the string from the file to a float
        aux_x = line.split(' ')[0]
        x.append(float(aux_x))
        # add new value to the flux array, must convert the string from the file to a float
        aux_y = line.split(' ')[1]
        y.append(float(aux_y))
        # add new value to the flux error array, must convert the string from the file to a float
        aux_z = line.split(' ')[2]
        z.append(float(aux_z))
    # close the spectrum file
    f.close()

    # apply a regular wavelength bin resampling in each spectrum (flux)
    f_interp1d_y = interpolate.interp1d(
        x, y, bounds_error=False, fill_value=0)
    # use interpolation function returned by f_interp1d_y()
    y_interp1d = f_interp1d_y(x_reg)
    y_interp1d = numpy.array(y_interp1d)

    # apply a regular wavelength bin resampling in each spectrum (error)
    f_interp1d_z = interpolate.interp1d(
        x, z, bounds_error=False, fill_value=0)
    # use interpolation function returned by f_interp1d_z()
    z_interp1d = f_interp1d_z(x_reg)
    z_interp1d = numpy.array(z_interp1d)

    # save the file's name and the resulting flux vector in a row of the output flux csv file
    file_csv_y.write(file + ',')
    mywriter_y.writerow(y_interp1d)

    # save the file's name and the resulting flux error vector in a row of the output error csv file
    file_csv_z.write(file + ',')
    mywriter_z.writerow(z_interp1d)

    # set the original wavelength and flux arrays to 0 for the next spectrum values
    x = []
    y = []
    z = []

# close the output csv files
file_csv_y.close()
file_csv_z.close()

# go to the directory of the spectrum matrices
os.chdir(dir_outputs)

# for each csv file in the dir_outputs
for file_csv in os.listdir():
    # set the path of the output csv file
    file_path_csv = dir_outputs + file_csv
    # open and read the ouput csv file
    csv_file = open(file_path_csv, "r", newline='')
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # create an output csv error file
    output_error_file = "output_err_" + file_csv[7:]
    # open in writing mode the ouptut csv file
    file_err_csv = open(output_error_file, "w", newline='')
    mywriter_err = csv.writer(file_err_csv, delimiter=',')
    # write the headers
    file_err_csv.write('Spectrum ascii File,')
    mywriter_err.writerow(x_reg)

    line_counter = 0
    # each row of the csv file in the dir_outputs equals to a spectrum
    for rows in csv_reader:
        # open again the output csv flux file but for reading
        file_csv_y = open('C:/Users/Cristina/Documents/uni/4B/TFG/Regular_bin_sizes/output_y.csv', "r", newline='')
        myreader_y = csv.reader(file_csv_y, delimiter=',')
        # line_counter = 0 -> headers of csv
        if line_counter != 0:
            # separate the name of the file with the actual spectrum values
            name_spectrum = rows[0]
            spect_arr = rows[1:]
            # convert the spect_arr to a numpy array
            spect_arr = numpy.asarray(spect_arr, dtype=float)
            # calculate the euclidean distance of spect_arr with every row in the file_csv_y file (spect_arr_y)
            line_counter_y = 0
            # each row equals to a spectrum
            for row_y in myreader_y:
                # line_counter_y = 0 -> headers of csv
                if line_counter_y != 0:
                    # separate the name of the file with the actual spectrum values
                    name_spectrum_y = row_y[0]
                    spect_arr_y = row_y[1:]
                    # convert the spect_arr_y to a numpy array
                    spect_arr_y = numpy.asarray(spect_arr_y, dtype=float)
                    # euclidean distance calculation
                    dst = distance.euclidean(spect_arr, spect_arr_y)
                    # add in the distances array
                    distances.append(float(dst))
                    line_counter_y = line_counter_y + 1
                else:
                    line_counter_y = line_counter_y + 1
            # convert the distances array to numpy
            distances = numpy.asarray(distances, dtype=float)
            #print(len(distances)) -> 554
            # search for the position of the minimum distance
            min_pos = numpy.argmin(distances) + 1

            file_csv_z = open('C:/Users/Cristina/Documents/uni/4B/TFG/Regular_bin_sizes/output_z.csv', "r", newline='')
            myreader_z = csv.reader(file_csv_z, delimiter=',')
            line_counter_z = 0
            # get the corresponding error spectrum from the file_csv_z and write them into the output error csv file
            for row_z in myreader_z:
                if line_counter_z == min_pos:
                    file_err_csv.write(rows[0] + ',')
                    mywriter_err.writerow(row_z[1:])
                    line_counter_z = line_counter_z + 1
                else:
                    line_counter_z = line_counter_z + 1
            # close spectrum flux error csv file
            file_csv_z.close()

            line_counter = line_counter + 1
        else:
            line_counter = line_counter + 1
        
        # initalization of the array for the new spectrum
        distances = []

        # close spectrum flux csv file
        file_csv_y.close()
    
    # close output csv error file
    file_err_csv.close()

# close csv file
csv_file.close()