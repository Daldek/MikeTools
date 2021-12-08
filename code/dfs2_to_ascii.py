from functions import *

in_dfs2_list = []

in_ascii = input("ASCII template: ").replace('"', '')

while True:
    in_dfs2 = input("Dfs2 file path (press 'enter' to quit): ").replace('"', '')
    if in_dfs2 == '':
        break
    if os.path.isfile(in_dfs2) is False:
        print("The path entered is not a file.")
        quit()

    # Printing the header of the current dfs2 file
    print(Dfs2(in_dfs2).read())
    item_number = input('Item number to be converted (leave blank to pick first): ')
    if item_number == '':
        item_number = 0

    # Checking if a file should contain only integers
    is_int = input("Do you want to force integer values in the result files? (type 'y' to confirm): ").lower()
    if is_int == 'y':
        is_int = True
    else:
        is_int = False

    # Adding arguments to a tuple
    list_of_parameters = (in_dfs2, int(item_number), is_int)

    # Passing a set of arguments to a list
    in_dfs2_list.append(list_of_parameters)

# Script termination if no dfs2 file is provided for conversion
if not in_dfs2_list:
    print("Nothing to do. The user has not entered a file path.")
    quit()

# Creating a folder
out_folder = os.path.join(os.path.dirname(in_dfs2_list[0][0]), 'dfs2_to_ascii')
try:
    os.mkdir(out_folder)
except FileExistsError:
    print(f"The destination folder already exists \n{out_folder}")
else:
    print(f"A new folder has been created \n{out_folder}")

# Execution of the function
for list_of_arguments in in_dfs2_list:
    print(f"\nInput dfs2 file: {list_of_arguments[0]}")
    out_ascii = os.path.join(out_folder, os.path.split(list_of_arguments[0])[1].replace('.dfs2', '.asc'))
    print(f"Output ascii file: {out_ascii}")
    dfs2_to_ascii(in_ascii, out_ascii, *list_of_arguments)
