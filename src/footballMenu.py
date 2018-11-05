# Football menu system

import football as fb
import pprint
import commonFunctions as cf
import filterPredictions as fp
from datetime import datetime
from datetime import timedelta

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

# temporary, placeholder functions:

def single_game_analysis(x):
    print("\nThe single game analysis feature is not yet available.\n")

def leave(x):
    print("\nExit to previous menu.\n")


def choose_leagues(league_data, fixtures, data_source):
    #league_data_and_fixtures = 
    fb.select_league(league_data, fixtures, data_source)
    #league_data = league_data_and_fixtures[0]
    #fixtures = league_data_and_fixtures[1]

def display_selected_leagues(league_data):
    if league_data == {}:
        print("\nNo league data currently loaded. Select league(s) or import data first.")
        print("\nPress enter to return to previous menu.")
        input()
        return 0
    pprint.pprint(league_data)
    return 0
    
def display_fixtures(fixtures, game_range):
    """
    Takes in the current list of fixtures (each fixture being at least 
    a list of 4 items) and the current game_range object.
    
    Displays the list on the screen.
    """
    today = datetime.today()
    game_count = 0
    teams = {}
    league = ""
    if fixtures == []:
        print("\nNo fixtures currently loaded. Select league(s) first.")
        print("\nPress enter to return to previous menu.")
        input()
        return 0

    # If game_range is a timedelta object (space in time)
    if isinstance(game_range, timedelta):
        for fixture in fixtures:
            # If game date within range, display the fixture.
            if (fixture[4] - today).days <= game_range.days - 1:
                game_count += 1
                if fixture[0] != league:
                    print("\n\n" + fixture[0] + "\n")
                league = fixture[0]
                for detail in range(1,4):
                    print(fixture[detail] + " ", end = " ")
                print("")
            
    # If game_range is number of games
    if isinstance(game_range, int):
        # Create a dictionary of present teams and count the team's presence
        for fixture in fixtures:
            teams[fixture[2]] = teams.get(fixture[2], 0) + 1 
            if teams[fixture[2]] <= game_range:
                # Set to display if the home team hasn't been displayed enough times yet.
                display_home_fixture = True
            teams[fixture[3]] = teams.get(fixture[3], 0) + 1
            if teams[fixture[3]] <= game_range:
                # Set to display if the away team hasn't been displayed enough times yet.
                display_away_fixture = True

            if display_home_fixture or display_away_fixture:
                # If either team is set to display, display the fixture.
                game_count +=1
                if fixture[0] != league:
                    print("\n\n" + fixture[0] + "\n")
                league = fixture[0]
                for detail in range(1, 4):
                    print(fixture[detail] + " ", end = " ")
                print("")
                # If no fixtures dislayed, dislpay a message.   
            display_home_fixture, display_away_fixture = False, False
    if game_count == 0:
        print("No games available for the selected game range.\n")
    return 0
    
def display_predictions(predictions):
    """
    Takes in a list of game predictions..
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

def select_range(game_range):
    print("How would you like to specify the number of games to analyse?")
    print("1) By days from now")
    print("2) By games from now")
    print("M) Previous menu")
    valid_options = ["1", "2", "m"]
    while True:
        option = input().lower()
        if option == "1" or option == "2" or option == "m":
            break
    if option == "1":
        while True:
            print("\nEnter range in days (between 1 and 365):")
            option2 = input()
            if cf.is_number(option2):
                if int(option2) > 0 and int(option2) < 366:
                    game_range = timedelta(int(option2))
                    return game_range
        
    if option == "2":
        while True:
            print("\nEnter range in games per team (between 1 and 50):")
            option2 = input()
            if cf.is_number(option2):
                if int(option2) > 0 and int(option2) < 51:
                    game_range = int(option2)
                    return game_range

    if option == "m":
        return game_range

def special_filters(filtered_predictions, applied_filters):
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
            return(filtered_predictions, applied_filters)
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

def filter_predictions(predictions_in_range, filtered_predictions, applied_filters):
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
        print("3) Games where a team is expected to win by a specified number of goals")
        print("4) Games where a minimum of a specified number of goals are scored")
        print("5) Games where a maximum of a specified number of goals are scored")
        print("6) View special filters")
        print("7) Display filtered predictions")
        print("8) Clear all filters")
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
            filtered_predictions, applied_filters = special_filters(filtered_predictions, applied_filters)
        elif s == "7":
            display_predictions(filtered_predictions)
        elif s == "8":
            filtered_predictions, applied_filters = predictions_in_range, []

def reports(league_data, fixtures, predictions, predictions_in_range, game_range, applied_filters, filtered_predictions):
    
    report_options = [["(1) Export league data (!fixture information not currently included!)", "1"],
                      ["(2) Display currently loaded league data", "2"],
                      ["(3) Select game range", "3"],
                      ["(4) Display currently loaded fixtures", "4"],
                      ["(5) Display all predictions in game range", "5"],
                      ["(6) Filter predictions (Clears all existing filters)", "6"],
                      ["(7) Display filtered predictions in game range", "7"],
                      ["(8) Save all predictions in range to file", "8"],
                      ["(9) Save filtered predictions in range to file", "9"],
                      ["(M) Return to previous menu", "m"]
                      ]
    
    exit_menu = False
    available_options = []
    selection = ""
    while not exit_menu:
        while selection not in available_options:
            print("\nReports Menu")
            print("============\n")
            if isinstance(game_range, timedelta):
                if game_range.days > 1:
                    end_of_sentence = " days from today.\n"
                else:
                    end_of_sentence = " day from today.\n"
                print("Current game range is " + str(game_range.days) + end_of_sentence)
            elif isinstance(game_range, int):
                if isinstance(game_range, int):
                    if game_range > 1:
                        end_of_sentence = " games per team from now.\n"
                    else:
                        end_of_sentence = " game per team from now.\n"
                print("Current game range is " + str(game_range) + end_of_sentence)
            # Gather a list of available_option numbers for input recognition
            for option in report_options:
                available_options.append(option[1])
            selected_leagues = []
            for option in report_options:
                print(option[0]) 
            selection = input().lower()

        # Menu selection conditionals
        if selection.lower() == "m":
                exit_menu = True
                return (league_data, fixtures, predictions, predictions_in_range, game_range, applied_filters, filtered_predictions)
        if selection == report_options[0][1]: # Export league data to JSON
            cf.export_data(league_data, "json")
        if selection == report_options[1][1]: # Display currently loaded league data
            display_selected_leagues(league_data)
        if selection == report_options[2][1]: # Select game range
            game_range = select_range(game_range)   
            # Update the predictions_in_range list to suit the newly selected range
            predictions_in_range = fb.get_predictions_in_range(predictions, game_range)
        if selection == report_options[3][1]: # Display current fixtures
            display_fixtures(fixtures, game_range)
        if selection == report_options[4][1]: # Display current predictions
            display_predictions(predictions_in_range)
        if selection == report_options[5][1]: # Filter predictions
            filtered_predictions, applied_filters = filter_predictions(predictions_in_range, filtered_predictions, applied_filters)
        if selection == report_options[6][1]: # Display filtered predictions
            display_predictions(filtered_predictions)
        if selection == report_options[7][1]: # Save all predictions in range
            if predictions_in_range:
                cf.export_data(fb.prepare_prediction_dataframe(predictions_in_range), "xls")
            else:
                print("\nNo predictions loaded. Generate predictions or run game analysis first.\n")
        if selection == report_options[8][1]: # Save filtered predictions in range
            if filtered_predictions:
                cf.export_data(fb.prepare_prediction_dataframe(filtered_predictions), "xls")
            else:
                print("\nNo predictions found.\n")
        selection = ""


def football_menu(league_data, fixtures, predictions, predictions_in_range, game_range, applied_filters, filtered_predictions):
    data_source = "Soccer Stats"
    football_options = [["(1) Select a league", "1", choose_leagues],  # The selectLeague function from football.py
                        ["(2) Generate predictions on currently loaded fixtures", "2"],
                        ["(3) Single game analysis from fixture list*", "3", single_game_analysis],
                        ["(4) Manual single game analysis", "4", fb.manual_game_analysis],
                        ["(5) Reports", "5", reports],
                        ["(6) Import data from JSON file", "6"],
                        ["(7) Clear currently loaded league data", "7"],
                        ["(8) Clear currently stored prediction data", "8"],
                        ["(9) Change data source (CLEARS ALL DATA)", "9"],
                        ["(Q) Quit", "q", leave]
                        ]
    
    # ["(M) Previous menu", "m", leave] - removed as prev menu currently bypassed
    selected_leagues = []
    exit_menu = False
    available_options = []
    selection = ""

    # Gather a list of availableOption numbers for input recognition
    for option in football_options:
        available_options.append(option[1])
    
    while not exit_menu:
        if league_data == {}:
            football_options[0][0] = "(1) Select a league"
        else:
            football_options[0][0] = "(1) Select another league"
        
        selected_leagues = []

        #  If there are leagues selected in LeagueData, add them to the selectedLeagues
        #  list and display the list.
        if league_data != {}:
            for league in league_data:
                selected_leagues.append(league)
            print("\n Selected league(s):\n")
            for league in selected_leagues:
                print(league)
            print()
        else:
            print("\nNo league currently selected. Please start by selecting a league.\n")

        print("Currently selected data source: " + data_source + "\n")
        
        # Display the available options
        for option in football_options:
            print(option[0])
            
        # Display any additional information
        print("\nItems marked with a * are not available in this version.")

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
                choose_leagues(league_data, fixtures, data_source)
                selection = ""
                continue
            if selection == "2": # Run analysis on currently loaded fixtures
                predictions = fb.upcoming_fixture_predictions(fixtures, predictions, league_data)
                predictions_in_range = fb.get_predictions_in_range(predictions, game_range)
                print("\nPredictions have been processed and can be viewed via the \"Reports\" menu.\nPress enter to continue.")
                input()
                selection = ""
                continue
            if selection == "4": # Manual single game analysis
                exit_manual_analysis_menu = False
                while not exit_manual_analysis_menu:
                    selection = ""
                    another_game = ""
                    
                    # Manual_predictions holds an error message if something goes wrong in the prediction process.
                    manual_predictions = fb.manual_game_analysis(league_data, predictions)
                    # Add new predictions to the fixtures in range.
                    predictions_in_range = fb.get_predictions_in_range(predictions, game_range)
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
                                
            if selection == "5": # Reports
                league_data, fixtures, predictions, predictions_in_range, game_range, applied_filters, filtered_predictions = reports(league_data, fixtures, predictions, predictions_in_range, game_range, applied_filters, filtered_predictions)
                selection = ""
                continue
            if selection == "6": # Import data from JSON file
                new_data = cf.import_json_file()
                if new_data == None: # If load fails
                    del new_data
                else:
                    league_data = new_data.copy()
                    del new_data
                selection = ""
                continue
            if selection == "7": # Clear currently loaded league data.
                league_data = {}
                fixtures = []
                selection = ""
                continue    
            if selection == "8": # Clear currently loaded predictions data.
                predictions.clear()
                selection = ""
                applied_filters = []
                continue
            if selection == "9": # Switch data source.
                if data_source == "Soccer Stats":
                    data_source = "Bet Study"
                else:
                    data_source = "Soccer Stats"
                league_data = {}
                fixtures = []
                predictions.clear()
                selection = ""
                applied_filters = []
                continue
                
            # General action for other menu items
            if selection == option[1]:
                option[2](league_data)
                selection = ""
                continue
