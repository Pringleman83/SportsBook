import commonFunctions as cf
from datetime import datetime
import football as f

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

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
    for team in f.list_teams(league_data):
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
    home_team_league, away_team_league = f.get_league(home_team, away_team, league_data)
    
    if home_team_league == away_team_league:
        league = home_team_league
    else:
        league = "(mixed leagues)"
        
    print(home_team + " vs " + away_team)
        
    comparison = f.compare(home_team, away_team, league_data)
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
        home_team_goals = int(home_team_max_goals)
    
    if away_team_goals > away_team_max_goals:
        away_team_goals = int(away_team_max_goals)
    
    prediction_goal_separation = abs(home_team_goals - away_team_goals)
    total_goals = home_team_goals + away_team_goals
    
    if home_team_goals > 0 and away_team_goals > 0:
        both_to_score = "Yes"
    else:
        both_to_score = "No"
    
    prediction_name = "Home_home_F_A_vs_Away_away_F_A"
    prediction_description = "home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a) : away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))"
    
    # Save current prediction as a list item        
    prediction = {"League": league, "Date and time": "Manual entry: ", "Prediction type": prediction_name, "Home team": home_team,
    "Home team prediction": home_team_goals, "Away team": away_team, "Away team prediction": away_team_goals, "Total goals expected": total_goals,
    "Predicted separation": prediction_goal_separation, "Both to score": both_to_score,  "date_as_dtobject": today}

    # Flatten league stats for prediction storage and exporting
    index = 0
    for team in [home_team, away_team]: # Do for each team
        if team == home_team:           # Used for the prediction keys
            h_a_stat_key = "Home Team"
        elif team == away_team:
            h_a_stat_key = "Away Team"
        league = [home_team_league, away_team_league][index]
        index += 1
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
    
        home_team_max_goals = league_data[fixture_league][home_team]["Home"]["For per Game"] * 2.5
        away_team_max_goals = league_data[fixture_league][away_team]["Away"]["For per Game"] * 2.5
        
        home_team_goals = int((league_data[fixture_league][home_team]["Home"]["For per Game"] * 1.25) * league_data[fixture_league][away_team]["Away"]["Against per Game"])
        away_team_goals = int((league_data[fixture_league][away_team]["Away"]["For per Game"] * 1.25) * league_data[fixture_league][home_team]["Home"]["Against per Game"])
        
        if home_team_goals > home_team_max_goals:
            home_team_goals = int(home_team_max_goals)
        
        if away_team_goals > away_team_max_goals:
            away_team_goals = int(away_team_max_goals)
        
        prediction_goal_separation = abs(home_team_goals - away_team_goals)
        total_goals = home_team_goals + away_team_goals
        
        if home_team_goals > 0 and away_team_goals > 0:
            both_to_score = "Yes"
        else:
            both_to_score = "No"
        
        prediction_name = "Home_home_F_A_vs_Away_away_F_A"
        prediction_description = "home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a) : away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))"
        
        # Save current prediction as a list item        
        prediction = {"League": fixture_league, "Date and time": fixture_datetime, "Prediction type": prediction_name, "Home team": home_team,
        "Home team prediction": home_team_goals, "Away team": away_team, "Away team prediction": away_team_goals, "Total goals expected": total_goals, 
        "Predicted separation": prediction_goal_separation, "Both to score": both_to_score, "date_as_dtobject": fixture[4]}

        # Flatten league stats for prediction storage and exporting
        for team in [home_team, away_team]: # Do for each team
            if team == home_team:           # Used for the prediction keys
                h_a_stat_key = "Home Team"
            elif team == away_team:
                h_a_stat_key = "Away Team"
            for section in ["Home", "Away", "Total"]: # Go through each set of stats
                for stat in league_data[fixture_league][team][section]: # Add each stat and a descriptive key to the prediction dictionary
                    prediction[h_a_stat_key + " " + section + " " + stat] = league_data[fixture_league][team][section][stat]
        
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

def upcoming_fixture_predictions_benchmarks(football_data):
    """
    Takes in the fixtures and predictions lists and the bench_leagues list of
    league tables.
    Runs predictions on all upcoming fixtures using home vs away benchmark
    league tables.
    Adds each prediction to the predictions list.
    Returns the updated predictions list.
    """ 
    # Optional - Don't add predictions where benchmark games are below threshold.
    threshold = 3
    avoid_below_threshold = True
    
    #print(football_data["fixtures"]) # DEBUG CODE
    
    for fixture in football_data["fixtures"]:
        fixture_league = fixture[0]
        fixture_datetime = fixture[1]
        home_team = fixture[2]
        away_team = fixture[3]
        benchmark_tables = f.benchmark_analysis(fixture, football_data, display = False)
        #print("HOME TEAM: " + home_team + " AWAY TEAM: " + away_team) # DEBUG CODE
        
        #print(benchmark_tables) # DEBUG CODE
        
        #comparison = compare(homeTeam, awayTeam, league_data)
        """
        comaprison return notes:
        [H/A compare[Pld,W,D,L,F,A,Pts], Total compare[Pld,W,D,L,F,A,Pts]]
        """
        # Act on benchmark games threshold.
        if avoid_below_threshold and benchmark_tables[2][home_team]["Played"] < threshold:
            continue
        
        home_team_max_goals = football_data["league_data"][fixture_league][home_team]["Home"]["For per Game"] * 2.5
        away_team_max_goals = football_data["league_data"][fixture_league][away_team]["Away"]["For per Game"] * 2.5
        
        home_team_goals = int((benchmark_tables[2][home_team]["For per Game"] * 1.25) * benchmark_tables[2][away_team]["Against per Game"])
        away_team_goals = int((benchmark_tables[2][away_team]["For per Game"] * 1.25) * benchmark_tables[2][home_team]["Against per Game"])
        
        if home_team_goals > home_team_max_goals:
            home_team_goals = int(home_team_max_goals)
        
        if away_team_goals > away_team_max_goals:
            away_team_goals = int(away_team_max_goals)
        
        prediction_goal_separation = abs(home_team_goals - away_team_goals)
        total_goals = home_team_goals + away_team_goals
        
        if home_team_goals > 0 and away_team_goals > 0:
            both_to_score = "Yes"
        else:
            both_to_score = "No"
        
        prediction_name = "Benchmark games Home_home_F_A_vs_Away_away_F_A"
        prediction_description = "Benchmark games only: home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a) : away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))"
        
        # Save current prediction as a list item        
        prediction = {"League": fixture_league, "Date and time": fixture_datetime, "Prediction type": prediction_name, "Home team": home_team,
        "Home team prediction": home_team_goals, "Away team": away_team, "Away team prediction": away_team_goals, "Total goals expected": total_goals, 
        "Predicted separation": prediction_goal_separation, "Both to score": both_to_score, "date_as_dtobject": fixture[4]}

        #print(prediction) # DEBUG CODE

        # Flatten league stats for prediction storage and exporting
        for team in [home_team, away_team]: # Do for each team
            if team == home_team:           # Used for the prediction keys
                h_a_stat_key = "Home Team"
            elif team == away_team:
                h_a_stat_key = "Away Team"
            for table in range(len(benchmark_tables)): # Go through each set of stats
                for stat in benchmark_tables[table][team]:
                    #print(stat) # DEBUG CODE
                    if table == 0:
                        table_desc = "Home"
                    elif table == 1:
                        table_desc = "Away"
                    elif table == 2:
                        table_desc = "Total" # Add each stat and a descriptive key to the prediction dictionary
                    prediction[h_a_stat_key + " " + table_desc + " " + stat] = benchmark_tables[table][team][stat]
        
        prediction["Description"] = prediction_description
        
        """
        "home_team_stats": league_data[home_team_league][home_team],
        "away_team_stats": league_data[away_team_league][away_team]}
        """
        
        # If the prediction is not already in the predictions list, add it.
        if prediction not in football_data["predictions"]:
            football_data["predictions"].append(prediction)
            
        #print("PREDICTIONS:") # DEBUG CODE
        #print(football_data["predictions"]) # DEBUG CODE
        
    return
