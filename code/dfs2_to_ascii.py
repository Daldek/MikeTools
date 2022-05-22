from classes import *

in_dfs2 = input("Dfs2 file path: ")
in_dfs2_path = in_dfs2.replace('"','')

new_dfs2 = MyASCII(in_dfs2_path)
new_dfs2.write_asc()
