from classes import *

in_ascii = input("ASCII file path: ")
proj = input("Projection (OGC WKT format): ")
item = input("Item (not yet supported, leave blank): ")

in_ascii_path = in_ascii.replace('"','')

new_dfs2 = MyDfs2(in_ascii_path, proj, item)
new_dfs2.create_dfs2()
