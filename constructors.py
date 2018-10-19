"""

Basic idea is have League class be also a factory for team class, so every League instance has
it's own team list

Basic League and Team classes constructors

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
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class League:
    def __init__(self, data: dict):

        self.__teams = ...
        self.extension = data.get('extension')
        self.name = data.get('name')
        self.len_teams = data.get('teams')

    def __len__(self):
        return self.len_teams if self.len_teams == len(...) else 'Len error, please make an issue about this.'
        #  Better to not just trust the hardcoded values, just in case there is any change on the web page/leagues
        #  organizations

    def __repr__(self):
        return f'League: {self.name}'

    @property
    def teams(self)-> list:
        return self.__teams

    @property
    def info(self)-> str:
        return f'{self}, Teams: {self.teams}'

    def append(self, other)-> None:
        assert isinstance(other, Team)
        self.__teams.append(other)
