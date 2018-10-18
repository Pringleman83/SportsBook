from utils import AbstractUtility
from sport import Sport
import argparse

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


class Display:
    """ Extra Display utilities functions and placeholders"""
    def __init__(self):
        pass


class MainMenu(AbstractUtility):
    """
    Main menu class object. Takes user input and moves onto the next menu.
    """
    def __init__(self):
        super().__init__()
        self.running = True
        self.session = False
        self.main_options = ('Tennis', 'Football')
        self.parse_args()
        self.current_sport = None

    def parse_args(self):
        # parse_args function has to be review to whether it is useful or not

        """"
        Parses the command line arguments, so that power-users can
        skip the menus. Currently very bare-bones.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-s', '--sport', help="The sport you wish to analyse.")

        self.args = parser.parse_args()

    def _caller(self, n: int)-> None:

        self.current_sport = Sport(self.main_options[n], self)

    def run(self)-> None:
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
                    self.running = self.session = False
                if self.is_number(selected_input):
                    if int(selected_input) in list(range(len(self.main_options))):
                        self._caller(int(selected_input))
                    else:
                        self._log('Selected input is not valid, please try again.')


app = MainMenu()
app.run()
