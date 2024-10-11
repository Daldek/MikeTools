from pathlib import Path
import numpy as np
import pandas as pd
import mikeio
from mikeio import Dfs2


class AscFile:
    """Class for analyzing and manipulating ASCII grid files used in Mike21 models.
    This class can compare generate random ASCII grids or create a numpy array for new Dfs2.
    """

    def __init__(
        self,
        path=None,
        ncols=None,
        nrows=None,
        xllcorner=None,
        yllcorner=None,
        cellsize=None,
        nodata_value=None,
        data=None,
        data_min=None,
        data_mean=None,
        data_max=None,
        data_std=None,
        data_variance=None,
    ):
        """Class initialization
        :param path: path to an ASCII (ESRI grid) file"""
        self.path = path
        self._ncols = ncols
        self._nrows = nrows
        self._xllcorner = xllcorner
        self._yllcorner = yllcorner
        self._cellsize = cellsize
        self._nodata_value = nodata_value
        self._data = data
        self._data_min = data_min
        self._data_mean = data_mean
        self._data_max = data_max
        self._data_std = data_std
        self._data_variance = data_variance

    def _validate_file(self):
        "Validate if the input file exists and if it's an asc file"
        f_path = Path(self.path)
        if not f_path.exists():
            raise FileNotFoundError(f"{self.path} does not exists!")
        if f_path.suffix != ".asc":
            raise ValueError(f"{self.path} in not an asc file!")

    def get_properties(self):
        """Retrieve properties from the ASCII file if not already set."""
        self._validate_file()
        if all(
            attr is None
            for attr in [
                self._ncols,
                self._nrows,
                self._xllcorner,
                self._yllcorner,
                self._cellsize,
                self._nodata_value,
            ]
        ):
            with open(self.path, "r", encoding="utf-8") as f:
                raw_header = [
                    next(f).strip() for _ in range(6)
                ]  # Use strip() to remove newlines
                values = [
                    float(item.split()[-1]) for item in raw_header
                ]  # Extract values directly

            (
                self._ncols,
                self._nrows,
                self._xllcorner,
                self._yllcorner,
                self._cellsize,
                self._nodata_value,
            ) = values
        return (
            self._ncols,
            self._nrows,
            self._xllcorner,
            self._yllcorner,
            self._cellsize,
            self._nodata_value,
        )

    def get_data(self):
        """Returns a flattened 1D list of data from the ASCII file."""
        if self._data is None:
            with open(self.path, encoding="utf-8") as f:
                raw_data = f.readlines()[6:]
                flattened_data = [
                    float(x) for line in raw_data for x in line.split() if x
                ]

            self._data = flattened_data
        return self._data

    def get_data_as_3d_numpy_array(self):
        """Converts the data into a 3D numpy array suitable for Dfs2 files.
        The array dimensions correspond to time, rows, and columns."""
        data = np.array(self.get_data())
        reshaped_data = data.reshape((1, int(self._nrows), int(self._ncols)))
        reshaped_data[reshaped_data == self._nodata_value] = np.nan
        self._data = reshaped_data
        return self._data

    def get_statistics(self):
        """Calculates basic statistics of the input asc file

        Returns:
            float: min, mean, max and variance values
        """
        if all(
            attr is None
            for attr in [
                self._data_min,
                self._data_mean,
                self._data_max,
                self._data_std,
                self._data_variance,
            ]
        ):
            self._data_min = np.min(self._data)
            self._data_mean = np.mean(self._data)
            self._data_max = np.max(self._data)
            self._data_std = np.std(self._data, mean=self._data_mean)
            self._data_variance = np.var(self._data, mean=self._data_mean)
        return (
            self._data_min,
            self._data_mean,
            self._data_max,
            self._data_std,
            self._data_variance,
        )

    def create_dfs2(self, projection):
        """Creates a Dfs2 file using properties from the ASCII file."""
        self.get_properties()
        grid = mikeio.Grid2D(
            x0=self._xllcorner,
            dx=self._cellsize,
            y0=self._yllcorner,
            dy=self._cellsize,
            nx=int(self._ncols),
            ny=int(self._nrows),
            projection=projection,
        )
        da = mikeio.DataArray(
            data=np.flip(self.get_data_as_3d_numpy_array(), 1),
            geometry=grid,
            time=pd.date_range("2100", periods=1, freq="D"),
            item=mikeio.ItemInfo("Example", mikeio.EUMType.Elevation),
        )

        ds = mikeio.Dataset([da])
        dfs2_name = self.path[:-3] + "dfs2"
        ds.to_dfs(dfs2_name)
        return dfs2_name

    @staticmethod
    def generate_random_grid(nrows=5, ncols=5, no_data_value=-9999):
        """Generates random 5x5 grid and saves it as an ASCII grid file"""
        data = np.random.randint(0, 100, size=(nrows, ncols))

        with open("random_grid.asc", "w", encoding="utf-8") as f:
            f.write(f"NCOLS {ncols}\n")
            f.write(f"NROWS {nrows}\n")
            f.write("XLLCORNER 0.0\n")
            f.write("YLLCORNER 0.0\n")
            f.write("CELLSIZE 1.0\n")
            f.write(f"NODATA_VALUE {no_data_value}\n")
            np.savetxt(f, data, fmt="%d")
        return f


class MyDfs2:
    """Class for creating an ASCII grid from a Dfs2 input file."""

    def __init__(self, path):
        """Initializes the MyASCII class.
        :param path: Path to the Dfs2 file."""
        self.path = path
        self._dfs2 = None
        self._ncols = None
        self._nrows = None
        self._xllcorner = None
        self._yllcorner = None
        self._cellsize = None
        self._nodata_value = None

    def _validate_file(self):
        "Validate if the input file exists and if it's a dfs2 file"
        f_path = Path(self.path)
        if not f_path.exists():
            raise FileNotFoundError(f"{self.path} does not exists!")
        if f_path.suffix != ".dfs2":
            raise ValueError(f"{self.path} in not a dfs2 file!")

    def get_properties(self):
        """Gets the Dfs2 file properties"""
        self._validate_file()
        if all(
            attr is None
            for attr in [
                self._ncols,
                self._nrows,
                self._xllcorner,
                self._yllcorner,
                self._cellsize,
                self._nodata_value,
            ]
        ):
            self._dfs2 = Dfs2(self.path)
            self._ncols = self._dfs2.nx
            self._nrows = self._dfs2.ny
            self._xllcorner = self._dfs2.origin[0] - (self._dfs2.dx / 2)
            self._yllcorner = self._dfs2.origin[1] - (self._dfs2.dy / 2)
            self._cellsize = self._dfs2.dx  # hope this value is same as dy
            self._nodata_value = -9999
        return (
            self._ncols,
            self._nrows,
            self._xllcorner,
            self._yllcorner,
            self._cellsize,
            self._nodata_value,
        )

    def write_asc(self):
        "Creates an ASCII grid based on the dfs2 input file"
        self.get_properties()
        asc_path = self.path[:-4] + "asc"
        ds = self._dfs2.read()[0]  # currently desiged to only read simple dfs2 files
        da = mikeio.dataset.Dataset(ds)
        data = np.flip(
            np.squeeze(np.nan_to_num(da.to_numpy(), nan=self._nodata_value)), 0
        )
        with open(asc_path, "w", encoding="utf-8") as file_obj:
            file_obj.write("ncols " + str(self._ncols) + "\n")
            file_obj.write("nrows " + str(self._nrows) + "\n")
            file_obj.write("xllcorner " + str(self._xllcorner) + "\n")
            file_obj.write("yllcorner " + str(self._yllcorner) + "\n")
            file_obj.write("cellsize " + str(self._cellsize) + "\n")
            file_obj.write("NODATA_value " + str(self._nodata_value) + "\n")
            for row in data:
                for value in row:
                    file_obj.write(str(value) + " ")
                file_obj.write("\n")
        return 1
