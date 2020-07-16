from datetime import datetime, timedelta
from mikeio.dfs0 import Dfs0
import numpy as np

data = []
data_value_type = [0, 1]
d = np.random.random([20])
data.append(d)
dfs = Dfs0()
dfs.create(filename='RandomValues.dfs0',
           data=data,
           start_time=datetime(2020, 1, 1),
           dt=60,
           variable_type=[100000],
           unit=[1000],
           data_value_type=[0]
           )
