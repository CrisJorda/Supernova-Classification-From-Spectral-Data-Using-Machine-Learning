# This code select the phase parameter for every output file produced with 'get_snid.sh' and writes the spectrum's file
# name and phase in 'outputs_phase.txt'

# Import external libraries
import os

# Create the 'outputs_phase.txt' file and open it in writting mode
file_txt = open("outputs_phase.txt", "w")

# Go to the directory of the output SNID files
dir = '/home/cris/outputs/'
os.chdir(dir)

# For every file in the directory
for file in os.listdir():
    # Set the path and open fer reading the file
    file_path = dir + file
    f = open(file_path)
    content = f.readlines()

    # Go to the phase section of the file and read the first line
    line_counter = 70
    line = content[line_counter]
    line = " ".join(line.split())
    # The grade column is the 10th
    grade = line.split(' ')[9]
    # If the phase's grade is not 'good' (i.e., 'bad'), go to the next line
    while grade != 'good':
        print(line_counter)
        line_counter = line_counter + 1
        print(line_counter)
        line = content[line_counter]
        line = " ".join(line.split())
        grade = line.split(' ')[9]
        print(grade)
    # Select the phase value for the row with 'good' grade
    age = line.split(' ')[7]
    # close file
    f.close()

    # write in 'outputs_phase.txt' the name's file and phase of this spectrum
    new_line = '{}; {}\n'.format(file, age)
    file_txt.write(new_line)

# close file
file_txt.close()