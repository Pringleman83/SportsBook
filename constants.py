"""
Constants file
"""

leagues = {
    'Football':
        {
            1: {'name': 'English Premier League', 'extension': "england/premier-league/", 'teams': 20},
            2: {'name': 'English Championship', 'extension': "england/championship/", 'teams': 24},
            3: {'name': 'English League One', 'extension': "england/league-one/", 'teams': 24},
            4: {'name': 'English League Two', 'extension': "england/league-two/", 'teams': 24},
            5: {'name': 'Spanish Primera', 'extension': "spain/primera-division/", 'teams': 20},
            6: {'name': 'Spanish Segunda', 'extension': "spain/segunda-division/", 'teams': 22},
            7: {'name': 'Spanish Segunda B', 'extension': "spain/primera-division/", 'teams': 20},
            8: {'name': 'French Lique 1', 'extension': "france/ligue-1/", 'teams': 20},
            9: {'name': 'French Ligue 2', 'extension': "france/ligue-2/", 'teams': 20},
            10: {'name': 'German Bundesliga', 'extension': "germany/bundesliga/", 'teams': 18},
            11: {'name': 'German 2 Bundesliga', 'extension': "germany/2.-bundesliga/", 'teams': 18},
            12: {'name': 'German Liga', 'extension': "germany/3.-liga/", 'teams': 20},
            13: {'name': 'Italian Serie A', 'extension': "italy/serie-a/", 'teams': 20},
            14: {'name': 'Italian Serie B', 'extension': "italy/serie-b/", 'teams': 19},
            15: {'name': 'Brazillian Serie A', 'extension': "brazil/serie-a/", 'teams': 20},
            16: {'name': 'Brazillian Serie B', 'extension': "brazil/serie-b/", 'teams': 20},
            17: {'name': 'Argentinian Primera Division', 'extension': "argentina/primera-division/", 'teams': 26},
            18: {'name': 'Argentinian Prim B Nacional', 'extension': "argentina/prim-b-nacional/", 'teams': 25},
            19: {'name': 'Argentinian Prim B Metro', 'extension': "argentina/prim-b-metro/", 'teams': 20},
            20: {'name': 'Scottish Premier', 'extension': "scotland/premiership/", 'teams': 12},
            21: {'name': 'Scottish Championship', 'extension': "scotland/championship/", 'teams': 10},
            22: {'name': 'Scottish League One', 'extension': "scotland/league-one/", 'teams': 10},
            23: {'name': 'Scottish League Two', 'extension': "scotland/league-two/", 'teams': 10},
            24: {'name': 'Swiss Super League', 'extension': "switzerland/super-league/", 'teams': 10},
            25: {'name': 'Swiss Challenge League', 'extension': "switzerland/challenge-league/", 'teams': 10},
            26: {'name': 'Ukranian Premier League', 'extension': "ukraine/premier-league/", 'teams': 12},
            27: {'name': 'Ukranian Persha Liga', 'extension': "ukraine/persha-liga/", 'teams': 16},
            28: {'name': 'Dutch Eredivisie', 'extension': "netherlands/eredivisie/", 'teams': 18},
            29: {'name': 'Dutch Eerste Divisie', 'extension': "netherlands/eerste-divisie/", 'teams': 20},
            30: {'name': 'Greek Super League', 'extension': "greece/super-league/", 'teams': 16},
            31: {'name': 'Greek Football League', 'extension': "greece/football-league/", 'teams': 18},
            32: {'name': 'Czech Liga', 'extension': "czech-republic/czech-liga/", 'teams': 16},
            33: {'name': 'Czech FNL', 'extension': "czech-republic/fnl/", 'teams': 16},
            34: {'name': 'Russian Premier League', 'extension': "russia/premier-league/", 'teams': 16},
            35: {'name': 'Russian FNL', 'extension': "russia/fnl/", 'teams': 20},
            36: {'name': 'Turkish Super Lig', 'extension': "turkey/super-lig/", 'teams': 18},
            37: {'name': 'Turkish 1 Lig', 'extension': "turkey/1.-lig/", 'teams': 18},
        }
}

submenu_options = ["(1) Select a league",
                   "(2) Generate predictions on currently loaded fixtures",
                   "(3) Single game analysis from fixture list*",
                   "(4) Manual single game analysis",
                   "(5) Reports",
                   "(6) Import data from JSON file",
                   "(7) Clear currently loaded league data",
                   "(8) Clear currently stored prediction data",
                   "(M) Previous menu",
                   "\nItems marked with a * are not available in this version."]
