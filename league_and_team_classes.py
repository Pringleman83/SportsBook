#Possible implementation of object orientation approach

"""
For each Team object created a League object is created if necessary. There should be no need to manually
create a league object (don't do it!).

If a team's League object already exists, the team object is simply added to the existing League object's
team dictionary and the League object is added to the Team's league dictionary.

The League and Team classes have registry dictionaries holding links to all instantiated objects.

This means that each object is iterable and all data can be accessed via loops rather than direct calls.
"""

import pprint as p  # Just for the examples at the end of the file.

# A dictionaries of aliases for comparing data from vaious sources
team_aliases = {"manchester united": ["manchester united", "man utd", "manchester utd", "man united"],
             "manchester city": ["manchester city", "man city"]
            }
league_aliases = {}


class League:
    """
    League object.
    Contains all teams within that league.
    Has methods for returning league specific stats such as top scoring team etc.
    """
    # A blank list that will hold the names of all created league objects initiated.
    leagues = {}
    
    def __init__(self, league_name):
        """
        Initiate a league object.
        Takes a league name.
        Adds the name to the list of leages created.
        """

        # The object holds a list of all of the team objects belonging to the league
        self.data = {"league_name": league_name,
                     "teams": []}
        
        # A list of league aliases for the comparing of data from various sources.
        self.aliases = []
        
        # Add the name of the league initiated to the league list.
        self.leagues[league_name] = self


class Team:
    """
    Team Object.
    Contains all of the data belonging to each team.
    Contains a list of all team objects that have been initiated.
    Has methods for comparing teams and predicting outcomes.
    """ 

    # A dictionary containing instantiated lteam names and their instances.
    # Example: "Manchester United" : <object instance>
    teams = {}

    # A dictionary containing instantiated league names and their instances.
    # Example: "English Premier" : <object instance>
    leagues = {}
    
    def __init__(self, team_name, league_name, home_stats, away_stats):
        """
        Initiate a team object.
        Takes the team name, the league it belongs to, the team's home stats as a list and the teams away stats as a list.
        Calculates additional statistics base on those passed to it for future use.
        """
        self.data = {"league_name": league_name,
            "team_name": team_name,
            "home":{
                "played": int(home_stats[0]),
                "won": int(home_stats[1]),
                "drew": int(home_stats[2]),
                "lost": int(home_stats[3]),
                "for": int(home_stats[4]),
                "against": int(home_stats[5]),
                "points": int(home_stats[6]),
                "wins_per_game": int(home_stats[1]) / int(home_stats[0]),
                "draws_per_game": int(home_stats[2]) / int(home_stats[0]),
                "losses_per_game": int(home_stats[3]) / int(home_stats[0]),
                "goals_for_per_game": int(home_stats[4]) / int(home_stats[0]),
                "goals_against_per_game": int(home_stats[5]) / int(home_stats[0]),
                "points_per_game": int(home_stats[6]) / int(home_stats[0])
                },
            "away":{
                "played": int(away_stats[0]),
                "won": int(away_stats[1]),
                "drew": int(away_stats[2]),
                "lost": int(away_stats[3]),
                "for": int(away_stats[4]),
                "against": int(away_stats[5]),
                "points": int(away_stats[6]),
                "wins_per_game": int(away_stats[1]) / int(away_stats[0]),
                "draws_per_game": int(away_stats[2]) / int(away_stats[0]),
                "losses_per_game": int(away_stats[3]) / int(away_stats[0]),
                "goals_for_per_game": int(away_stats[4]) / int(away_stats[0]),
                "goals_against_per_game": int(away_stats[5]) / int(away_stats[0]),
                "points_per_game": int(away_stats[6]) / int(away_stats[0])
                },
            "total":{
                "played": int(home_stats[0]) + int(away_stats[0]),
                "won": int(home_stats[1]) + int(away_stats[1]),
                "drew": int(home_stats[2]) + int(away_stats[2]),
                "lost": int(home_stats[3]) + int(away_stats[3]),
                "for": int(home_stats[4]) + int(away_stats[4]),
                "against": int(home_stats[5]) + int(away_stats[5]),
                "points": int(home_stats[6]) + int(away_stats[6]),
                "wins_per_game": (int(home_stats[1]) + int(away_stats[1])) / (int(home_stats[0]) + int(away_stats[0])),
                "draws_per_game": (int(home_stats[2]) + int(away_stats[2])) / (int(home_stats[0]) + int(away_stats[0])),
                "losses_per_game": (int(home_stats[3]) + int(away_stats[3])) / (int(home_stats[0]) + int(away_stats[0])),
                "goals_for_per_game": (int(home_stats[4]) + int(away_stats[4])) / (int(home_stats[0]) + int(away_stats[0])),
                "goals_against_per_game": (int(home_stats[5]) + int(away_stats[5])) / (int(home_stats[0]) + int(away_stats[0])),
                "points_per_game": (int(home_stats[6]) + int(away_stats[6])) / (int(home_stats[0]) + int(away_stats[0]))
                }
            }
            
        # List of team aliases for the comparing of data from various sources.
        self.aliases = []
        
        # Add the name of the team initiated to the teams list.
        self.teams[team_name] = self

        # Instantiate League object if it doesn't already exist.
        # Add this team to the instance.
        if league_name not in self.leagues:
            
            # Create a new league object.
            self.data["league"] = League(league_name)
            
            # Add the league object to the Team class league list.
            self.leagues[league_name] = (self.data["league"])
            
            # Add this team to the newly created league objects team list.
            # (This object's league object.teams list . append self)
            self.data["league"].data["teams"].append(self)

        # If the League object already exists
        else:
            # Add the existing league object to the Team class leagues list.
            # This will enable terating through team objects outside of the class.
            self.data["league"] = self.leagues[league_name] # This objects "league":<League object> = the league object named league_name in the league list.

            # Add this team to the existing league objects team list.
            # (This object's league object.teams list . append self)            
            self.data["league"].data["teams"].append(self)

        def __gt__(self, opponent):
            """
            Takes an oopposing team.
            Determines the default method of sorting teams.
            Uses Total Points Per Game as an ultimate sorter as this takes into account the number of games played.
            A seperate method can be used to compare by a specified statistic.
            """
            if self.data["total"]["points_per_game"] > opponent.data["total"]["points_per_game"]:
                return True
            else:
                return False
        
        def compare_home_away(self, opponent, home_game_boolean):
            """
            Takes in the opponent and whether the game is played at home or away.
            Returns a comparison of all home team home statistics and away team away statistics in a usable form.
            """
            pass
        
        def compare_total(self, opponent):
            """
            Takes in the opponent and whether the game is played at home or away.
            Returns a comparison of all total game statistics in a usable form.
            """
            pass
        
        def predict_outcome(self, opponent, home_game_boolean, prediction_algorithm):
            """
            Takes in the opponent, a boolean indicating whether the game is to be played at home or away
            and a prediction algorithm (likely to be a function).
            Returns a tuple of two ints, predicted home score and predicted away score.
            """
            pass

#Testing / Example

manu = Team("Manchester United", "English Premier", [10,10,0,0,30,2,30],[9,7,2,0,12,4,23])
liverpool = Team("Liverpool", "English Premier", [10,8,1,2,12,4,25],[9,4,3,2,6,4,15])
blues = Team("Birmingham City", "English Championship", [10,10,0,0,30,2,30],[9,7,2,0,12,4,23])
liverpool = Team("Aston Villa", "English Championship", [10,8,1,2,12,4,25],[9,4,3,2,6,4,15])

for league in League.leagues:
    print("\n"+ league)
    print("="*len(league) + "\n")
    
    for team in League.leagues[league].data["teams"]:
        """for item in team.data:
            print(str(team.data[item]) + " ", end = " ")
        print()"""
        p.pprint(team.data)


