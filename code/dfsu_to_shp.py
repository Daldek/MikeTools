from functions import *

input_file = input('Input Dfsu file: ')  # an absolute path
item = input('Item: ')
output_folder = input('Output folder: ')  # an absolute path
prefix = input('The prefix to be added to the output file name: ')
time_step = input('Time step: ')  # integer, counted from 0

dfsu_to_shp(input_file, item, output_folder, int(time_step))
