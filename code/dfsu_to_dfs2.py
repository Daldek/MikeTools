from functions import *

input_dfsu = r"C:\Users\PLPD00293\Desktop\Klaralven_sim1_scen_MQ_del2_M_28-30.dfsu"
item_name = "Surface elevation"
cell_size = 50
output_dfs2 = r"C:\Users\PLPD00293\Desktop\surface_elevation_interpolated.dfs2"

tmp = dfsu_to_dfs2(input_dfsu, item_name, cell_size, cell_size, output_dfs2)
