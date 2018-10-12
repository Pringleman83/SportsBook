from footballMenu import football_menu
from commonFunctions import is_number
import argparse
from sys import exit

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


class MainMenu(object):
    """
    Main menu class object. Takes user input and moves onto the next menu.
    """
    def __init__(self):

        self.parse_args()

    def tennis(self):
        """
        Placeholder for Tennis selection.
        Serves no function except for menu testing.
        """
        print("The tennis option is a placeholder for testing.")
        print("The option is not supported in this build. \n\n")

    def football(self):
        """
        Just calls the imported football_menu() function, so that if this
        functionality changes in future it's easy to change once
        rather than repeating ourselves throughout the code.
        """

        league_data = {}
        fixtures = []
        predictions = []

        football_menu(league_data, fixtures, predictions)

    def parse_args(self):
        """"
        Parses the command line arguments, so that power-users can
        skip the menus. Currently very bare-bones.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-s', '--sport', help="The sport you wish to analyse.")

        self.args = parser.parse_args()

    def display_menu(self):
        """
        Main menu function
        Offers all options in the options list.
        Returns the selected function to run.
        """
        options = {
            1: "Football",
            2: "Tennis",
        }
        # If the user picked a sport by CLI argument, skip the main menu.
        # This should be refactored to use the options dict, probably.
        if self.args.sport:
            if self.args.sport == "football":
                self.football()
            elif self.args.sport == "tennis":
                self.tennis()
            else:
                print("{} is not currently a supported sport."
                      .format(self.args.sport))
                return

        print("Welcome to SportsBook - A sports analysis tool.")
        while True:
            print("Main Menu")
            print("---------")
            print("Please select from one of the following sports:")
            # Display all options
            for key in options:
                print("{}) {}".format(key, options[key]))
            print("q) Quit")
            # Take user selection
            while True:
                selected = input("Enter option: ")
                # Quit option
                if selected.lower() == "q":
                    exit()
                # If a number has been entered,
                # convert the string to an integer.
                if is_number(selected):
                    selected = int(selected)
                    # If selected is a number,
                    # check to see if it is a valid key.
                    try:
                        if options[selected] == "Football":
                            self.football()
                        elif options[selected] == "Tennis":
                            self.tennis()
                    except KeyError:
                        # If it's not valid, go back to the beginning.
                        break
                    # If we got this far, go back to the beginning.
                    break


mainmenu = MainMenu()
mainmenu.display_menu()
