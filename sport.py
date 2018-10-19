from utils import AbstractUtility
from constants import submenu_options, leagues
from constructors import League

class Football:
    pass


class Tennis:
    pass


class Sport(AbstractUtility):

    def __init__(self, _type: str, mainmenu):
        super().__init__()
        self.main_menu = mainmenu
        self._type = _type

        self.league = self.option = None
        self.league_text = 'No league selected, please start by selecting one' if self.league is None else self.league

        self._run()

    def sub_menu_trigger(self, n: int)-> None:
        self.test = {
            1: self.select_league
                     }
        return self.test[n]()

    def select_league(self):
        while self.league is None:
            # TODO check list of range problem with the +1 thingy
            self.custom_pretty_print([f"{i} {leagues['Football'][i]['name']}" for i in leagues['Football']], 3)
            # this is needed due to the new dict data structure
            self.league = input('Select a league ->')
            if self.league.isnumeric():
                self.league = int(self.league)
                if self.valid_input(self.league, leagues[self._type]):
                    self.league = League(leagues[self._type][self.league])
                    print(self.league)
                else:
                    print('That is not a valid option')
                    self.league = None

    def _run(self) -> None:

        while self.option is None:  # self.option cannot pivot this loop it'll have to be changed
            self._log(f'\nCurrent selected league is -> {self.league_text}\n')

            for option in submenu_options:
                self._log(option)

            self.option = input('->  ')

            if self.option.lower() == 'm':
                self.main_menu.session = False

            if self.option.isnumeric():
                self.option = int(self.option)
                if self.valid_input(self.option, submenu_options):
                    pass

                else:

                    self._log(f' {self.option} is not a valid input , please try again.')
                    self.option = None

        # at this point we have the selected option.
        while self.option is not None and self.league is None:
            self.sub_menu_trigger(self.option)


