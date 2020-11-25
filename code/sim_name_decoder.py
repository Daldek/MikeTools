from functions import *

names = ['Name_sim1_scen_MQ_del2_M_28-30.dfsu', 'Name_sim3_scen_Q10_del2_M_28-30.dfsu',
         'Name_sim1_scen_MQ_del2_M_28-30.m21fm', 'Name_sim3_scen_Q10_del2_M_28-30.m21fm',
         'Klaralven_sim1_scen_MQ_del2_M_28-30.m21fm - Result Files',
         'Klaralven_sim2_scen_MQ_klimat_del2_M_28-30.m21fm - Result Files',
         'Klaralven_sim3_scen_Q10_del2_M_28-30.m21fm - Result Files',
         'Klaralven_sim4_scen_Q25_del2_M_28-30.m21fm - Result Files',
         'Klaralven_sim5_scen_Q50_del2_M_31-33.m21fm - Result Files',
         'Klaralven_sim6_scen_Q100-klimat_del2_M_31-33.m21fm - Result Files',
         'Klaralven_sim7_scen_Q200-klimat_del2_M_31-33.m21fm - Result Files',
         'Klaralven_sim8_scen_Q200_del2_M_31-33.m21fm - Result Files',
         'Klaralven_sim9_scen_BHF_del2_M_31-33.m21fm - Result Files']


for name in names:
    print(sim_name_decoder(name, 0))
    print(sim_name_decoder(name, 1))
    print(sim_name_decoder(name, 2))
    print(sim_name_decoder(name, 3))
    print(sim_name_decoder(name, 4))
    print(sim_name_decoder(name, 5))
    print(sim_name_decoder(name, 6))
    print(sim_name_decoder(name, 7))
