from functions import *

folder = r'C:\Users\PLPD00293\Desktop\log examples\m21fm'

# execution
commands_list = mike2bat(folder)

# creating a txt file
bat = folder + "\\Launcher.bat"
bat_writer = open(bat, "w+")

# Save the results to the txt file
for command in commands_list:
    bat_writer.write('%s\r\n' % command)
bat_writer.close()
