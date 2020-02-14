# Prymitywne usprawnienie porownywania plikow symulacji, stworzone specjalnie
# konkretnych symulacji

import os

ParentFolder = input("Folder path ")

# Write the results
LogReporter = ParentFolder + "\\SimReporter.txt"
StatusWriter = open(LogReporter, "w+")

# List all log Files and save the last line to file
for root, dirs, files in os.walk(ParentFolder):
    for file in files:
        if file.endswith('.m21fm'):
            with open(os.path.join(root, file), 'r') as log:
                lines = log.read().splitlines()
                start_time = lines[56].replace(' ', '')
                time_steps = lines[58].replace(' ', '')
                ini_surf_type = lines[717].replace(' ', '')
                file_name_2d = 'none'
                reference_value = 'none'
                if ini_surf_type == 'type=3':
                    file_name_2d = lines[722].replace(' ', '')
                    reference_value = lines[753].replace(' ', '')
                StatusWriter.write(file + " " + start_time + '\r\n'
                + time_steps + '\r\n'
                + ini_surf_type + '\r\n'
                + file_name_2d + '\r\n'
                + reference_value + '\r\n'
                + '\r\n')

# Close the summary text file
StatusWriter.close()
