import os
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime
import re
from dhitools import dfsu
from mikeio import Dfs2, Dfsu, Mesh, Dataset
from mikeio.eum import EUMType, EUMUnit, ItemInfo
from mikeio.spatial import Grid2D
from osgeo import gdal, ogr, osr
import rasterio
from rasterio.transform import from_origin
import xarray as xr
from classes import AscFile


def dfs2_to_ascii(in_dfs2, in_ascii, out_ascii, is_int):
    print('Reading dfs2...')
    dfs = Dfs2(in_dfs2)
    ds = dfs.read()

    print("Reading ascii template...")
    ascii_template = AscFile(in_ascii)
    elevation = ds['Grid Data']

    print("ASCII file writing in progress...")
    with open(out_ascii, 'w') as file_object:
        for attribute in ascii_template.get_properties():
            file_object.write(attribute + "\n")
        for row in elevation[0]:
            for value in row:
                if is_int is False:
                    file_object.write(str(value) + ' ')
                else:
                    file_object.write(str(int(value)) + ' ')
            file_object.write('\n')

    print("ASCII file has been saved.")
    return 1


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
    return commands_list


def dfsu_to_shp(dfsu_path, item_name, output_folder, time_step):
    # decode simulation name
    sim_name = str(dfsu_path).split('\\')[-1:][0].replace(".dfsu", "")
    print("Simulation name: " + str(sim_name))

    # read data
    dfsu_file = Dfsu(dfsu_path)
    print(dfsu_file)
    ds = dfsu_file.read()
    item = ds[item_name][time_step]
    print("Data have been read")

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
    gfd.to_file(str(output_folder) + "\\" + str(sim_name) + r"_" + str(item_name) + r".shp")
    print("Shapefile has been exported\nDone!")


def dfsu_to_dfs2(input_dfsu, item_name, dx, dy, output_dfs2):
    # read Dfsu file
    dfs = Dfsu(input_dfsu)
    ds = dfs.read(items=[item_name])
    print("Data have been read")

    # interpolate
    g = dfs.get_overset_grid(dxdy=(dx, dy), buffer=-1e-2)
    interpolant = dfs.get_2d_interpolant(g.xy, n_nearest=1)
    dsi = dfs.interp2d(ds, *interpolant, shape=(g.ny, g.nx))
    print("Data have been interpolated")

    # write to Dfs2
    dsi.flipud()
    dfs2 = Dfs2()
    coordinate = [dfs.projection_string, g.x0, g.y0, 0]
    dfs2.write(output_dfs2, data=dsi, coordinate=coordinate, dx=g.dx, dy=g.dy)
    print("Dfs2 file has been exported\nDone!")
    return g.x0, g.y0


def dfsu_to_geotiff(input_dfsu, item_name, dx, dy, epsg_code, output_tiff):
    # coordinate system
    output_coord = 'EPSG:' + str(epsg_code)

    # read a Dfsu file
    dfs = Dfsu(input_dfsu)
    ds = dfs.read(items=[item_name])
    print("Data have been read")

    # interpolation
    g = dfs.get_overset_grid(dxdy=(dx, dy), buffer=-1e-2)
    interpolant = dfs.get_2d_interpolant(g.xy, n_nearest=1)
    dsi = dfs.interp2d(ds, *interpolant, shape=(g.ny, g.nx))
    dsi.flipud()
    datgrid = dsi[item_name][0]
    print("Data have been interpolated")

    # write to a geotiff
    with rasterio.open(
     output_tiff,
     'w',
     driver='GTiff',
     height=g.ny,
     width=g.nx,
     count=1,
     dtype=datgrid.dtype,
     crs=output_coord,
     transform=from_origin(g.bbox[0], g.bbox[3], dx, dy),
     nodata=-9999
     ) as dst:
        dst.write(datgrid, 1)
    print("GeoTiff file has been exported\nDone!")
    return g.x0, g.y0


def dfs2_to_netcdf(input_dfs2, x0, y0, output_netcdf):
    '''
    :param input_dfs2: input dfs2 file
    :param x0: xll coordinate
    :param y0: yll coordinate
    :param output_netcdf: output netcdf file
    :return: netCDF file that can be opened e.g. in QGIS
    '''

    # read Dfs2
    dfs = Dfs2(input_dfs2)
    ds = dfs.read()

    # set geometry
    nx = ds[0].shape[2]
    ny = ds[0].shape[1]
    x = [x0 + dfs.dx*i for i in range(nx)]
    y = [y0 + dfs.dy*i for i in range(ny)]

    # write to netCDF
    y = list(reversed(y))
    res = {}
    spdims = ["y", "x"]
    dims = spdims
    coords = {}

    coords["x"] = xr.DataArray(x, dims="x", attrs={"standard_name": "x", "units": "meters"})
    coords["y"] = xr.DataArray(y, dims="y", attrs={"standard_name": "y", "units": "meters"})

    for item in ds.items:
        v = item.name
        res[v] = xr.DataArray(np.squeeze(ds[v]), dims=dims,
                              attrs={'name': v,
                                     # TODO add standard name from https://cfconventions.org/standard-names.html
                                     'units': item.unit.name,
                                     'eumType': item.type,
                                     'eumUnit': item.unit})

    xr_ds = xr.Dataset(res, coords=coords)
    xr_ds.to_netcdf(output_netcdf)
    return 1
