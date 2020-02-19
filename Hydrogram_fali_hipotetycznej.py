# Wzory Punzeta
# Skrypt obliczajacy hydrogram fali hipotetycznej w zlewniach niekontrolowanych o powierzchni powyzej 50 km2,
# zlokalizowanych w zlewni gornej Wisly. Dane z projektu ze studiow (R. Stodolak, zbiorniki, I stopien IiGW)

import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from mikeio.dfs0 import dfs0

# Dane wejsciowe
H_max = 677.1  # Najwyzej polozony punkt zlewni
H_max_cieku = 525.0  # Maksymalna wysokosc cieku
H_min = 308.4  # Najnizej polozony puinkt zlewni, przekroj zamykajacy
L_cieku = 31.567  # Dlugosc cieku
L_sucha_dolina = 0.0  # Dlugosc suchej doliny
A_zlewni = 151.614  # Powierzchnia zlewni
P_roczny = 666  # Średni opad roczny
N_zlewni = 60  # Wskaznik nieprzepuszczalnosci wyrazony w procentach
V_Czerkeszyn = 0.48  # Predkosc splywu wg Czerkeszyna
N_ksztalt_fali = 1.5  # Wspolczynnik ksztaltu fali

# Obliczenie wspolczynnika zmiennocsci Cvmax
delta_W = H_max - H_min
c_v_max = (3.027 * np.power((delta_W / 1000), 0.173))/(np.power(A_zlewni, 0.102) * np.power(L_cieku, 0.066))

# Obliczenie fiMaxp%
p_proc = 0.1  # Obliczenia dla prawdopodobienstwa przewyzszenia przpelywu p = 0.1%
t = 0

if p_proc == 0.01:
    t = 3.718
elif p_proc == 0.1:
    t = 3.09
elif p_proc == 0.2:
    t = 2.878
elif p_proc == 0.5:
    t = 2.575
elif p_proc == 1:
    t = 2.326
elif p_proc == 2:
    t = 2.054
elif p_proc == 5:
    t = 1.645

fi_max_p = 1.0 + 0.944 * np.power(t, 1.48) * np.power(c_v_max, (0.144 * np.power(t, 0.895) + 1.0))

# Obliczenie Qmax50% wg wzoru karpackiego
I_cieku = (((H_max_cieku / 1000) - (H_min / 1000)) / L_cieku) * 1000  # Sredni spadek cieku, wyrazony w promilach

# Wzor dla zlewni gorskich
q_max_50 = (0.00166 * np.power(A_zlewni, 0.747) * np.power(P_roczny, 0.536) * np.power(N_zlewni, 0.603))\
           / np.power(I_cieku, 0.075)

# Wzor dla zlewni wyzynnych
# q_max_50 = 0.00033 * np.power(A_zlewni, 0.872) * np.power(P_roczny, 1.065) * np.power(N_zlewni, 0.07)\
#            * np.power(I_cieku, 0.089)

# Obliczenie przpelywu o zadanym prawdopodobienstwie przewyzszenia
q_max_p = q_max_50 * fi_max_p

# Hydrogram fali hipotetycznej
# Czas koncentracji, metoda Rietza - Krepsa
tk = (L_cieku + L_sucha_dolina) / (3.6 * V_Czerkeszyn)
tk_round = math.ceil(tk)

# Wspolczynnik alfa
alfa = np.log(2) / ((N_ksztalt_fali - 1) * tk)

timesteps_przybor = np.arange(0, tk, 1).tolist()
# timesteps_przybor.append(tk)
timesteps_opadanie = np.arange(tk_round, 100, 1).tolist()

q_przybor = []
q_opadanie = []

for timestep_przybor in timesteps_przybor:
    if timestep_przybor == 0:
        q_przybor.append(0)
    else:
        flow_przybor = q_max_p * np.power(np.sin((np.pi / 2) * (timestep_przybor / tk)), 2)
        q_przybor.append(flow_przybor)

for timestep_opadanie in timesteps_opadanie:
    flow_opadanie = q_max_p * np.power(2.71, (alfa * (-1)) * (timestep_opadanie - tk))
    q_opadanie.append(flow_opadanie)

q = q_przybor + q_opadanie
timesteps = timesteps_przybor + timesteps_opadanie

plt.plot(timesteps, q)
plt.show()

data = []
data.append(np.array(q))
dfs = dfs0()
dfs.create(filename='Punzet.dfs0',
           data=data,
           start_time=datetime(2020, 1, 1),
           dt=3600,
           names=['Flow'],
           title='Punzet')
