from functions import *

input_dfsu = input('Input dfsu file: ')
item_name = input('Item: ')
cell_size = int(input('Cell size: '))
epsg_code = int(input('EPSG: '))

output_raster = input_dfsu.replace(".dfsu", "_") + item_name.replace(" ", "-").lower() + r".tif"
dfsu_to_geotiff(input_dfsu, item_name, cell_size, cell_size, epsg_code, output_raster)
print("Done\n")
