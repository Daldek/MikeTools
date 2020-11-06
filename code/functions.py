import os
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime
import re
from dhitools import dfsu
from mikeio import Dfs2, Dfsu
from mikeio.eum import EUMType, EUMUnit, ItemInfo
from osgeo import gdal, ogr, osr


def read_dfsu(infile, items, cell_size, timestep):
    # Elena's script
    print('Reading dfsu ...')
    data = dfsu.Dfsu(infile)
    print(data.summary())
    print('Rasterazing dfsu ...')
    data.grid_res(res=cell_size)

    grids = np.empty([len(items), data.grid_x.shape[0], data.grid_x.shape[1]])
    for n, i in enumerate(items):
        grid = data.gridded_item(item_name=i, tstep_start=timestep, res=cell_size)
        grid = np.around(grid, decimals=2)
        grids[n] = grid[0]
        print('Gridded data for ' + i + ' has been created')

    return grids, data.grid_x, data.grid_y, data.projection


def write_geotiff(data_array, x, y, raster_name, cell, proj, to_integer):
    # Elena's script
    if to_integer == 1:
        data_array = data_array[~np.isnan(data_array)].astype(int)
        raster_type = gdal.GDT_Int32
    else:
        raster_type = gdal.GDT_Float32
    cols = x.shape[1]
    rows = x.shape[0]
    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(raster_name, cols, rows, 1, raster_type)
    out_raster.SetGeoTransform((np.amin(x), cell, 0, np.amin(y), 0, cell))
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(data_array)
    out_raster.SetProjection(proj)
    outband.FlushCache()


def sim_name_decoder(input_name, group_number):
    """
    Online regex tester: https://regex101.com/
    Example 1: Name_sim1_scen_MQ_del2_M_28-30.dfsu
    Example 2: Name_sim3_scen_Q10_del2_M_28-30.dfsu

    #0 Whole expression
    #1 Prefix (name)
    #2 Simulation number
    #3 Scenario
    #4 Mesh version
    #5 Mesh version (if has a number)
    #6 Manning roughness
    # Extension
    """
    pattern = re.compile(
        r'([a-zA-Z]+)_sim(\d+)_scen_([a-zA-Z]+|[a-zA-Z]+\d+)_([a-zA-Z]+|[a-zA-Z]+-[a-zA-Z])(\d+|)_M_(\d+|\d+-\d+).('
        r'm21fm|dfsu)')
    matches = pattern.finditer(input_name)
    for match in matches:
        if group_number == 4 or group_number == 5:
            mesh_version = str(match.group(4)) + str(match.group(5))
            return mesh_version
        else:
            return match.group(group_number)


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


def dfsu2shp(dfsu_path, item_name, output_folder, prefix, time_step):
    # decode simulation name
    sim_name = str(dfsu_path).split('\\')[-1:][0]
    print("Simulation name: " + str(sim_name))
    sim_number = sim_name_decoder(sim_name, 2)
    print("Simulation number: " + str(sim_number))

    # read data
    dfsu_file = Dfsu(dfsu_path)
    print(dfsu_file)
    ds = dfsu_file.read()
    item = ds[item_name][time_step]
    print("Data has been read")

    # extract geometry
    shp = dfsu_file.to_shapely()
    poly_list = [p for p in shp]
    print("Geometry has been extracted")

    # create a geopandas dataframe
    df = pd.DataFrame({item_name: item})
    print("Data frame has been created")
    gfd = gpd.GeoDataFrame(df, geometry=poly_list)

    # save to shapefile
    item_name = item_name.lower()
    item_name = item_name.replace(" ", "-")
    gfd.to_file(str(output_folder) + "\\" + str(prefix) + "_sim_" + str(sim_number) + "_" + str(item_name)
                + "_vector_ts_" + str(time_step) + r".shp")
    print("Shapefile has been exported\nDone!")
