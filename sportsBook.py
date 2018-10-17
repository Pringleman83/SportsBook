from utils import AbstractUtility
import argparse
from sys import exit

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


class Display:

    def __init__(self):
        pass


class MainMenu(AbstractUtility, ...):
    """
    Main menu class object. Takes user input and moves onto the next menu.
    """
    def __init__(self):
        super().__init__()
        self.running = True
        self.session = False
        self.main_options = ('tennis', 'football')

        self.parse_args()

    @staticmethod
    def _log(args):
        print(args)

    def tennis(self):
        """
        Placeholder for Tennis selection.
        Serves no function except for menu testing.
        """
        self._log("The tennis option is a placeholder for testing.")
        self._log("The option is not supported in this build. \n\n")

    def football(self):
        """
        Just calls the imported football_menu() function, so that if this
        functionality changes in future it's easy to change once
        rather than repeating ourselves throughout the code.
        """

        league_data = {}
        fixtures = []
        predictions = []
        self._log('football')
        #football_menu(league_data, fixtures, predictions)

    def parse_args(self):
        """"
        Parses the command line arguments, so that power-users can
        skip the menus. Currently very bare-bones.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-s', '--sport', help="The sport you wish to analyse.")

        self.args = parser.parse_args()

    def caller(self, n):

        return self.football() if n == 1 else self.tennis()

    def run(self):
        """
        Main menu function
        Offers all options in the options list.
        Returns the selected function to run.
        """

        self._log("Welcome to SportsBook - A sports analysis tool.")
        while self.running:

            self._log("Main Menu")
            self._log("---------")
            self._log("Please select from one of the following sports:")

            # Display all options

            for k, v in enumerate(self.main_options):
                self._log(f"{k}) {v}")
            self._log("q) Quit")

            self.session = True

            while self.session:
                selected_input = input("Enter option: ")
                if selected_input.lower() == "q":
                    exit()
                if self.is_number(selected_input):
                    if int(selected_input) in list(range(len(self.main_options))):
                        self.caller(int(selected_input))
                    else:
                        self._log('Selected input is not valid, please try again.')


app = MainMenu()
app.run()
