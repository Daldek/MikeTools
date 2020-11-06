from functions import *
import time
import sys

# user input
folder = input('Directory path containing log files: ')
sub_dirs = input('Include subdirectories?: (y/n) ')

# checking if subfolders should be included
if sub_dirs.lower() == 'y':
    sub_dirs = True
elif sub_dirs.lower() == 'n':
    sub_dirs = False
else:
    print('Incomprehensible answer!')
    time.sleep(3)
    sys.exit()

# execution
status_list = log_reader(folder, sub_dirs)

# creating a txt file
log_reporter = folder + "\\LogReporter.txt"
status_writer = open(log_reporter, "w+")

# Save the results to the txt file
for sim_status in status_list:
    status_writer.write('%s\r\n' % sim_status)
status_writer.close()
