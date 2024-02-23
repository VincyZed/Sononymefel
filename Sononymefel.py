import argparse
import os
import sqlite3
import ast
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


parser = argparse.ArgumentParser(description='Sononymefel - A script to automatically tag your sample library in FL Studio using Sononym\'s database.')
parser.add_argument('dbfile_path', metavar='dbfile_path', type=str, help='The path to the Sononym database file. It is normally called "sononym.db" and should be at the root of your sample library.')
parser.add_argument('--fl_user_data_folder', metavar='', type=str, default=os.path.join(os.path.expanduser('~/Documents/Image-Line')),
                    help='The FL Studio User Data folder\'s location. If you have not changed it, it is located in Documents\\Image-Line. This default location will be used if this argument is not provided.')
parser.add_argument('--sample_library_folder', metavar='', type=str, default=None,
                    help='The root folder of your sample library. The location of the Sononym database file will be used if this argument is not provided.')

args = parser.parse_args()

# If the sample library folder is not provided, use the folder where the database file is located
if args.sample_library_folder is None:
    args.sample_library_folder = os.path.dirname(args.dbfile_path)

def get_user_confirmation():
    print(bcolors.WARNING + "WARNING: This operation will overwrite your existing tags.\nIt is strongly recommended make a backup of the Tags file if you have existing tags in case something goes wrong!\n" + bcolors.ENDC)
    while True:
        user_input = input("Are you sure you want to proceed? [y/n]: ").lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please type 'y' or 'yes' to continue, 'n' or 'no' to abort.")


def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list




clear_screen()
print(bcolors.OKBLUE + "=======================" + bcolors.ENDC)
print(bcolors.OKBLUE + "Welcome to Sononymefel!" + bcolors.ENDC)
print(bcolors.OKBLUE + "=======================\n" + bcolors.ENDC)

print(bcolors.UNDERLINE + "Sononym database file location:" + bcolors.ENDC + "        " + args.dbfile_path)
print(bcolors.UNDERLINE + "Sample library folder location:" + bcolors.ENDC + "        " + args.sample_library_folder)
print(bcolors.UNDERLINE + "FL Studio User Data folder location:" + bcolors.ENDC + "   " + args.fl_user_data_folder + "\n")


if (get_user_confirmation()):
    con = sqlite3.connect(args.dbfile_path)

    table_name = 'assets'

    # Fetch the rows
    query = f'SELECT filename, categories_VS FROM {table_name}' 

    cur = con.cursor()
    cur.execute(query)
    print("\n\nFetching database...")
    rows = cur.fetchall()


    # Fetch the list of tags
    query = f'SELECT DISTINCT categories_VS FROM {table_name}'
    cur.execute(query)
    tags = cur.fetchall()

    # Flatten the list since columns contain arrays
    flat_list = flatten([ast.literal_eval(tag[0]) for tag in tags if tag[0]])

    # Get unique values
    tag_list = set(flat_list)

    con.close()


    print("Writing tags file for the FL Studio Browser...")
    tags_file = open(args.fl_user_data_folder + '/FL Studio/Settings/Browser/Tags', 'w', encoding='utf-8')

    words_to_eliminate = {'Perc ':'', 'XFX ':'', 'Tone ':''}

    # Begin the top row with this
    tags_row = '@TagCase=*'

    for tag in tag_list:
        # Eliminate tag families
        for key, value in words_to_eliminate.items():
            tag = tag.replace(key, value)
        # Only put quotes around tags that have spaces in them
        if ' ' in tag:
            tags_row += ",\"" + tag + "\""
        else:
            tags_row += "," + tag

    tags_file.write(tags_row + "\n")

    for row in rows:
        # Trim the beginning and end
        row = str(row)[2:-3]
        for key, value in words_to_eliminate.items():
            row = row.replace(key, value)
        
        row = row.replace("/","\\")

        
        if "', '[" in row:
            tags = row.split("', '[", 1)[1]
            path = row.split("', '[", 1)[0]
        if  "\", '[" in row:
            tags = row.split("\", '[", 1)[1]
            path = row.split("\", '[", 1)[0]

        # Remove double-quotes from tags and make them lowercase
        tags = new_s = re.sub(r'\"(\w+)\"', r'\1', tags).lower()

        # Format and write the row to the tags file
        folder = args.sample_library_folder.lower()
        if not folder.endswith("\\"):
            folder += "\\"

        row = "\"" + folder + path + '\",' + tags + "\n"
        tags_file.write(row)


    tags_file.close()

    print(bcolors.OKGREEN + "\n\nTags file written successfully!\n" + bcolors.ENDC)
    input("Press any key to continue...")

else:
    print(bcolors.FAIL + "\nAborting..." + bcolors.ENDC)
