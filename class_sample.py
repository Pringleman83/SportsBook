#Possible implementation of object orientation approach

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
    leagues = []
    
    def __init__(self, league_name):
        """
        Initiate a league object.
        Takes a league name.
        Adds the name to the list of leages created.
        """
        
        # The object holds a list of all of the team objects belonging to the league
        self.data = {"league_name": self.league_name,
                     "teams": []}
        
        # A list of league aliases for the comparing of data from various sources.
        self.aliases = []
        
        # Add the name of the league initiated to the league list.
        leagues.append(league_name)

class Team:
    """
    Team Object.
    Contains all of the data belonging to each team.
    Contains a list of all team objects that have been initiated.
    Has methods for comparing teams and predicting outcomes.
    """
    
    # A blank list that will hold the names of all created team objects initiated.
    teams = []
    
    def __init__(self, team_name, league_name, home_stats, away_stats):
        """
        Initiate a team object.
        Takes the team name, the league it belongs to, the team's home stats as a list and the teams away stats as a list.
        Calculates additional statistics base on those passed to it for future use.
        """
        self.data:{"league_name": self.league_name,
                   "team_name": self.team_name,
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
                       "goals_for_per_game": (int(home_stats[4]) + int(away_stats[4])) / (int(home_stats[0]) + int(away_stats[0]))
                       "goals_against_per_game": (int(home_stats[5]) + int(away_stats[5])) / (int(home_stats[0]) + int(away_stats[0]))
                       "points_per_game": (int(home_stats[6]) + int(away_stats[6])) / (int(home_stats[0]) + int(away_stats[0]))
                   }
                  }
                # List of team aliases for the comparing of data from various sources.
                self.aliases = []
                
                # Add the name of the team initiated to the teams list.
                teams.append(team_name)
            
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
