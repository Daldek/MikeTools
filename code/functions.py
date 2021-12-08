import os
import pandas as pd
import geopandas as gpd
from mikeio import Dfs2, Dfsu
import rasterio
from rasterio.transform import from_origin
from classes import AscFile


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


def dfs2_to_ascii(in_ascii, out_ascii, in_dfs2, item_number, is_int):
    print('Reading dfs2...')
    dfs = Dfs2(in_dfs2)
    ds = dfs.read()


    print("Reading ascii template...")
    ascii_template = AscFile(in_ascii)
    elevation = ds.tail(1)[item_number]  # Last timestep

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
