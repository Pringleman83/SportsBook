# Useful functions
from prettytable import PrettyTable
import json

def home_or_away(either = True, menu = True):
    """
    Takes in optional booleans for either and menu (default is true).
    Asks the user to enter h, a, e (if either is True) or m (if menu is True).
    Validates the input and returns "Home", "Away", "Either" or "Exit".
    """
    while True:
        if either and menu:
            print("Enter H, A, E or M to return to previous menu making no changes.")
        elif menu:
            print("Enter H, A or M to return to previous menu making no changes.")
        elif either:
            print("Enter H, A or M to return to previous menu making no changes.")
        else:
            print("Enter H, or A.")
            
        s = input().lower()
        if s == "h":
            team = "Home"
            break
        elif s == "a":
            team = "Away"
            break
        elif s == "e" and either:
            team = "Either"
            break
        elif s == "m" and menu:
            team = "Exit"
            break
    return team

def input_number():
    """
    Asks the user to enter a number.
    Validates the input and returns the given number.
    """
    while True:
        number = input()
        if is_number(number):
            number = int(number)
            break
    return number

def remove_duplicates(old_list):
    """
    Takes a list.
    Returns a new list with all duplicates removed.
    """
    new_list = []
    for item in old_list:
        if item not in new_list:
            new_list.append(item)
    return new_list

def import_json_file(file_name = "ask", display_updates = True):

    """
    If no arguments are passed, asks for a filename to import.
    Will otherwise use the passed argument for the filename.
    Loads the filename.json and returns it as a dictionary.
    """
    if file_name == "ask":
        print("\nEnter the name of the file you wish to load (no extension required): ", end="")
        file_name = input()
    
    if display_updates:
        print("---LOADING...---")
    try:
        with open(file_name + ".json") as infile:
            loaded_json = json.load(infile)
            if display_updates:
                print("---LOADED---")
        return loaded_json
    except FileNotFoundError:
        print('File not found')

    input("Press enter to continue")

def export_data(data, file_extension = "choose"):
    """
    Saves any passed data to a file.
    The file_extension parameter, if passed, determines the file type.
    If it is "json" or "xls", the data will be saved as that file type.
    If it is "choose", the user will be given the coice of the two formats.
    Data passed to be saved in xls format must be a Pandas dataframe object.
    """
    
    if file_extension == "choose":
        # Give the user a choice of file types
        choice = ""
        valid_options = ["1","2","m"]
        print("\nExport data: Please select one of the following file types: ")
        print("1: JSON \n2: Excel \n\nOr enter M to return to the previous menu")
        while choice not in valid_options:
            choice = input().lower()
        if choice == "m":
            print("No file saved.")
            return
        elif choice == "1":
            file_extension = "json"
        elif choice == "2":
            file_extension = "xls"
    
    print("\nEnter a file name (no extension required): ", end="")
    file_name = input()
    print("---SAVING...---")
    
    if file_extension == "json":    

        # Add file prefix to prevent any nastiness with moving around the file system.
        with open("SB_" + file_name + ".json", "w") as outfile:
            json.dump(data, outfile, indent=1)
        print(f"---File SB_{file_name}.json SAVED---")
        input("Press enter to continue")
        return
    
    elif file_extension == "xls":
        
        # Save Excel file
        data.to_excel("SB_" + file_name + ".xls")
        
        print(f"---File SB_{file_name}.xls SAVED---")
        input("\nPress enter to continue\n")
        return
    print("\nSomething went wrong - file not saved.\n")
    return
    
def is_number(s) -> bool:

    """
    Tests if the value passed is a number.
    Returns True or False.
    """
    if isinstance(s, str):
        s = s.strip()
        return s.isnumeric()
    return isinstance(s, int) or isinstance(s, float)

def valid_input(selection, options) -> bool:
    """
    Takes the user's selection and a list of valid options.
    Returns True if the selection is in the list.
    Returns False if it's not.
    """

    if isinstance(selection, str):
        if selection.isnumeric():
            selection = int(selection)
    return selection in options


def custom_pretty_print(data, k):
    """Takes any given dictionary or list {data} and prints its keys (in the case of a dictionary)
        or values (in the case of a list) in k columns.

    data = dictionary or list
    k = key or number of columns wanted


    e.g:

    my_dictionary = {"1 English Premier League": ["1", "england/premier-league/", 20],
                    "2 English Championship": ["2", "england/championship/", 24],
                    "3 English League One": ["3", "england/league-one/", 24],
                    "4 English League Two": ["4", "england/league-two/", 24],
                    "5 Spanish Primera": ["5", "spain/primera-division/", 20],
                    "6 Spanish Segunda": ["6", "spain/segunda-division/", 22],
                    "7 Spanish Segunda B": ["7", "spain/segunda-b/", 20],
                    "8 French Lique 1": ["8", "france/ligue-1/", 20]}

    -- custom_pretty_print(my_dictionary, 3):

    would produce the following print ->

        +--------------------------+------------------------+----------------------+
        | 1 English Premier League | 2 English Championship | 3 English League One |
        | 4 English League Two     | 5 Spanish Primera      | 6 Spanish Segunda    |
        | 7 Spanish Segunda B      | 8 French Lique 1       |                      |
        +--------------------------+------------------------+----------------------+


    -- custom_pretty_print(my_dictionary, 2):

    would produce the following print ->

        +--------------------------+------------------------+
        | 1 English Premier League | 2 English Championship |
        | 3 English League One     | 4 English League Two   |
        | 5 Spanish Primera        | 6 Spanish Segunda      |
        | 7 Spanish Segunda B      | 8 French Lique 1       |
        +--------------------------+------------------------+


    There are currently 2 hardcodded variables that could be changed if needed in the future.

    x.align 'l' this sets the alignment to left.
    column/row distribution, current distribution is

    1 2 3
    4 5 6

    rather than

    1 3 5
    2 4 6

    Any of this could be very well changed if needed, will probably de-hardcode this variables and make them needed or
    optional to the function in the future. Open issue or message Surister for any further info or request






     """

    def _get_k_sized_list(data, k):
        s_0 = 0
        s_1 = k
        l = []
        for _ in range(len(data)//k):

            if isinstance(data, dict):
                l.append(list(data.keys())[s_0:s_1])
            elif isinstance(data, list):
                l.append(data[s_0:s_1])
            s_0 += k
            s_1 += k
        
        # Add last items and blank items to ensure all items are displayed
        blanks = k - (len(data) % k)

        if isinstance(data, dict):
            l.append(list(data.keys())[s_0:len(data)])
        if isinstance(data, list):
            l.append(data[s_0:len(data)])
    
        for _ in range(blanks):     # This resolves the problem of having an odd list divided
                                    # in a even fashion (and the other way around)

            l[-1].append("")

        return l

    x = PrettyTable()
    for i in _get_k_sized_list(data, k):
        x.add_row(i)
        x.align = 'l'
        x.header = False
    print(x)
