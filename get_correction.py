# This code reads every file which name is on the 9th column of 'Characteristics_table' CSV file, separates the wavelength vector
# from the flux density vector, and applies the 2 corrections. The resulting vectors of the 1st corrections are saved in a new TXT 
# file in the directory deredden_dataset. When the 2nd correction is applied, the results are saved in a new TXT file in the 
# directory corrected_dataset

# import external libraries
import csv
import numpy
from extinction import fitzpatrick99, remove

# directories used
dir_orig = 'dataset/original_dataset/'  # directory of the original dataset files
dir_dered = 'dataset/deredden_dataset/' # directory of the modified dataset files with the dereddening effect applied
dir_corr = 'dataset/corrected_dataset/' # directory of the modified dataset files with the reddening and resdshifts effects applied

# declaration of arrays
x = [] # wavelength values array
y = [] # flux values array
z = [] # error flux values array (not always present)

# setting constants
R_v = 3.1   # Ratio
A_v = 0     # Reddening effect

# open and read the csv file
with open('Characteristics_table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_counter = 0
    for rows in csv_reader:
        # each row equals to a spectrum
        # line_counter = 0 -> headers of csv
        if line_counter == 4124:
            # choose the column of the spectrum selected
            # rows[8] -> Spectrum ascii File column
            name_file = rows[8]
            # the name contains 'Â ' in the beginning
            name_file = name_file[2:]
            print(name_file)
            # now the name corresponds to the file name

            # create the file's path
            path_file_orig = dir_orig + name_file
            # open and read the spectrum file
            with open(path_file_orig, 'r') as f:
                # for each line, separate the wavelength value, the flux value and the error value (if exists)
                for line in f:
                    line = " ".join(line.split())
                    # if the file contains only 2 columns
                    if line.count(' ') == 1:
                        # add new value to the array, must convert the string from the file to a float
                        aux_x = line.split(' ')[0]
                        x.append(float(aux_x))
                        # add new value to the array, must convert the string from the file to a float
                        aux_y = line.split(' ')[1]
                        y.append(float(aux_y))
                    # if the file contains 3 columns
                    elif line.count(' ') >= 2:
                        # add new value to the array, must convert the string from the file to a float
                        aux_x = line.split(' ')[0]
                        x.append(float(aux_x))
                        # add new value to the array, must convert the string from the file to a float
                        aux_y = line.split(' ')[1]
                        y.append(float(aux_y))
                        # add new value to the array, must convert the string from the file to a float
                        aux_z = line.split(' ')[2]
                        z.append(float(aux_z))
                
                # 1st correction
                # rows[13] -> Galactic Extinction
                aux_E_bv = rows[13]
                # convert to float
                E_bv = float(aux_E_bv)
                # get the reddening effect
                A_v = R_v * E_bv
                # convert x (list) to a numpy array (requirements of the external library)
                x = numpy.array(x)
                # redden the flux values (y) and error values (z) (if exists the third column)
                y = remove(fitzpatrick99(x, A_v, R_v), y)
                if len(z):
                    z = remove(fitzpatrick99(x, A_v, R_v), z)
                
                # 2nd correction
                # rows[5] -> redshift
                aux_redshift = rows[5]
                # convert to float
                redshift = float(aux_redshift)
                # apply the redshift on every array
                x = x / (1 + redshift)
                y = y * (1 + redshift)
                if len(z):
                    z = z * (1 + redshift)
            
            # close the Spectrum ascii File
            f.close()

            # create the file's path
            path_file_corr = dir_corr + name_file
            # create and write the redden spectrum file
            with open(path_file_corr, 'w') as f:
                # in each line write 'wavelenght_value flux_value error_flux_value'
                new_line_num = 0
                if len(z) == 0:
                    while new_line_num < len(x):
                        new_line = '{} {}\n'.format(x[new_line_num], y[new_line_num])
                        f.write(new_line)
                        new_line_num = new_line_num + 1
                else:
                    while new_line_num < len(x):
                        new_line = '{} {} {}\n'.format(x[new_line_num], y[new_line_num], z[new_line_num])
                        f.write(new_line)
                        new_line_num = new_line_num + 1
            # close the redden spectrum file
            f.close()

            # initalization of the arrays for the new file
            x = []
            y = []
            z = []

            line_counter = line_counter + 1
        else:
            line_counter = line_counter + 1

# close the csv File
csv_file.close()