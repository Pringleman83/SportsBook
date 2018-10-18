from utils import AbstractUtility
from constants import submenu_options


class Football:
    pass


class Tennis:
    pass


class Sport(AbstractUtility):

    def __init__(self, _type, Mainmenu):
        super().__init__()
        self.main_menu = Mainmenu
        self._type = _type

        self.league = self.option = None
        self.league_text = 'No league selected, please start by selecting one' if self.league is None else self.league

        self._run()

    def _run(self):

        while self.option is None:
            self._log(f'\nCurrent selected league is -> {self.league_text}\n')

            for option in submenu_options:
                self._log(option)

            self.option = input()

            if self.option.lower() == 'm':
                self.main_menu.session = False

            if self.is_number(self.option):

                if int(self.option) in list(range(len(submenu_options))):
                    pass
                else:

                    self._log(f' {self.option} is not a valid input , please try again.')
                    self.option = None

