# Useful functions
import json
from prettytable import PrettyTable


class AbstractUtility:

    """
    This class provides some utility functions that would normally be module-level functions but for the sake
    of convenience they belong to this class.

    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def _log(args):
        print(args)

    @staticmethod
    def import_json_file():

        """
        Loads the leagueData.json file into the leagueData dictionary.
        """

        print("---LOADING...---")
        try:
            with open("leagueData.json") as infile:
                loaded_json = json.load(infile)
                print("---LOADED---")
            return loaded_json
        except FileNotFoundError:
            print('No data found')

        input("Press enter to continue")

    @staticmethod
    def export_json_file(data, file_name):
        """ Saves the leagueData dictionary to a json file called
        leagueData.json.
        """
        print("---SAVING...---")
        with open(file_name + ".json", "w") as outfile:
            json.dump(data, outfile, indent=1)
        print("---SAVED---")
        input("Press enter to continue")

    @staticmethod
    def is_number(s) -> bool:

        """
        Tests if the value passed is a number.
        Returns True or False.
        """
        if isinstance(s, str):
            return s.isnumeric()
        return isinstance(s, int) or isinstance(s, float)

    @staticmethod
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

    def custom_pretty_print(self, data, k):
        """Takes any given dictionary or list {data} and prints its keys (in the case of a dictionary) or values (in the case of a list) in k columns.

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

        def get_k_sized_list(data, k):
            s_0 = 0
            s_1 = k
            l = []
            for _ in range(len(data)//k):

                if type(data) == dict:
                    l.append(list(data.keys())[s_0:s_1])
                elif type(data) == list:
                    l.append(data[s_0:s_1])
                s_0 += k
                s_1 += k

            # Add last items and blank items to ensure all items are displayed
            blanks = k - (len(data) % k)
            if isinstance(data, dict):
                l.append(list(data.keys())[s_0:len(data)])
            if isinstance(data, list):
                l.append(data[s_0:len(data)])

            for _ in range(blanks):
                l[-1].append("")
            return l

        x = PrettyTable()
        for i in get_k_sized_list(data, k):
            x.add_row(i)
            x.align = 'l'
            x.header = False
        self._log(x)
