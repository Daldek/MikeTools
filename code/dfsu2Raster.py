import sys
from functions import *

# Input
folders_list = ['Klaralven_sim1_scen_MQ_del2_M_28-30.m21fm - Result Files',
                'Klaralven_sim2_scen_MQ_klimat_del2_M_28-30.m21fm - Result Files',
                'Klaralven_sim3_scen_Q10_del2_M_28-30.m21fm - Result Files',
                'Klaralven_sim4_scen_Q25_del2_M_28-30.m21fm - Result Files',
                'Klaralven_sim5_scen_Q50_del2_M_31-33.m21fm - Result Files',
                'Klaralven_sim6_scen_Q100-klimat_del2_M_31-33.m21fm - Result Files',
                'Klaralven_sim7_scen_Q200-klimat_del2_M_31-33.m21fm - Result Files',
                'Klaralven_sim8_scen_Q200_del2_M_31-33.m21fm - Result Files',
                'Klaralven_sim9_scen_BHF_del2_M_31-33.m21fm - Result Files',
                'Klaralven_sim10_scen_MQ_del1_M_28-30.m21fm - Result Files',
                'Klaralven_sim11_scen_MQ_klimat_del1_M_28-30.m21fm - Result Files',
                'Klaralven_sim12_scen_Q10_del1_M_28-30.m21fm - Result Files',
                'Klaralven_sim13_scen_Q25_del1_M_28-30.m21fm - Result Files',
                'Klaralven_sim14_scen_Q50_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim15_scen_Q100-klimat_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim16_scen_Q200-klimat_del12_M_31-33.m21fm - Result Files',
                'Klaralven_sim17_scen_Q200_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim18_scen_BHF_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim19_scen_Q100-klimat_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim20_scen_Q200-klimat_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim21_scen_Q200_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim22_scen_BHF_del1_M_31-33.m21fm - Result Files',
                'Klaralven_sim27_scen_MQ_del3_M_28-30.m21fm - Result Files',
                'Klaralven_sim28_scen_MQ_klimat_del3_M_28-30.m21fm - Result Files',
                'Klaralven_sim29_scen_Q10_del3_M_28-30.m21fm - Result Files',
                'Klaralven_sim30_scen_Q25_del3_M_28-30.m21fm - Result Files',
                'Klaralven_sim31_scen_Q50_del3_M_31-33.m21fm - Result Files',
                'Klaralven_sim32_scen_Q100-klimat_del3_M_31-33.m21fm - Result Files',
                'Klaralven_sim33_scen_Q200-klimat_del3_M_31-33.m21fm - Result Files',
                'Klaralven_sim34_scen_Q200_del3_M_31-33.m21fm - Result Files',
                'Klaralven_sim35_scen_BHF_del3_M_31-33.m21fm - Result Files']

for folder in folders_list:
    input_dfsu = 'C:\\Users\\PLPD00293\\Desktop\\Klaralven\\' + folder + '\\Map_last.dfsu'
    cell_size = 6
    items = ['Current speed', 'Surface elevation', 'Total water depth']
    output_folder = r'C:\\Users\\PLPD00293\\Desktop\\Klaralven\\' + folder
    model = sim_name_decoder(folder, 5)
    scenario = sim_name_decoder(folder, 3)
    print("Input Dfsu: " + input_dfsu)
    print("Model: " + model)
    print("Scenario: " + scenario)

    # new model's name
    if model == 'del1':
        model = 'B'
    elif model == 'del2':
        model = 'A'
    elif model == 'del3':
        model = 'C'
    else:
        pass

    # new scenario's name
    if scenario == 'MQ':
        scenario = 'sc1'
    elif scenario == 'MQ_klimat':
        scenario = 'sc2'
    elif scenario == 'Q10':
        scenario = 'sc3'
    elif scenario == 'Q25':
        scenario = 'sc4'
    elif scenario == 'Q50':
        scenario = 'sc5'
    elif scenario == 'Q100-klimat':
        scenario = 'sc6'
    elif scenario == 'Q200-klimat':
        scenario = 'sc7'
    elif scenario == 'Q200':
        scenario = 'sc8'
    elif scenario == 'BHF':
        scenario = 'sc9'
    else:
        pass

    print("New model name: " + model)
    print("New scenario name: " + scenario)

    for item in items:
        # new item's name
        if item == 'Current speed':
            out_item = 'hast'
        elif item == 'Surface elevation':
            out_item = 'moh'
        elif item == 'Total water depth':
            out_item = 'djup'
        else:
            out_item = item

        print("Item: " + item)
        output_dfs2 = output_folder + r"\\" + model + '_' + scenario + '_' + out_item + '.tif'
        print("Output dfs2 file: " + output_dfs2)
        dfsu_to_geotiff(input_dfsu, item, cell_size, cell_size, 3008, output_dfs2)
