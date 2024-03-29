import numpy as np
import pandas as pd
import mikeio
from mikeio import Dfs2
from mikecore.eum import eumUnit
from mikeio.eum import EUMType, ItemInfo

class AscFile():
    '''This class analyzes an ASCII file header. This analysis can be used to compare 2
    (or more) ASCII files used in Mike21 models or to create a numpy array to create
    a new Dfs2 file'''
    def __init__(self, path):
        """Class initialization
        :param path: path to an ASCII (ESRI grid) file"""
        self.path = path


    def get_properties(self):
        '''Getting data from ASCII file and extracting raw numbers'''
        self.ncols = ''
        self.nrows = ''
        self.xllcorner = ''
        self.yllcorner = ''
        self.cellsize = ''
        self.nodata_value = ''
        
        with open(self.path, "r") as f:
            raw_header = [next(f) for x in range(6)]
            self.header = [x[:-1] for x in raw_header]  # removing '\n' for the end of each line
            values = [float(list(item.split(' '))[-1]) for item in self.header]  # extraction of values

        self.ncols, self.nrows, self.xllcorner,self.yllcorner, self.cellsize, self.nodata_value = values
        return values  # should I return properties as a list?


    def get_data(self):
        '''The get_data function returns a 1D list'''
        with open(self.path) as f:
            raw_data = f.read().splitlines()[6:]
            split_data = [list(line.split(' ')) for line in raw_data]
            no_empty_strings = [[x for x in y if x] for y in split_data]
            flattened_data = list(np.concatenate(no_empty_strings).flat)
            float_data = [float(x) for x in flattened_data]

        self.data = float_data
        return self.data


    def get_data_as_3D_numpy_array(self):
        '''A 3D array was used in Mikeio's example. Two dimensions relate to X and Y coordinates,
        while the third dimension relates to time and - it seems to me - is required
        to specify at least one time step when creating a Dfs2 file.'''
        self.get_data()
        self.array = np.array(self.data).reshape(1, int(self.nrows), int(self.ncols))
        self.array[self.array == self.nodata_value] = 'nan'
        return self.array


class MyDfs2(AscFile):
    '''Creating Dfs2 file based on an ascii file'''
    def __init__(self, path, projection, item):
        super().__init__(path)
        self.projection = projection
        self.item = item


    def create_dfs2(self):
        self.get_properties()
        self.get_data_as_3D_numpy_array()
        grid = mikeio.Grid2D(x0 = self.xllcorner,
                             dx = self.cellsize,
                             y0 = self.yllcorner,
                             dy = self.cellsize,
                             nx = int(self.ncols),
                             ny = int(self.nrows),
                             projection = self.projection)
        da = mikeio.DataArray(data = np.flip(self.array, 1),
                                   geometry = grid,
                                   time = pd.date_range("2100",periods=1,freq='D'),
                                   item = mikeio.ItemInfo("Example", mikeio.EUMType.Elevation))
        
        ds = mikeio.Dataset([da])
        dfs2_name = self.path[:-3] + "dfs2"
        ds.to_dfs(dfs2_name)


class MyASCII():
    '''Creating ASCII file based on Dfs2'''
    def __init__(self, path):
        self.path = path

    
    def get_properties(self):
        self.dfs2 = Dfs2(self.path)
        # self.ds = self.dfs2.read()[0]  # currently desiged to only read simple dfs2 files
        # self.da = mikeio.dataset.Dataset(self.ds)
        self.ncols = self.dfs2.nx
        self.nrows = self.dfs2.ny
        self.xllcorner = self.dfs2.origin[0] - (self.dfs2.dx / 2)
        self.yllcorner = self.dfs2.origin[1] - (self.dfs2.dy / 2)
        self.cellsize = self.dfs2.dx  # hope this value is same as dy
        self.nodata_value = -9999  # default value, most common as I know
        # self.geometry = self.dfs2.geometry
        return 1

    
    def write_asc(self):
        self.get_properties()
        asc_path = self.path[:-4] + "asc"
        ds = self.dfs2.read()[0]  # currently desiged to only read simple dfs2 files
        da = mikeio.dataset.Dataset(ds)
        data = np.flip(np.squeeze(np.nan_to_num(da.to_numpy(), nan = self.nodata_value)), 0)
        with open(asc_path, 'w') as file_obj:
            file_obj.write('ncols ' + str(self.ncols) + '\n')
            file_obj.write('nrows ' + str(self.nrows) + '\n')
            file_obj.write('xllcorner ' + str(self.xllcorner) + '\n')
            file_obj.write('yllcorner ' + str(self.yllcorner) + '\n')
            file_obj.write('cellsize ' + str(self.cellsize) + '\n')
            file_obj.write('NODATA_value ' + str(self.nodata_value) + '\n')
            for row in data:
                for value in row:
                    file_obj.write(str(value) + ' ')
                file_obj.write('\n')
        return 1
