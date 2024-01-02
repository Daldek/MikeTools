import os
from classes import *


path = input("Insert path to a dfs2 file or to a folder which containt such file(s): ")
path = path.replace('"', '')

if os.path.isfile(path):
    new_dfs2 = MyASCII(path)
    new_dfs2.write_asc()
    print(path)
else:
    for f in os.listdir(path):
        if f.endswith('.dfs2'):
            new_dfs2 = MyASCII(os.path.join(path, f))
            new_dfs2.write_asc()
            print(f)
