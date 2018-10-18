
"""
Basic League and Team classes

teams = ['BCN', 'MDR', 'LIS']
a = League('Spanish league')
for team in teams:
    a.append(Team(team))

for team in a.teams:
    print(team.name)

# BCN
# MDR
# LIS
"""


class Team:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class League:
    def __init__(self, name, *teams: Team):

        for team in teams:
            if not isinstance(team, Team):
                raise TypeError

        self.__teams = list(teams)

        self.name = name

    def __len__(self):
        return len(self.__teams)

    def __repr__(self):
        return f'League: {self.name}'

    @property
    def teams(self):
        return self.__teams

    @property
    def info(self):
        return f'{self}, Teams: {self.teams}'

    def append(self, other):
        assert isinstance(other, Team)
        self.__teams.append(other)
