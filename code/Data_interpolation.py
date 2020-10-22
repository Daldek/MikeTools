# Author: Adam Ostafin (adam.ostafin@wsp.com), Piotr de Bever (piotr.de.bever@wsp.com)

import datetime
from datetime import datetime
import pandas as pd
import numpy as np

# Input file link
# input_excel = input("Paste excel file path ")  # input excel file location
input_excel = "C:\Work\python\_programy\proba_zmazania_hanby\deszcze.xlsx"

# excel_sheet_name = input("Paste sheet name with rain distribution ")  # excel sheet with rain distribution data
excel_sheet_name = "Sheet1"
time_step = 5  # input("Specify time step (in minutes) ")

data_frame = pd.read_excel(input_excel,
                           sheet_name=excel_sheet_name,
                           header=1,
                           usecols="B:C")  # it counts from 0, excluding workspace(columnes used for calculation)

test_date = data_frame["data"].tolist()
nonequidistant_time_list = []

test_rain = data_frame["mm"].tolist()
nonequidistant_rain_list = []
for rain_value in test_rain:
    nonequidistant_rain_list.append(rain_value)

#----------------------------date interpolation part----------------------------

for date_step in test_date:  # convert all list items to numbers
    # pandas timestamp to integer
    date_string = str(date_step)
    date_number = int(datetime.fromisoformat(date_string).timestamp())
    nonequidistant_time_list.append(date_number)

#test_date = nonequidistant_time_list

equidistant_time_list = np.arange(nonequidistant_time_list[0],
                                  nonequidistant_time_list[-1],
                                  (time_step*60))  # new list arrange with time step

final_date_list = []
for date_step in equidistant_time_list:  # convertion from numerical list to date list
    timestamp = datetime.fromtimestamp(date_step)
    equidistant_date = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    final_date_list.append(equidistant_date)

#-----------------------------rain interpolation part---------------------------

# interpolation function
def rain_interpolation(first_time_step, second_time_step, last_time_step,
                       rain_step_1, rain_step_2):
    rain_intensity = rain_step_1 \
                     + ((second_time_step - first_time_step)
                        / (last_time_step - first_time_step)) \
                     * (rain_step_2 - rain_step_1)
    return rain_intensity

# print(nonequidistant_rain_list)
# lower_boudary = 0
# upper_boundary = 1
count = 0
equidistant_rain_list = []

for non_eq_date_step in nonequidistant_time_list:
    eq_boundary_list = []
    # eq_date_list = [] CONTROL STEP
    if non_eq_date_step == nonequidistant_time_list[0]:
        count += 1

    else:
        date_lower_boundary = nonequidistant_time_list[(count - 1)]
        date_upper_boundary = nonequidistant_time_list[count]
        rain_lower_boundary = nonequidistant_rain_list[(count - 1)]
        rain_upper_boundary = nonequidistant_rain_list[count]

        # for eq_date_step in range(date_lower_boundary, date_upper_boundary, (time_step*60)):

        for eq_date_step in equidistant_time_list:
            if eq_date_step >= date_lower_boundary:
                if eq_date_step <= date_upper_boundary:
                    eq_boundary_list.append(eq_date_step)
                    # for eq_date_step2 in eq_boundary_list:  # CONTROL STEP convertion from numerical list to date list
                    #     timestamp = datetime.fromtimestamp(eq_date_step2)
                    #     equidistant_date = timestamp.strftime(
                    #         '%Y-%m-%d %H:%M:%S')
                    #     eq_date_list.append(equidistant_date)
        for eq_boundary_list_step in eq_boundary_list:  # equidistant rain value calculation
            eq_rain_value = rain_interpolation(
                date_lower_boundary, eq_boundary_list_step,
                date_upper_boundary,
                rain_lower_boundary, rain_upper_boundary)
            equidistant_rain_list.append(eq_rain_value)
        count += 1

print(len(equidistant_rain_list))
print(len(equidistant_time_list))
