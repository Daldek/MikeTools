"""
Author: Elena Marchenko (elena.marchenko@wsp.com)
"""

import sys
import Functions

# Input
input_dfsu = r'C:\\Users\\PLPD00293\\Desktop\\Espoo\\Map.dfsu'
timestep = 20
cell_size = 2
items = ['Current speed', 'Current direction', 'Total water depth']
output_folder = 'C:\\Users\\PLPD00293\\Desktop\\Espoo'

to_integer = 0  # 0 - float, 1 - convert output to integer

# Execute
a = input_dfsu.rfind(r'\\')
input_name = input_dfsu[a+1:-5]
print(input_name)

# [grids, x, y, proj] = Functions.read_dfsu(input_dfsu, items, cell_size, timestep)
try:
    [grids, x, y, proj] = Functions.read_dfsu(input_dfsu, items, cell_size, timestep)
except:
    sys.exit('Cannot read the input DFSU file. Check the file for occasional errors.')

for n, i in enumerate(items):
    output_name = output_folder + r'/' + input_name + '_' + str(cell_size) + 'm_ts' + str(timestep) + '_' + i + '.tiff'
    output_name = output_name.replace(' ', '_')
    grid = grids[n]
    Functions.write_geotiff(grid, x, y, output_name, cell_size, proj, to_integer)
