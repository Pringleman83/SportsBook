# Football menu system

import football as fb
import pprint
import predictiveAlgorithms as p
import commonFunctions as cf
import filterPredictions as fp
import visuals as v
from datetime import datetime
from datetime import timedelta

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

# temporary, placeholder functions:

def leave(x):
    print("\nExit to previous menu.\n")

def display_selected_leagues(league_data):
    """
    Takes the league_data dictionary and displays it on screen.
    """
    if league_data == {}:
        print("\nNo league data currently loaded. Select league(s) or import data first.")
        print("\nPress enter to return to previous menu.")
        input()
        return 0
    pprint.pprint(league_data)
    return 0
    
def filter_fixtures_by_range(fixtures, future_range):
    """
    Takes in the current list of fixtures (each fixture being at least 
    a list of 5 items) and the current future_range object.
    
    Returns a list of fixtures within the given range.
    """
    today = datetime.today()
    game_count = 0
    teams = {}
    fixtures_in_range = []
    if fixtures == []:
        print("\nNo fixtures currently loaded. Select league(s) first.")
        print("\nPress enter to return to previous menu.")
        input()
        return "No fixtures"
    
    # If future_range is a timedelta object (space in time)
    if isinstance(future_range, timedelta):
        for fixture in fixtures:
            # If game date within range, save the fixture.
            if (fixture[4] - today).days <= future_range.days - 1 and fixture[4] >= today - timedelta( days = 1):
                game_count += 1
                fixtures_in_range.append(fixture)
    
    # If future_range is number of games
    if isinstance(future_range, int):
        
        new_fixtures = sorted(fixtures, key=lambda x: x[4])
        # Create a dictionary of present teams and count the team's presence
        for fixture in new_fixtures:
            # Discount any fixtures that are for a previous date.
            # These can occur if there are games that didn't take place on
            #the planned date.
            if fixture[4] < today:
                continue
            teams[fixture[2]] = teams.get(fixture[2], 0) + 1 
            if teams[fixture[2]] <= future_range:
                # Set to display if the home team hasn't been saved enough times yet.
                save_home_fixture = True
            teams[fixture[3]] = teams.get(fixture[3], 0) + 1
            if teams[fixture[3]] <= future_range:
                # Set to save if the away team hasn't been added to the fixtures_in_range enough times yet.
                save_away_fixture = True

            if save_home_fixture or save_away_fixture:
                # If either team is set to save, add the fixture to fixtures_in_range.
                game_count +=1
                fixtures_in_range.append(fixture)
                # If no fixtures added to fixtures_in_range, dislpay a message.   
            save_home_fixture, save_away_fixture = False, False
    if game_count == 0:
        print("No games available for the selected game range.\n")
    
    # Sort fixtures by league
    fixtures_in_range_sorted = sorted(fixtures_in_range, key=lambda x: x[0])
        
    return fixtures_in_range_sorted
    
def display_fixtures(fixtures):
    """
    Takes in a list of fixtures (each fixture being at least 
    a list of 5 items).
    
    The 5th item is a datetime object and is not used in this function.
    
    Displays the list on the screen.
    """
    league = ""
    if fixtures == []:
        print("\nNo fixtures currently loaded. Select league(s) first.")
        print("\nPress enter to return to previous menu.")
        input()
        return 0

    for fixture in fixtures:
        # Display new league name.
        if fixture[0] != league:
            league = fixture[0]
            print("\n\n" + league + "\n")
            
        # Display the fixture.
        for detail in range(1,4):
            print(fixture[detail] + " ", end = " ")
        print("")
        
    return 0

def display_results(results):
    """
    Takes in a list of results (each result being at least 
    a list of 7 items).
    
    The 7th item is a ,datetime object and is not used in this function.
    
    Displays the list on the screen.
    """
    league = ""
    if results == []:
        print("\nNo results currently loaded. Select league(s) first.")
        print("\nPress enter to return to previous menu.")
        input()
        return 0

    for result in results:
        # Display new league name.
        if result[0] != league:
            league = result[0]
            print("\n\n" + league + "\n")
            
        # Display the fixture.
        for detail in range(1,6):
            print(result[detail] + " ", end = " ")
        print("")
        
    return 0
    
def display_predictions(predictions):
    """
    Takes in a list of game predictions.
    Displays the predictions on screen.
    """
    league = ""
    manual_entries = []
    if not predictions:
        print("\nNo predictions to display.")

        print("\nPress enter to return to previous menu.")
        input()
        return 0
    
    print("\nPredictions")
    print("===========")
    
    for game in predictions:
        # If a new league is present, print the league name
       # print("\nTEST FOR NEXT GAME:\nGame[League]: " + game["League"] + " game[Date and time]" + game["Date and time"]) #DEBUG CODE
        if game["League"] != league and game["Date and time"] != "Manual entry: ":
            print("\n\n" + game["League"] + "\n")
            
        if game["Date and time"] == "Manual entry: ":
            manual_entries.append(game)
        else:
            league = game["League"]
            print(game["Date and time"], game["Home team"], game["Home team prediction"], game["Away team"], game["Away team prediction"])
        
    if manual_entries != []:
        print("\n\nManual Entries\n")
        for manual_entry in manual_entries:
            print(manual_entry["Home team"], manual_entry["Home team prediction"], manual_entry["Away team"], manual_entry["Away team prediction"])

    print("\nPress enter to return to previous menu.")
    input()
    return 0

def select_fixture(fixtures):
    """
    Takes a fixture list.
    Asks the user to select a game.
    Fixtures format:
    List of lists containing: [0-League, 1-date+time, 2-home team, 3-away team, 4-datetime object]
    Returns the selected fixture.
    """
    league = ""
    option_list = []
    choice = ""
    while choice not in option_list:
        game_num = 1
        for fixture in fixtures:
            if fixture[0] != league:
                league = fixture[0]
                print("\n" + league + "\n")
            print (str(game_num) + " " + fixture[1] + " " + fixture[2] + " - " + fixture[3])
            option_list.append(str(game_num))# Gather a list of options available.
            game_num += 1
        print("\nSelect a fixture from above. Enter number 1 to " + str(game_num - 1))
        #print(option_list)
        choice = input()
    return fixtures[int(choice) - 1]
    
def select_range(range_in, mode = "future"):
    """
    Takes in a range of time and an option mode ("past" or "future").
    Asks the user to select a new range in days or games ( datetime days or an int).
    Returns the updated range.
    """
    print("How would you like to specify the number of games to analyse?")
    if mode == "future":
        print("1) By days from now")
        print("2) By games from now")
        print("M) Previous menu")
    elif mode == "past":
        print("1) By days before now")
        print("2) By games before now")
        print("M) Previous menu")
    else:
        print("Unsupported mode in function select_range")
        return 0
    valid_options = ["1", "2", "m"]
    while True:
        option = input().lower()
        if option in valid_options:
            break
    if option == "1":
        while True:
            print("\nEnter range in days (between 1 and 365):")
            option2 = input()
            if cf.is_number(option2):
                if int(option2) > 0 and int(option2) < 366:
                    range_out = timedelta(int(option2))
                    return range_out
        
    if option == "2":
        while True:
            print("\nEnter range in games per team (between 1 and 50):")
            option2 = input()
            if cf.is_number(option2):
                if int(option2) > 0 and int(option2) < 51:
                    range_out = int(option2)
                    return range_out

    if option == "m":
        return 0
 
def get_range(range_in):
    """
    Takes a range variable (either an int for number of games or a timedelta object).
    Returns a string of number of days or number of games and the type.
    Eg. "1 day", "2 days", "1 game" or "2 games".
    """
    if isinstance(range_in, timedelta):
        if range_in.days > 1:
            end = " days"
        else:
            end = " day"
        range_out = str(range_in.days) + end 
    
    elif isinstance(range_in, int):
        if isinstance(range_in, int):
            if range_in > 1:
                end = " games"
            else:
                end = " game"
        range_out = str(range_in) + end
    
    return range_out

def special_filters(predictions_in_range, filtered_predictions, applied_filters):
    """
    The special filters menu for filtering predictions.
    Takes in the currently ranged predictions, the currently filtered
    predictions and the currently applied filters.
    
    On exiting the menu it return the filtered predictions and applied filters.
    """
    print("\nSpecial Filters")
    print("==================\n")
    
    # If no filtered predictions exist.
    if filtered_predictions == []:
    # Filtered predictions is a copy of predictions in range.
        filtered_predictions = predictions_in_range[:]
        applied_filters = []
                
    while True:
        if applied_filters == []:
            print("No filters currently applied.")
        else:
            print("The following filters are applied:\n")
            for filter in applied_filters:
                print(filter)
        print("\n" + str(len(filtered_predictions)) + " games remaining")

        print("\nSelect one of the following special filters to apply:\n")
        print("1) James Shoemark's Over 2.5 Goals Special")
        print("2) Display filtered predictions")
        #print("3)")
        #print("4)")
        #print("5)")
        #print("6)")
        #print("7)")
        #print("8)")
        print("M) Return to previous menu.")
        print()
        s = input().lower()
        
        if s == "m":
            return (filtered_predictions, applied_filters)
        elif s == "1":
            filtered_predictions, applied_filters = fp.special_james_shoemark_3_or_more(filtered_predictions, applied_filters)
        elif s == "2":
            display_predictions(filtered_predictions)
        """elif s == "3":
            filtered_predictions, applied_filters = fp.special_
        elif s == "4":
            filtered_predictions, applied_filters = fp.special_
        elif s == "5":
            filtered_predictions, applied_filters = fp.special_
        elif s == "6":
            filtered_predictions, applied_filters = fp.special_
        elif s == "7":
            filtered_predictions, applied_filters = fp.special_
        elif s == "8":
            filtered_predictions, applied_filters = fp.special_"""
            
def form_filters(predictions_in_range, filtered_predictions, results_in_range, past_range, applied_filters):
    """
    The form filters menu for filtering predictions.
    Takes in the currently ranged predictions, the currently filtered
    predictions the results in the currently selected range and the currently
    applied filters.
    
    On exiting the menu it return the filtered predictions and applied filters.
    """
    print("\nForm Filters")
    print("============\n")
    
    # If no filtered predictions exist.
    if filtered_predictions == []:
    # Filtered predictions is a copy of predictions in range.
        filtered_predictions = predictions_in_range[:]
        applied_filters = []
                
    while True:
        if applied_filters == []:
            print("No filters currently applied.")
        else:
            print("The following filters are applied:\n")
            for filter in applied_filters:
                print(filter)
        print("\n" + str(len(filtered_predictions)) + " games remaining")

        print("\nSelect one of the following form filters to apply:\n")
        print("1) Where a team has won all of their previous games in the results range by x goals.")
        print("2) Display filtered predictions")
        #print("3)")
        #print("4)")
        #print("5)")
        #print("6)")
        #print("7)")
        #print("8)")
        print("M) Return to previous menu.")
        print()
        s = input().lower()
        
        if s == "m":
            return (filtered_predictions, applied_filters)
        elif s == "1":
            filtered_predictions, applied_filters = fp.form_wins(filtered_predictions, results_in_range, past_range, applied_filters)
        elif s == "2":
            display_predictions(filtered_predictions)
        """elif s == "3":
            filtered_predictions, applied_filters = fp.special_
        elif s == "4":
            filtered_predictions, applied_filters = fp.special_
        elif s == "5":
            filtered_predictions, applied_filters = fp.special_
        elif s == "6":
            filtered_predictions, applied_filters = fp.special_
        elif s == "7":
            filtered_predictions, applied_filters = fp.special_
        elif s == "8":
            filtered_predictions, applied_filters = fp.special_"""

def filter_predictions(predictions_in_range, filtered_predictions, results_in_range, past_range, applied_filters):
    """
    The filter predictions menu.
    Take in the currently ranged predictions, the filtered_predictions and
    the list of applied filters.
    
    Returns the filtered predictions and the applied filters on exit.
    """
    print("\nFilter Predicitons")
    print("==================\n")
    
    # If no filtered predictions exist.
    if filtered_predictions == []:
    # Filtered predictions is a copy of predictions in range.
        filtered_predictions = predictions_in_range[:]
        applied_filters = []
                
    while True:
        if applied_filters == []:
            print("No filters currently applied.")
        else:
            print("The following filters are applied:\n")
            for filter in applied_filters:
                print(filter)
        print("\n" + str(len(filtered_predictions)) + " games remaining")

        print("\nSelect one of the following filters to apply. Remove all games except: \n")
        print("1) Games where both teams are expected to score")
        print("2) Games where no teams are expected to score")
        print("3) Games where a team is expected to win by at least x goals")
        print("4) Games where a minimum of a specified number of goals are scored")
        print("5) Games where a maximum of a specified number of goals are scored")
        print("6) View form filters")
        print("7) View special filters")
        print("8) Display filtered predictions")
        print("9) Clear all filters")
        print("M) Return to previous menu.")
        print()
        s = input().lower()
        
        if s == "m":
            return(filtered_predictions, applied_filters)
        elif s == "1":
            filtered_predictions, applied_filters = fp.both_to_score(filtered_predictions, applied_filters)
        elif s == "2":
            filtered_predictions, applied_filters = fp.bore_draw(filtered_predictions, applied_filters)
        elif s == "3":
            filtered_predictions, applied_filters = fp.win_by_x(filtered_predictions, applied_filters)
        elif s == "4":
            filtered_predictions, applied_filters = fp.x_or_more_goals_scored(filtered_predictions, applied_filters)
        elif s == "5":
            filtered_predictions, applied_filters = fp.x_or_less_goals_scored(filtered_predictions, applied_filters)
        elif s == "6":
            filtered_predictions, applied_filters = form_filters(predictions_in_range, filtered_predictions, results_in_range, past_range, applied_filters)
        elif s == "7":
            filtered_predictions, applied_filters = special_filters(predictions_in_range, filtered_predictions, applied_filters)
        elif s == "8":
            display_predictions(filtered_predictions)
        elif s == "9":
            filtered_predictions, applied_filters = predictions_in_range, []
            
def benchmark(fixture, football_data):
    error = 0
    print("\n Benchmark Result analysis\n")
    if football_data["league_data"] == {}:
        print("No league data loaded")
        error += 1
    if football_data["fixtures"] == []:
        print("No fixtures loaded")
        error += 1
    if football_data["fixtures_in_range"] == []:
        print("No fixtures in range loaded")
        error += 1
    if football_data["results"] == []:
        print("No results loaded")
        error += 1
    if football_data["results_in_range"] == []:
        print("No results in range loaded")
        error += 1
    if error > 0:
        print("\nPress enter to return to the previous menu.")
        input()
        return
    fb.benchmark_analysis(fixture, football_data)
    
        
def reports(football_data):
    """
    The reports menu.
    Takes all football data.
    """
    
    report_options = [["(1)  Export league data (!fixture information not currently included!)", "1"],
                      ["(2)  Display currently loaded league data", "2"],
                      ["(3)  Select future game range (for fixtures and predictions)", "3"],
                      ["(4)  Select past game range (for results)", "4"],
                      ["(5)  Display fixtures in range", "5"],
                      ["(6)  Display all predictions in game range", "6"],
                      ["(7)  Filter predictions", "7"],
                      ["(8)  Display filtered predictions in game range", "8"],
                      ["(9)  Display results in range", "9"],
                      ["(10) Save all predictions in range to file", "10"],
                      ["(11) Save filtered predictions in range to file", "11"],
                      ["(M)  Return to previous menu", "m"]
                      ]
    
    exit_menu = False
    available_options = []
    selection = ""
    while not exit_menu:
        while selection not in available_options:
            print("\nReports Menu")
            print("============\n")
            print("Current future game range is " + get_range(football_data["future_range"]))
            print("Current past game range is " + get_range(football_data["past_range"]))
            # Gather a list of available_option numbers for input recognition
            for option in report_options:
                available_options.append(option[1])
            for option in report_options:
                print(option[0]) 
            selection = input().lower()

        # Menu selection conditionals
        if selection.lower() == "m":
                exit_menu = True
                return 0
        if selection == report_options[0][1]: # Export league data to JSON
            cf.export_data(football_data["league_data"], "json")
        if selection == report_options[1][1]: # Display currently loaded league data
            display_selected_leagues(football_data["league_data"])
        if selection == report_options[2][1]: # Select future game range
            football_data["future_range"] = select_range(football_data["future_range"])   
            # Update the predictions_in_range list to suit the newly selected range
            football_data["predictions_in_range"] = fb.get_predictions_in_range(football_data["predictions"], football_data["future_range"])
        if selection == report_options[3][1]: # Select past game range
            football_data["past_range"] = select_range(football_data["past_range"], mode = "past")   
            # Update the results_in_range list to suit the newly selected range
            football_data["results_in_range"] = fb.get_results_in_range(football_data["results"], football_data["past_range"])
        if selection == report_options[4][1]: # Display current fixtures
            if football_data["fixtures"] == []:
                print("\nNo fixtures currently loaded. Select league(s) first.")
                print("\nPress enter to return to previous menu.")
                input()
            else: 
                display_fixtures(filter_fixtures_by_range(football_data["fixtures"], football_data["future_range"]))
        if selection == report_options[5][1]: # Display current predictions
            display_predictions(football_data["predictions_in_range"])
        if selection == report_options[6][1]: # Filter predictions
            filtered_predictions, applied_filters = filter_predictions(football_data["predictions_in_range"], football_data["filtered_predictions"], football_data["results_in_range"], football_data["past_range"], football_data["applied_filters"])
        if selection == report_options[7][1]: # Display filtered predictions
            display_predictions(football_data["filtered predictions"])
        if selection == report_options[8][1]: # Display results in range
            display_results(football_data["results_in_range"])
        if selection == report_options[9][1]: # Save all predictions in range
            if football_data["predictions_in_range"]:
                cf.export_data(fb.prepare_prediction_dataframe(football_data["predictions_in_range"]), "xls")
            else:
                print("\nNo predictions loaded. Generate predictions or run game analysis first.\n")
        if selection == report_options[10][1]: # Save filtered predictions in range
            if filtered_predictions:
                cf.export_data(fb.prepare_prediction_dataframe(football_data["filtered_predictions"]), "xls")
            else:
                print("\nNo predictions found.\n")
        selection = ""


def football_menu(football_data):
    """
    The main football menu.
    Takes all football_data.
    """
    data_source, next_data_source = "Soccer Stats", "Bet Study"
    
    selected_leagues = []
    exit_menu = False
    available_options = []
    selection = ""
    
    while not exit_menu:
        football_options = [["(1) Select a league", "1", fb.select_league],  # The selectLeague function from football.py
                            ["(2) Generate predictions on currently loaded fixtures", "2"],
                            ["(3) Single game visual analysis from fixture list", "3", select_fixture],
                            ["(4) Single game benchmark result analysis", "4", benchmark],
                            ["(5) Manual single game analysis", "5", fb.manual_game_analysis],
                            ["(6) Reports", "6", reports],
                            ["(7) Import data from JSON file", "7"],
                            ["(8) Clear current prediction data", "8"],
                            ["(9) Clear all data", "9"],
                            ["(10) Change data source to " + next_data_source + " (CLEARS ALL DATA)", "10"],
                            ["(Q) Quit", "q", leave]
                            ]
        
        # ["(M) Previous menu", "m", leave] - removed as prev menu currently bypassed.

        # Gather a list of availableOption numbers for input recognition
        for option in football_options:
            available_options.append(option[1])
    
    
        if football_data["league_data"] == {}:
            football_options[0][0] = "(1) Select a league"
        else:
            football_options[0][0] = "(1) Select another league"
        
        selected_leagues = []

        #  If there are leagues selected in LeagueData, add them to the selectedLeagues
        #  list and display the list.
        if football_data["league_data"] != {}:
            for league in football_data["league_data"]:
                selected_leagues.append(league)
            print("\n Selected league(s):\n")
            for league in selected_leagues:
                print(league)
            print()
        else:
            print("\nNo league currently selected. Please start by selecting a league.\n")

        print("Currently selected data source: " + data_source + "\n")
        
        # For clarity of switching data source
        if data_source == "Soccer Stats":
            next_data_source = "Bet Study"
        else:
            next_data_source = "Soccer Stats"
        # Display the available options
        for option in football_options:
            print(option[0])
            
        # Display any additional information
        #print("\nItems marked with a * are not available in this version.")

        # Keep asking for a selection while the selection provided is not in the availableOptions list.
        while selection not in available_options:
            selection = input().lower()

        # If the selection is in the list, run it's function passing
        # the leagueData dictionary by default.
        for option in football_options:
            """if selection == "m":
                exit_menu = True
                break           
                continue """ #Commented out as previous menu bypassed.
            if selection == "q":
                quit()
            if selection == "1": # Select league
                fb.select_league(football_data["league_data"], football_data["fixtures"], football_data["results"], data_source)
                # Set fixtures in range
                football_data["fixtures_in_range"] = filter_fixtures_by_range(football_data["fixtures"], football_data["future_range"])
                # Set results in range
                football_data["results_in_range"] = fb.get_results_in_range(football_data["results"], football_data["past_range"])
                selection = ""
                continue
            if selection == "2": # Run analysis on currently loaded fixtures
                if football_data["fixtures"] == []:
                    print("\nNo fixtures currently loaded. Select a league first.")
                    selection = ""
                    continue
                choice = ""
                while choice not in ["1", "2"]:
                    print("\nSelect a method of prediciton:")
                    print("\n1) Classic home goals vs away goals")
                    print("2) Benchmark games home goals vs away goals")
                    choice = input()
                if choice == "1":
                    football_data["predictions"] = p.upcoming_fixture_predictions(football_data["fixtures"], football_data["predictions"], football_data["league_data"])
                    football_data["predictions_in_range"] = fb.get_predictions_in_range(football_data["predictions"], football_data["future_range"])
                    print("\nPredictions have been processed and can be viewed via the \"Reports\" menu.\nPress enter to continue.")
                    input()
                    selection = ""
                    continue
                if choice == "2":
                    p.upcoming_fixture_predictions_benchmarks(football_data)
                    football_data["predictions_in_range"] = fb.get_predictions_in_range(football_data["predictions"], football_data["future_range"])
                    print("\nPredictions have been processed and can be viewed via the \"Reports\" menu.\nPress enter to continue.")
                    input()
                    selection = ""
                    continue
            if selection == "3": # Visually compare selected fixture
                # Get fixtures in range
                #football_data["fixtures_in_range"] = filter_fixtures_by_range(football_data["fixtures"], football_data["future_range"])
                # If no fixtures yet, return to menu.
                if football_data["league_data"] == {}:
                    print("No league data loaded. Select a league to download first.")
                    print("\nPress enter to return to the previous menu.")
                    input()
                    selection = ""
                    continue
                # Select fixture.
                fixture_to_view = select_fixture(football_data["fixtures_in_range"])
                # Perform visual comparison
                v.visual_comparison(fixture_to_view, football_data["league_data"])
                # Return to menu
                selection = ""
                continue
            if selection == "4": # Benchmark results analysis
                if football_data["league_data"] == {}:
                    print("No league data loaded. Select a league to download first.")
                    print("\nPress enter to return to the previous menu.")
                    input()
                    selection = ""
                    continue
                
                exit_option = False
                while exit_option == False:
                    # Select fixture.
                    fixture_to_view = select_fixture(football_data["fixtures_in_range"])
                    benchmark(fixture_to_view, football_data)
                    while True:
                        print("\nWould you like to benchmark analyse another game? (Y/N)\n")
                        answer = input()
                        if answer.lower() == "y":
                            break
                        elif answer.lower() == "n":
                            exit_option = True
                            break
                    
                selection = ""
                continue    
            if selection == "5": # Manual single game analysis
                exit_manual_analysis_menu = False
                while not exit_manual_analysis_menu:
                    selection = ""
                    another_game = ""
                    
                    # Manual_predictions holds an error message if something goes wrong in the prediction process.
                    manual_predictions = p.manual_game_analysis(football_data["league_data"], football_data["predictions"])
                    # Add new predictions to the fixtures in range.
                    football_data["predictions_in_range"] = fb.get_predictions_in_range(football_data["predictions"], football_data["future_range"])
                    while another_game.lower() != "y" and another_game.lower() != "n":
                    
                        # If something went wrong, don't ask to run another game analysis.
                        if manual_predictions == "No leagues loaded":
                            exit_manual_analysis_menu = True
                            break
                        else:
                            print("\nAnalyse another game? (Y/N)")
                            another_game = input()
                        if another_game.lower() == "n":
                            exit_manual_analysis_menu = True
                            break
                        if another_game.lower() == "y":
                            break
                                
            if selection == "6": # Reports
                reports(football_data)
                selection = ""
                continue
            if selection == "7": # Import data from JSON file
                new_data = cf.import_json_file()
                if new_data == None: # If load fails
                    del new_data
                else:
                    football_data["league_data"] = new_data.copy()
                    del new_data
                selection = ""
                continue
            if selection == "8": # Clear currently loaded predictions data.
                football_data["predictions"] = []
                football_data["predictions_in_range"] = []
                football_data["filtered_predictions"] = []
                football_data["applied_filters"] = []
                selection = ""
                continue
            if selection == "9": # Clear currently loaded data.
                football_data["league_data"] = {}
                football_data["fixtures"] = []
                football_data["results"] = []
                football_data["predictions"] = []
                football_data["predictions_in_range"] = []
                football_data["filtered_predictions"] = []
                football_data["applied_filters"] = []
                selection = ""
                continue    
            if selection == "10": # Switch data source.
                data_source, next_data_source = next_data_source, data_source
                # Clear all data
                football_data["league_data"] = {}
                football_data["fixtures"] = []
                football_data["predictions"] = []
                football_data["predictions_in_range"] = []
                football_data["filtered_predictions"] = []
                football_data["applied_filters"] = []
                football_data["results"] = []
                selection = ""
                continue
                
            # General action for other menu items
            if selection == option[1]:
                option[2](football_data["league_data"])
                selection = ""
                continue
