import commonFunctions as cf
import pandas as pd
import scrapers as scrape
from datetime import datetime
from datetime import timedelta

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


def select_league(league_data, fixtures, data_source):
    """Takes  in the leagueData dictionary.
    Prompts the user to select a league.
    Returns the key value of the selected league.
    """ 
    # Create the appropriate availableLeagues dictionary: "League name": "League link from data source"
    if data_source == "Bet Study":
        # Imported from the bet-study-leagues.json file.
        available_leagues = cf.import_json_file("bet-study-leagues", False)
    else:
        # Imported from the soccer-stats-leagues.json file.
        available_leagues = cf.import_json_file("soccer-stats-leagues", False)
        
    while True:
        available_options = []
        new_leagues = {} # Used for input validation and tidy display of available leagues.
        option = ""  # Number entered by user
        gather_data = "" # Will store gathered data if user chooses a league.
        
        # Create the available_options list of availble option numbers for input validation later on.
        option_number = 0
        for league in available_leagues:
            option_number += 1 
            new_leagues[str(option_number) + " " + league] = [str(option_number), league] # Add option numbers to a new leagues dictionary for display.
            available_options.append(str(option_number)) # Add the option number string to the list of selectable options.

        # Display the new leagues keys with the newly added option numbers.
        cf.custom_pretty_print(new_leagues, 3)
        
        # Add extra options to available options.
        extra_options = ["0", "all"]
        for extra_option in extra_options:
            available_options.append(extra_option)
        
        # Create a list to store the selected leagues.
        selected_leagues = []
        
        # Print instructions outside of the loop to avoid repetition.
        print("\nSelected data source: " + data_source)
        print("\nEnter leagues to add (one at a time). Enter all to select all leagues. Enter 0 when done.")
        
        # True loop to add multiple leagues
        while True:
            while option not in available_options:
                option = input().lower()
            
            # If all entered, add all leagues to the list of selections and commence scrape.
            if option == "all":
                for league in available_leagues:
                    selected_leagues.append(league)
                option = "0"
            else:
                # Check which league belongs to the selected option and add it to the selection list.
                for league in new_leagues:
                    if option == new_leagues[league][0]:
                        selected_leagues.append(new_leagues[league][1])

            # Debug code: Display selected_leagues list.
            # print("Selected leagues: " + selected_leagues)
            
            # If user enters 0, exit the loop.
            if option == "0":
                del new_leagues # Remove the copy of the leagues dictionary.
                break
            
            # Reset the input to blank ready for the next selection.
            option = ""
        
        # If there are leagues in the selected_leagues list, scrape them.
        if selected_leagues:
            selected_leagues = cf.remove_duplicates(selected_leagues)
            print("\nDownloading the requested data, please wait...")
            for selection in selected_leagues:
                gather_data = inform_and_scrape(selection, league_data, fixtures, available_leagues, data_source)
        else:
            print("No leagues added.")
            
        # If gather_data is blank (user entered 0 without selecting leagues or scraping failed) just exit.
        # Otherwise, confirm data has been downloaded before exiting.
        if gather_data == "Success":
            print("\nLeague data has been downloaded. Press enter to continue.")
            
            input()
            return
        else:
            return

def inform_and_scrape(selection, league_data, fixtures, available_leagues, data_source):
    """
    Takes in the key value of a selected league.
    Advised that downloading of that league is taking place.
    Passes the league key to the get_league_data function for scraping.
    """
    # Debug code: display the URL that will be used to obtain the league data
    # print("This will use the following url: " + availableLeagues[selection] + "\n")
    
    # Select the appropriate function based on the selected data source.
    if data_source == "Bet Study":
        get_league_data_and_fixtures = scrape.get_league_data_bet_study(selection, league_data, fixtures, available_leagues)
    else:
        get_league_data_and_fixtures = scrape.get_league_data_soccer_stats(selection, league_data, fixtures, available_leagues)
    
    if get_league_data_and_fixtures == "Scrape error":
        return
    else:
        print(selection + " download complete.")
    
    #league_data_and_fixtures checked to contain a list of a dict
    #(league data) and a list of lists of fixtures
    return get_league_data_and_fixtures



def get_league(t, league_data):
    """
    Takes in a team name as a string and the leagueData dictionary.
    Returns the name of the league the team belongs to as a string.
    """
    league_team_pairs = league_data.items()
    for team in league_team_pairs:
        if t in team[1]:
            return team[0]
    print("Error: Team not found")
    return "Error: Team not found"


def compare(home_team, away_team, league_data):
    """
    Takes in 2 team names as strings.
    Compares the home team's home stats with the away team's away stats.
    Also compares both teams total stats.
    Returns a list of 2 lists.
    First list contains Home / Away differences.
    Second list contains Total differences.
    Works as expected, but doesn't provide a clear comparison alone.
    For example, a difference of -2 for goals "for" is good for the away team.
    However, a difference of - 2 for goals "against" is good for the home team.
    Possible solution is to manually reverse bad stats. However, this will be
    difficult to do without affecting modularity. Eg. if a new stat is added to the
    league data, this function may need to be updated.
    A solution would be to use dictionaries instead of lists. Bending my head now
    though, so probably my next task for another day.
    """
    # Check what league the home team belongs to
    home_league = get_league(home_team, league_data)

    # Initialise the home team stats lists (one for home and one for total)
    home_team_home_stats = [home_team]
    home_team_total_stats = [home_team]

    # Append the value of each "Home" stat for the home team to the homeTeamHomeStats list
    # Append the value of each "Total" stat for the home team to the homeTeamTotalStats list
    for section in ["Home", "Total"]:
        for stat in league_data[home_league][home_team][section]:
            if section == "Home":
                home_team_home_stats.append(league_data[home_league][home_team][section][stat])
            if section == "Total":
                home_team_total_stats.append(league_data[home_league][home_team][section][stat])

    # Check what league the away team belongs to
    away_league = get_league(away_team, league_data)

    # Initialise the away stats lists (one for away and one for total)
    away_team_away_stats = [away_team]
    away_team_total_stats = [away_team]

    # Append the value of each "Away" stat for the away team to the awayTeamAwayStats list
    # Append the value of each "Total" stat for the away team to the awayTeamTotalStats list
    for section in ["Away", "Total"]:
        for stat in league_data[away_league][away_team][section]:
            if section == "Away":
                away_team_away_stats.append(league_data[away_league][away_team][section][stat])
            if section == "Total":
                away_team_total_stats.append(league_data[away_league][away_team][section][stat])

    # Initialise the homeAwaydifference, totalDifference and pcVariance lists
    home_away_difference = []
    total_difference = []
    # pcVariance = ["Variance %"] #Omitted, see line comment below

    # For each statistic for each team calculate the home and away difference and the total difference
    # Assign the values to the appropriate list
    for stat in range(1, len(home_team_home_stats)):
        
        home_away_difference.append(home_team_home_stats[stat] - away_team_away_stats[stat])
        total_difference.append(home_team_total_stats[stat] - away_team_total_stats[stat])

        """
        Calculating variance percentage: Not working as planned so currently omitted.
        Prototype only created for H/A difference, total difference would also need implementing.
        # Avoiding a division by zero error by appending 0 when the highest value is 0
        if max(homeTeamStats[stat], awayTeamStats[stat]) == 0:
            pcVariance.append(0)
        else:
            pcVariance.append(round(min(homeTeamStats[stat], awayTeamStats[stat])
                              / max(homeTeamStats[stat], awayTeamStats[stat])*100, 2))
        """
    # initialise comparison list for easy return of all generated lists
    comparison = [home_away_difference, total_difference]
    
    return comparison

def list_teams(league_data):
    """
    Takes the league_data dictionary.
    Returns a list of all teams within it.
    """
    team_list = []
    for league in league_data:
        for team in league_data[league]:
            team_list.append(team)
    return team_list

def manual_game_analysis(league_data, predictions):
    """
    Takes the league_data dictionary and current predictions.
    Asks the user to select the home and away teams from the available
    teams.
    Provides a comparison.
    Returns the prediction as a list: [homeTeam, predictedHomeScore, awayTeam, predictedAwayScore]
    """
    today = datetime.today()
    team_list = []
    selection1 = ""
    selection2 = ""
    team_list_display = []
    if league_data == {}:
        print("You can't run manual game analysis until you have selected the appropriate league(s).")
        print("Please select a league or import a JSON file first.")
        input("\nPress enter to continue")
        error = "No leagues loaded" # Response advising why the function failed.
        return error

    # Build the basic team list (this must be kept for later use)
    for team in list_teams(league_data):
        team_list.append(team)
    
    # Build a list of teams with their option numbers ready for display
    for team in team_list:
        team_list_display.append(str(team_list.index(team) + 1) + " " + team)
    
    # Display the newly generated list
    cf.custom_pretty_print(team_list_display, 3)
       
    # while homeTeam not in teamList or awayTeam not in teamList:

    while not cf.valid_input(selection1, range(1, len(team_list) + 1)):
        print("\nSelect home team from the above list:", end = " ")
        selection1 = input()
    while not cf.valid_input(selection2, range(1, len(team_list) + 1)):
        print("\nSelect away team from the above list:", end = " ")
        selection2 = input()

    home_team = team_list[int(selection1)-1]
    away_team = team_list[int(selection2)-1]
    home_team_league = get_league(home_team, league_data)
    away_team_league = get_league(away_team, league_data)
    
    if home_team_league == away_team_league:
        league = home_team_league
    else:
        league = "(mixed leagues)"
        
    print(home_team + " vs " + away_team)
        
    comparison = compare(home_team, away_team, league_data)
    print("\n\nComparison")
    print("==========")
    print("\nPositive numbers indicate Home team statistic is higher."
          " \nNegative numbers indicate Away team statistic is higher.\n")
    comparison_index_count = 0
        
    print("Home / Away Game Statistical Differences")
    print("========================================")

    for stat in ["Played", "Won", "Drew", "Lost", "For", "Against", "Points"]:
        print(stat, comparison[0][comparison_index_count], end = " ")
        comparison_index_count += 1
    print()
    for stat in ["Won per Game", "Drew per Game", "Lost per Game"]:
        print(stat, comparison[0][comparison_index_count], end = " ")
        comparison_index_count += 1
    print()
    for stat in ["For per Game", "Against per Game", "Points per Game"]:
        print(stat, comparison[0][comparison_index_count], end = " ")
        comparison_index_count += 1
        
    print("\n\nTotal Game Statistical Differences")
    print("==================================")
    comparison_index_count = 0
    
    for stat in ["Played", "Won", "Drew", "Lost", "For", "Against", "Points"]:
        print(stat, comparison[1][comparison_index_count], end = " ")
        comparison_index_count += 1
    print()
    for stat in ["Won per Game", "Drew per Game", "Lost per Game"]:
        print(stat, comparison[1][comparison_index_count], end = " ")
        comparison_index_count += 1
    print()
    for stat in ["For per Game", "Against per Game", "Points per Game"]:
        print(stat, comparison[1][comparison_index_count], end = " ")
        comparison_index_count += 1

    home_team_max_goals = league_data[home_team_league][home_team]["Home"]["For per Game"] * 2.5
    away_team_max_goals = league_data[away_team_league][away_team]["Away"]["For per Game"] * 2.5
    
    home_team_goals = int((league_data[home_team_league][home_team]["Home"]["For per Game"] * 1.25) * league_data[away_team_league][away_team]["Away"]["Against per Game"])
    away_team_goals = int((league_data[away_team_league][away_team]["Away"]["For per Game"] * 1.25) * league_data[home_team_league][home_team]["Home"]["Against per Game"])
    
    if home_team_goals > home_team_max_goals:
        home_team_goals = home_team_max_goals
    
    if away_team_goals > away_team_max_goals:
        away_team_goals = away_team_max_goals
    
    prediction_goal_separation = abs(home_team_goals - away_team_goals)
    
    if home_team_goals > 0 and away_team_goals > 0:
        both_to_score = "Yes"
    else:
        both_to_score = "No"
    
    prediction_name = "Home_home_F_A_vs_Away_away_F_A"
    prediction_description = "home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a) : away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))"
    
    # Save current prediction as a list item        
    prediction = {"League": league, "Date and time": "Manual entry: ", "Prediction type": prediction_name, "Home team": home_team,
    "Home team prediction": home_team_goals, "Away team": away_team, "Away team prediction": away_team_goals, 
    "Predicted separation": prediction_goal_separation, "Both to score": both_to_score, "Home result": "",
    "Away result": "", "Goal separation": "", "Both teams scored": "",  "date_as_dtobject": today}

    # Flatten league stats for prediction storage and exporting
    for team in [home_team, away_team]: # Do for each team
        if team == home_team:           # Used for the prediction keys
            h_a_stat_key = "Home Team"
        elif team == away_team:
            h_a_stat_key = "Away Team"
        league = get_league(team, league_data) # Get the team's league
        for section in ["Home", "Away", "Total"]: # Go through each set of stats
            for stat in league_data[league][team][section]: # Add each stat and a descriptive key to the prediction dictionary
                prediction[h_a_stat_key + " " + section + " " + stat] = league_data[league][team][section][stat]
    
    prediction["Description"] = prediction_description
    
    print("\n\nPredicted outcome: " + home_team + " " + str(home_team_goals) + " " + away_team + " " + str(away_team_goals) + "\n\nFull analysis details can be viewed be exporting the predictions to a file via the 'Reports' menu.")
    
    # If the prediction is not already in the predictions list, add it.
    if prediction not in predictions:
        predictions.append(prediction)
    
    return predictions


def upcoming_fixture_predictions(fixtures, predictions, league_data):
    """
    Takes in the fixtures and predictions lists and league_data dictionary.
    Runs predictions on all upcoming fixtures.
    Adds each prediction to the predictions list.
    Returns the updated predictions list.
    """ 
    for fixture in fixtures:
        fixture_league = fixture[0]
        fixture_datetime = fixture[1]
        home_team = fixture[2]
        away_team = fixture[3]
        #print("HOME TEAM: " + home_team + " AWAY TEAM: " + away_team) # DEBUG CODE
        
        #comparison = compare(homeTeam, awayTeam, league_data)
        """
        comaprison return notes:
        [H/A compare[Pld,W,D,L,F,A,Pts], Total compare[Pld,W,D,L,F,A,Pts]]
        """
        
        home_team_league = get_league(home_team, league_data)
        away_team_league = get_league(away_team, league_data)
        
        if home_team_league == away_team_league:
            league = home_team_league
        else:
            league = "(mixed leagues)"
    
        home_team_max_goals = league_data[home_team_league][home_team]["Home"]["For per Game"] * 2.5
        away_team_max_goals = league_data[away_team_league][away_team]["Away"]["For per Game"] * 2.5
        
        home_team_goals = int((league_data[home_team_league][home_team]["Home"]["For per Game"] * 1.25) * league_data[away_team_league][away_team]["Away"]["Against per Game"])
        away_team_goals = int((league_data[away_team_league][away_team]["Away"]["For per Game"] * 1.25) * league_data[home_team_league][home_team]["Home"]["Against per Game"])
        
        if home_team_goals > home_team_max_goals:
            home_team_goals = int(home_team_max_goals)
        
        if away_team_goals > away_team_max_goals:
            away_team_goals = int(away_team_max_goals)
        
        prediction_goal_separation = abs(home_team_goals - away_team_goals)
        
        if home_team_goals > 0 and away_team_goals > 0:
            both_to_score = "Yes"
        else:
            both_to_score = "No"
        
        prediction_name = "Home_home_F_A_vs_Away_away_F_A"
        prediction_description = "home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a) : away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))"
        
        # Save current prediction as a list item        
        prediction = {"League": league, "Date and time": fixture_datetime, "Prediction type": prediction_name, "Home team": home_team,
        "Home team prediction": home_team_goals, "Away team": away_team, "Away team prediction": away_team_goals, 
        "Predicted separation": prediction_goal_separation, "Both to score": both_to_score, "Home result": "",
        "Away result": "", "Goal separation": "", "Both teams scored": "", "date_as_dtobject": fixture[4]}

        # Flatten league stats for prediction storage and exporting
        for team in [home_team, away_team]: # Do for each team
            if team == home_team:           # Used for the prediction keys
                h_a_stat_key = "Home Team"
            elif team == away_team:
                h_a_stat_key = "Away Team"
            league = get_league(team, league_data) # Get the team's league
            for section in ["Home", "Away", "Total"]: # Go through each set of stats
                for stat in league_data[league][team][section]: # Add each stat and a descriptive key to the prediction dictionary
                    prediction[h_a_stat_key + " " + section + " " + stat] = league_data[league][team][section][stat]
        
        prediction["Description"] = prediction_description
        
        """
        "home_team_stats": league_data[home_team_league][home_team],
        "away_team_stats": league_data[away_team_league][away_team]}
        """
        
        # If the prediction is not already in the predictions list, add it.
        if prediction not in predictions:
            predictions.append(prediction)

    # Return the new predictions list
    return predictions
    
def get_predictions_in_range(predictions, game_range):
    """
    Takes the current predictions list and the currently selected game_range.
    Returns a new list of predictions within the given game range.
    """
    today = datetime.today()
    tomorrow = today + timedelta(days = 1)
    teams = {}
    predictions_in_range = []
    for prediction in predictions:
        if isinstance(game_range, timedelta):
            # If game date within range, display the fixture.
            if (prediction.get("date_as_dtobject", tomorrow) - today).days <= game_range.days - 1 or prediction["Date and time"] == "Manual entry: ":
                """print("\n date ") # DEBUG CODE
                print(game["date_as_dtobject"]) # DEBUG CODE
                print() # DEBUG CODE"""
                predictions_in_range.append(prediction)
            
    # If game_range is number of games
    if isinstance(game_range, int):
        # Create a dictionary of present teams and count the team's presence   
        for prediction in predictions:
            # Games that are manually entered do not count towards the game range limit.
            # Only counting team appearances in games that are not manually entered.
            if prediction["Date and time"] != "Manual entry: ":
                teams[prediction["Home team"]] = teams.get(prediction["Home team"], 0) + 1
                teams[prediction["Away team"]] = teams.get(prediction["Away team"], 0) + 1
                if teams[prediction["Home team"]] <= game_range:
                    # Set to display if the home team hasn't been displayed enough times yet.
                    home_game_in_range = True

                if teams[prediction["Away team"]] <= game_range:
                    # Set to display if the away team hasn't been displayed enough times yet.
                    away_game_in_range = True
                
                if home_game_in_range or away_game_in_range:
                    predictions_in_range.append(prediction)
                home_game_in_range, away_game_in_range = False, False
            else:
                # Ensure that the date_as_dtobject item is populated in manual entries when the game range is an int to prevent any unexpected errors later.
                prediction["date_as_dtobject"] = tomorrow
                predictions_in_range.append(prediction)
    return predictions_in_range
    
def prepare_prediction_dataframe(predictions):
    """
    Takes the predictions list of prediction dictionaries.
    Returns an appropriately ordered Pandas dataframe
    """
    # Create temporary copy of predictions dictionary without datetime object
    # Can also be used to add or remove information to the spreadsheet.
    temp_predictions = predictions.copy()
    for prediction in temp_predictions:
        del prediction["date_as_dtobject"]
    
    # Create the pandas dataframe object
    df = pd.DataFrame.from_dict(temp_predictions)
    df = df[["League", "Date and time", "Home team", "Away team", "Home team prediction",
         "Away team prediction", "Predicted separation", "Both to score", "Home result",
         "Away result", "Goal separation", "Both teams scored",

         "Home Team Home Played",
         "Home Team Home Won", "Home Team Home Drew", "Home Team Home Lost",
         "Home Team Home For", "Home Team Home Against", "Home Team Home Points",
         "Home Team Home Won per Game", "Home Team Home Drew per Game",
         "Home Team Home Lost per Game", "Home Team Home For per Game",
         "Home Team Home Against per Game", "Home Team Home Points per Game",
         
         "Home Team Away Played", "Home Team Away Won", "Home Team Away Drew",
         "Home Team Away Lost", "Home Team Away For", "Home Team Away Against",
         "Home Team Away Points", "Home Team Away Won per Game",
         "Home Team Away Drew per Game", "Home Team Away Lost per Game",
         "Home Team Away For per Game", "Home Team Away Against per Game",
         "Home Team Away Points per Game",

         "Home Team Total Played", "Home Team Total Won", "Home Team Total Drew",
         "Home Team Total Lost", "Home Team Total For", "Home Team Total Against",
         "Home Team Total Points", "Home Team Total Won per Game",
         "Home Team Total Drew per Game", "Home Team Total Lost per Game",
         "Home Team Total For per Game", "Home Team Total Against per Game",
         "Home Team Total Points per Game",

         "Away Team Home Played",
         "Away Team Home Won", "Away Team Home Drew", "Away Team Home Lost",
         "Away Team Home For", "Away Team Home Against", "Away Team Home Points",
         "Away Team Home Won per Game", "Away Team Home Drew per Game",
         "Away Team Home Lost per Game", "Away Team Home For per Game",
         "Away Team Home Against per Game", "Away Team Home Points per Game",
         
         "Away Team Away Played", "Away Team Away Won", "Away Team Away Drew",
         "Away Team Away Lost", "Away Team Away For", "Away Team Away Against",
         "Away Team Away Points", "Away Team Away Won per Game",
         "Away Team Away Drew per Game", "Away Team Away Lost per Game",
         "Away Team Away For per Game", "Away Team Away Against per Game",
         "Away Team Away Points per Game",

         "Away Team Total Played", "Away Team Total Won", "Away Team Total Drew",
         "Away Team Total Lost", "Away Team Total For", "Away Team Total Against",
         "Away Team Total Points", "Away Team Total Won per Game",
         "Away Team Total Drew per Game", "Away Team Total Lost per Game",
         "Away Team Total For per Game", "Away Team Total Against per Game",
         "Away Team Total Points per Game",

         "Prediction type", "Description"]]
         
    # Delete temporary dictionary.
    del temp_predictions
    return df