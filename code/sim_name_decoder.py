from functions import *

names = ['Name_sim1_scen_MQ_del2_M_28-30.dfsu', 'Name_sim3_scen_Q10_del2_M_28-30.dfsu',
        'Name_sim1_scen_MQ_del2_M_28-30.m21fm', 'Name_sim3_scen_Q10_del2_M_28-30.m21fm']

for name in names:
    print(sim_name_decoder(name, 0))
    print(sim_name_decoder(name, 1))
    print(sim_name_decoder(name, 2))
    print(sim_name_decoder(name, 3))
    print(sim_name_decoder(name, 4))
    print(sim_name_decoder(name, 5))
    print(sim_name_decoder(name, 6))
    print(sim_name_decoder(name, 7))
