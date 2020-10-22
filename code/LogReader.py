# Program sluzacy do sprawdzania czy obliczenia symulacji w folderach
# podrzednych zostaly zakonczone sukscesem, porazka czy wciaz trwaja

import os

ParentFolder = input("Folder path ")

# Write the results
LogReporter = ParentFolder + "\\LogReporter.txt"
StatusWriter = open(LogReporter, "w+")

# List all log Files and save the last line to file
for root, dirs, files in os.walk(ParentFolder):
    for file in files:
        if file.endswith('.log'):
            with open(os.path.join(root, file), 'r') as log:
                lines = log.read().splitlines()
                status = lines[-1]
                StatusWriter.write(file + '\t' + status + '\r\n')

# Close the summary text file
StatusWriter.close()
