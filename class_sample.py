#Possible implementation of object orientation approach

class League:
    """
    League object.
    Contains all teams within that league.
    Has methods for returning league specific stats such as top scoring team etc.
    """
    def __init__(self, league_name):
        self.data = {"league_name": self.league_name,
                     "teams": []}

class Team:
    def __init__(self, team_name, league_name, home_stats, away_stats):
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
                pass
