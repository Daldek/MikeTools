from functions import *

in_dfs2_list = []

while True:
    in_dfs2 = input("Dfs2 file path (press 'enter' to quit): ").replace('"', '')
    if in_dfs2 == '':
        break
    if os.path.isfile(in_dfs2) is False:
        print("The path entered is not a file.")
        quit()
    in_dfs2_list.append(in_dfs2)

if not in_dfs2_list:
    print("Nothing to do. The user has not entered a file path.")
    quit()

in_ascii = input("ASCII template: ").replace('"', '')
out_folder = os.path.join(os.path.dirname(in_dfs2_list[0]), 'dfs2_to_ascii')

is_int = input("Do you want to force integer values in the result files? (type 'y' to confirm): ").lower()
if is_int == 'y':
    is_int = True
else:
    is_int = False

try:
    os.mkdir(out_folder)
except FileExistsError:
    print(f"The destination folder already exists \n{out_folder}")
else:
    print(f"A new folder has been created \n{out_folder}")

for dfs2_file in in_dfs2_list:
    print(f"\nInpust dfs2 file: {dfs2_file}")
    out_ascii = os.path.join(out_folder, os.path.split(dfs2_file)[1].replace('.dfs2', '.asc'))
    print(f"Output ascii file: {out_ascii}")
    dfs2_to_ascii(dfs2_file, in_ascii, out_ascii, is_int)
