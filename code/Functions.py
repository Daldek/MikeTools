import numpy as np
from dhitools import dfsu
from osgeo import gdal, ogr, osr


def read_dfsu(infile, items, cell_size, timestep):
    print('Reading dfsu ...')
    data = dfsu.Dfsu(infile)
    print(data.summary())
    print('Rasterazing dfsu ...')
    data.grid_res(res=cell_size)

    grids = np.empty([len(items), data.grid_x.shape[0], data.grid_x.shape[1]])
    for n, i in enumerate(items):
        grid = data.gridded_item(item_name=i, tstep_start=timestep, res=cell_size)
        grid = np.around(grid, decimals=1)
        grids[n] = grid[0]
        print('Gridded data for ' + i + ' has been created')

    return grids, data.grid_x, data.grid_y, data.projection


def write_geotiff(data_array, x, y, raster_name, cell, proj, to_integer):
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
