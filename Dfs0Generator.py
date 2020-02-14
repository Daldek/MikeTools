from datetime import datetime, timedelta
from mikeio.dfs0 import dfs0
import numpy as np

data = []
d = np.random.random([20])
data.append(d)
dfs = dfs0()
dfs.create(filename='RandomValues.dfs0',
           data=data,
           start_time=datetime(2020, 1, 1),
           dt=60)
