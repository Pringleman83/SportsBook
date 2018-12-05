import commonFunctions as cf
import football as f

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


def both_to_score(predictions, applied_filters):
    """
    Takes a list of predictions and currently applied filters.
    Returns all predictions where both teams are expected to score and the updated applied filters list.
    """
    print("(Both teams to score)\n")
    filtered_predictions = []
    filter_name = "Both to score"
    for p in predictions:
        if p["Home team prediction"] > 0 and p["Away team prediction"] > 0:
            filtered_predictions.append(p)
    if len(filtered_predictions) > 0: 
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return (predictions, applied_filters)

def bore_draw(predictions, applied_filters):
    """
    Takes a list of predictions and the currently applied filters.
    Returns all predictions where the resulted is expected to be nil nil and
    the updated applied filters list.
    """
    print("(No score draws)\n")
    filtered_predictions = []
    filter_name = "0-0 draws"
    for p in predictions:
        if p["Total goals expected"] == 0:
            filtered_predictions.append(p)
    if len(filtered_predictions) > 0:
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return (predictions, applied_filters)

def win_by_x(predictions, applied_filters):
    """
    Takes a list of predictions and the currently applied filters.
    Asks the user to select home team, away team or either.
    Asks the user how many goals the filtered prediction should show that team winning by.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    filtered_predictions = []
    print("Win by x goals\n\n Which team to win?\n(H)ome team, (A)way team or (E)ither?\n")
    team = cf.home_or_away()
    if team == "Exit":
        return(predictions, applied_filters)
    
    print("\nEnter number of goals each team must have won by.")        
    x = cf.input_number()
    
    filter_name = team + " team to score at least " + str(x) + " goals more than their opponent." 
    for p in predictions:
        if team == "Home":
            if p["Home team prediction"] - p["Away team prediction"] >= x:
                filtered_predictions.append(p)        
        elif team == "Away":
            if p["Away team prediction"] - p["Home team prediction"] >= x:
                filtered_predictions.append(p)
        elif team == "Either":
            if p["Home team prediction"] - p["Away team prediction"] >= x or p["Away team prediction"] - p["Home team prediction"] >= x:
                filtered_predictions.append(p)
    if len(filtered_predictions) > 0:           
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return (predictions, applied_filters)

def x_or_more_goals_scored(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user how many goals expected to be scored at least.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    print("(x or more goals scored)\n")
    filtered_predictions = []
    print("Enter the lowest number of goals")
    x = cf.input_number()
 
    filter_name = "Total number of goals is " + str(x) + " or more"
    for p in predictions:
        if p["Total goals expected"] >= x:
            filtered_predictions.append(p)
    if len(filtered_predictions) > 0: 
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
        
def x_or_less_goals_scored(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user how many goals expected to be scored at most.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    print("(x or less goals scored)\n\n")
    filtered_predictions = []
    print("\nX goals or less expected to be scored in each game.")
    
    print("Enter the highest number of goals")
    x = cf.input_number()
    
    filter_name = "Total number of goals is " + str(x) + " or less"   
    for p in predictions:
        if p["Total goals expected"] <= x:
            filtered_predictions.append(p)
    if len(filtered_predictions) > 0:  
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
        
# Special filters

def special_james_shoemark_3_or_more(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Returns a list of predictions where total goals expected is over 4 and
    both teams are expected to score at least one goal along with the updated
    applied filters list.
    """
    print("(total goals expected is over 4 and both teams expected to score at least 1\n\n")
    filtered_predictions = []
    filter_name = "James Shoemark special selection"
    for p in predictions:
        if p["Total goals expected"] > 4 and p["Home team prediction"] > 1 and p["Away team prediction"] > 1:
            filtered_predictions.append(p)
    if len(filtered_predictions) > 0:        
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
        
# Team form filters
        
def form_wins(predictions, results, past_range, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user to select the home team or the away team.
    Asks the user by how many goals (at least) the slected team should have
    won each of their last matches in the provided results range.
    Returns a list of predictions where the specifications are met and the
    updated applied_filters list
    """
    
    """
    Currently looks at all results in the specified range for the team.
    This can be changed in the future to look only at home or away results.
    """
    
    """
    Each prediction:
    prediction = {"League": fixture_league, "Date and time": fixture_datetime,
    "Prediction type": prediction_name, "Home team": home_team,
    "Home team prediction": home_team_goals, "Away team": away_team,
    "Away team prediction": away_team_goals, "Total goals expected": total_goals, 
    "Predicted separation": prediction_goal_separation, "Both to score": both_to_score,
    "date_as_dtobject": fixture[4]}
    """
    
    """
    Each result:
    [league, game_date str, home_team, home_team_score, away_team, away_team_score, game_date_time]
    """
    
    print("(all previous games in results range won by x goals)\n\n")
    team = cf.home_or_away(either = False)
    
    print("Enter the lowest number of goals for the " + team + " team to have won each game by.") 
    x = int(cf.input_number())
    
    print("Enter the number of results to check.")
    number_of_results = cf.input_number()
    
    # Ask the user whther they'd like to see relevant results for each team.
    display_results = ""
    while True:
        print("Would you like to see the relevant results of teams that match the search criteria?")
        print("Enter Y or N")
        display_results = input()
        if display_results.lower() == "y" or display_results.lower() == "n":
            break
    
    filtered_predictions = []
    filter_name = team + " team has won all of their last " + str(number_of_results) + " games by " + str(x) + " or more goals"
    # For each prediction
    for p in predictions:
        
        """
        Get the results for the selected team from the results passed into the function.
        mode = "total" means that one list containing all(home and away) results for the
        selected team from the given results range is returned.
        """
        team_results = f.get_team_results(p["League"], p[team + " team"], results, mode = "total")
        
        # Set a flag for qualifying predictions.
        relevant_prediction = True
        
        # Create a list to save relevant results.
        relevant_results = []
        
        # Set the limit of results to check for each iteration of the prediction loop.
        game_limit = number_of_results
        
        # Set a game counter.
        game_count = 0
        
        # For each of the results for the selected team.
        for r in team_results:
            
            # For testing: Display the current team and the current result.
            #shows that if a team displays x wins in a row
            #print(p[team + " team"], r, sep = "\t")
            
            # Increment the game counter.
            game_count += 1
            
            # If the selected team is the home team in the result.
            if p[team + " team"] == r[2]:
                
                # Don't count games that were postponed.
                if cf.is_number(r[5]) == False:
                    game_count -= 1
                    continue
                
                # If the home team score is greater than the away team score by x or more.
                if int(r[3]) - int(r[5]) >= x:
                    # Add the result to the relevant results list.
                    relevant_results.append(r)
                    # Break out of results loop if game counter exceeds limit.
                    if game_count == game_limit:
                        break
                    # Continue the loop to check the remaining games.
                    continue
                # If not, this is not a relevant selection.
                else:
                    # Mark as not relevant.
                    relevant_prediction = False
                    # Exit the loop
                    break
            # If the team selected is the away team in the result.
            if p[team + " team"] == r[4]:
                # Don't count games that were postponed.
                if cf.is_number(r[5]) == False:
                    game_count -= 1
                    continue
                
                # If the away team score is greater than the home team score by x or more.
                if int(r[5]) - int(r[3]) >= x:
                    # Add the result to the relevant results list.
                    relevant_results.append(r)
                    # Break out of results loop if game counter exceeds limit.
                    if game_count == game_limit:
                        break
                    # Continue the loop to check the remaining games.
                    continue
                # If not, this is not a relevant selection.
                else:
                    # Mark as not relevant.
                    relevant_prediction = False
                    break
                
        if relevant_prediction:
            filtered_predictions.append(p)
            if display_results == "y":
                print("\n" + relevant_results[0][0] + "\n" + p[team + " team"] + " qualifying results: \n")
                for result in relevant_results:
                    for item in range(len(result)):
                        if item % 6 == 0:
                            continue
                        else:
                            print(result[item])
                    print()
            
    if len(filtered_predictions) > 0:        
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
        
def form_losses(predictions, results, applied_filters):#WIP
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user to select the home team or the away team.
    Asks the user by how many goals (at least) the slected team should have
    lost each of their last matches in the provided results range.
    Returns a list of predictions where the specifications are met and the
    updated applied_filters list
    """
    
    print("(all previous games in results range lost by x goals)\n\n")
    filtered_predictions = []
    filter_name = "James Shoemark special selection"
    for p in predictions:
        for r in results:
            pass
    
    if len(filtered_predictions) > 0:        
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)

def form_draws(predictions, results, applied_filters):#WIP
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user to select the home team or the away team.
    Asks the user how many goals the slected team should have scored (at least) 
    in each of the draws in the provided results range.
    Returns a list of predictions where the specifications are met and the
    updated applied_filters list
    """
    print("(all previous games in results range drew with x goals)\n\n")
    filtered_predictions = []
    filter_name = "James Shoemark special selection"
    for p in predictions:
        for r in results:
            pass
    
    if len(filtered_predictions) > 0:        
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)

def form_scoring(predictions, results, applied_filters):#WIP
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user to select the home team or the away team.
    Asks the user how many goals the slected team should have scored (at least) 
    in each of the games in the provided results range.
    Asks the user how many goals the slected team should have conceded 
    (at least) in each of the games in the provided results range.
    Returns a list of predictions where the specifications are met and the
    updated applied_filters list
    """

    
    
    print("(all previous games in results where team scored x goals and conceded x goals)\n\n")
    filtered_predictions = []
    filter_name = "x"
    for p in predictions:
        for r in results:
            pass
    
    if len(filtered_predictions) > 0:        
        applied_filters.append(filter_name)
        return (filtered_predictions, applied_filters)
    elif filter_name in applied_filters:
        print("\nFilter has already been applied.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
    else:
        print("\nFilter not applied as it will remove all remaining games.")
        print("Press enter to continue.")
        input()
        return(predictions, applied_filters)
