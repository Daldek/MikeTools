import os

# Basic functions

def log_reader(folder, include_subdirectories):
    def writer(path, f):
        with open(os.path.join(path, f), 'r') as log:
            lines = log.read().splitlines()
            status = lines[-1]
            status = status.replace('=', '').lower().strip()
            status = str(status) + '\t\t' + str(file.replace('.log', ''))
            status_list.append(status)

    # Write the results
    status_list = []

    # List all log files and save the last line to a list
    for root, dirs, files in os.walk(folder):
        for file in files:
            if include_subdirectories is False:
                if file.endswith('.log') and root == folder:
                    writer(root, file)
            else:
                if file.endswith('.log'):
                    writer(root, file)
    status_list.sort()
    return status_list


def mike_to_bat(folder):
    commands_list = []

    # commands to be written. Not that this function will only work with Mike 2019
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.m21fm') and root == folder:
                command = r'start /wait C:\"Program Files (x86)"\DHI\2019\bin\x64\MzLaunch.exe -gpu 1 -x ' \
                          + str(file)
                commands_list.append(command)
            if file.endswith('.m21') and root == folder:
                command = r'start /wait C:\"Program Files (x86)"\DHI\2019\bin\x64\MzLaunch.exe -exit -mpi 6 ' \
                          + str(file)
                commands_list.append(command)

    # creating a txt file
    bat = folder + "\\Launcher.bat"
    bat_writer = open(bat, "w+")

    # saving commands to file
    for command in commands_list:
        bat_writer.write('%s\r' % command)
    bat_writer.close()

    return commands_list
