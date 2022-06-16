# This python code reads the names of the spectrum files from a txt file, rescales the spectrum values 
# to fit them all in the same scale (between 3,000 and 9,000 angstroms in intervals of N angstroms), 
# and saves the new arrays in a csv file according on the spectrum phases (variable epoch bins).

# import external libraries
import os
import numpy
import csv
from scipy import interpolate
import pandas

# directories used
# directory of the txt files with the spectrum names files
dir_txt = 'C:/Users/Cristina/Documents/uni/4B/TFG/Variable_bin_sizes/txt/'
# directory of the spectrum files
dir_spectrum = 'C:/Users/Cristina/Documents/uni/4B/TFG/dataset/corrected_dataset/'

# number of values of the interpoleted spectrum
N = 601  # one value for each 10 angstroms
# N = 401 # one value for each 15 angstroms
# N = 301 # one value for each 20 angstroms
# N = 201 # one value for each 25 angstroms
# N = 241 # one value for each 30 angstroms

# declaration of arrays
x = []  # wavelength values array
y = []  # flux values array
x_reg = numpy.linspace(3000, 9000, N)  # new wavelength values array
y_interp1d = []  # resampled flux values array resulting from interpolate.interp1d() method

# go to the  directory of the txt files
os.chdir(dir_txt)

# for each file in the dir_txt
for file in os.listdir():
    # set the path of the names txt file
    file_path_txt = dir_txt + file
    # open and read the spectrum file
    f = open(file_path_txt)
    content = f.readlines()

    # create an output csv file
    output_file = "output_" + file[:-4] + ".csv"
    # open in writing mode the ouptut csv file
    file_csv = open(output_file, "w", newline='')
    mywriter = csv.writer(file_csv, delimiter=',')
    # write the headers
    file_csv.write('Spectrum ascii File,')
    mywriter.writerow(x_reg)

    # for each row of the names txt file is a spectrum's file name
    for name in content:
        # correct the file's name
        name_file = name[2:-1]
        # set the path of the spectrum file
        file_path_spectrum = dir_spectrum + name_file

        # open and read the spectrum file
        with open(file_path_spectrum, 'r') as spectrum:
            # for each line, separate the wavelength value and the flux value
            for line in spectrum:
                line = " ".join(line.split())
                # add new value to the wavelentgh array, must convert the string from the file to a float
                aux_x = line.split(' ')[0]
                x.append(float(aux_x))
                # add new value to the flux array, must convert the string from the file to a float
                aux_y = line.split(' ')[1]
                # if the flux value if 'nan' change it to 0.0
                if aux_y == 'nan': aux_y = 0.0
                y.append(float(aux_y))
        # close the spectrum file
        f.close()

        # apply a regular wavelength bin resampling in each spectrum
        f_interp1d = interpolate.interp1d(
            x, y, bounds_error=False, fill_value=0)
        # use interpolation function returned by f_interp1d()
        y_interp1d = f_interp1d(x_reg)
        y_interp1d = numpy.array(y_interp1d)

        # save the file's name and the resulting flux vector in a row of the output csv file
        file_csv.write(name_file + ',')
        mywriter.writerow(y_interp1d)

        # set the original wavelength and flux arrays to 0 for the next spectrum values
        x = []
        y = []

    # close the output csv file
    file_csv.close()

    # close the names txt file
    f.close()
