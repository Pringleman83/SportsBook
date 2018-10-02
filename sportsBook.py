from footballMenu import football_menu
from commonFunctions import *

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


def tennis():
    """
    Placeholder for Tennis selection.
    Serves no function except for menu testing.
    """
    print("The tennis option is a placeholder for testing. The option is not currently available. \n\n")

# options list can only now be declared (after its functions have been)


options = [[1, "Football", football_menu], [2, "Tennis", tennis], ["Q", "Quit"]]


def main_menu(options):
    """
    Main menu function
    Offers all options in the options list (no need to edit this function)
    Returns the selected funtion to run.
    """
    while True:
        print("Welcome to SportsBook - A sports analysis tool.")
        print("Please select from one of the following sports:")
        # Display all options
        for option in options:
            print(str(option[0]) + " " + str(option[1]))
        # Take user selection
        while True:
            print("Enter option: ")
            selected = input()
            # Quit option
            if selected.lower() == "q":
                exit()
            # If a number has been entered, convert the string to an integer
            if is_number(selected):
                selected = int(selected)
                # If the selection is in the list break out of the infinite loop
                if selected in range(len(options)) and selected != 0:
                    break
        # Having broken out of the loop, run the selected function
        if selected == options[0][0]:
            league_data = {}
            football_menu(league_data)
        if selected == options[1][0]:
            tennis()

# As this is the main file, call up the main menu


main_menu(options)
