from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import commonFunctions as cf

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


def select_league(league_data, fixtures):
    """Takes  in the leagueData dictionary.
    Prompts the user to select a league.
    Returns the key value of the selected league.
    """             
    while True:
        available_options = []
        option = ""  # Number entered by user
        selection = ""  # League the option relates to
   
        # Display the leagues available and create the availableOptions list of availble
        # option numbers for input validation later on.
        cf.custom_pretty_print(available_leagues, 3)
        for league in available_leagues:
            available_options.append(available_leagues[league][0])

        # While no valid option has been entered, wait for a valid option
        # (the earlier described input validation)
        while option not in available_options:
            print("\nSelect a league to add: ")
            option = input()

        # Assign the league name to the selection variable
        for league in available_leagues:
            if option == available_leagues[league][0]:
                selection = league

                # Debug code: Display selected league string
                # print("Selected league: " + league)

        gather_data = display_selection(selection, league_data, fixtures)
        # If the user exits instead of downloading the league data, just exit.
        # Otherwise, confirm data has been downloaded before exiting.
        if not gather_data:
            return (league_data, fixtures)
        else:
            print("\nLeague data has been downloaded. Press enter to continue.")
            input()
            return (league_data, fixtures)

# The availableLeagues dictionary: "League name":["Option number", "League link from betstudy.com",
#  "Number of teams in league"]


available_leagues = {"1 English Premier League": ["1", "england/premier-league/", 20],
                     "2 English Championship": ["2", "england/championship/", 24],
                     "3 English League One": ["3", "england/league-one/", 24],
                     "4 English League Two": ["4", "england/league-two/", 24],
                     "5 Spanish Primera": ["5", "spain/primera-division/", 20],
                     "6 Spanish Segunda": ["6", "spain/segunda-division/", 22],
                     "7 Spanish Segunda B": ["7", "spain/segunda-b/", 20],
                     "8 French Lique 1": ["8", "france/ligue-1/", 20],
                     "9 French Ligue 2": ["9", "france/ligue-2/", 20],
                     "10 German Bundesliga": ["10", "germany/bundesliga/", 18],
                     "11 German 2 Bundesliga": ["11", "germany/2.-bundesliga/", 18],
                     "12 German Liga": ["12", "germany/3.-liga/", 20],
                     "13 Italian Serie A": ["13", "italy/serie-a/", 20],
                     "14 Italian Serie B": ["14", "italy/serie-b/", 19],
                     "15 Brazillian Serie A": ["15", "brazil/serie-a/", 20],
                     "16 Brazillian Serie B": ["16", "brazil/serie-b/", 20],
                     "17 Argentinian Primera Division": ["17", "argentina/primera-division/", 26],
                     "18 Argentinian Prim B Nacional": ["18", "argentina/prim-b-nacional/", 25],
                     "19 Argentinian Prim B Metro": ["19", "argentina/prim-b-metro/", 20],
                     "20 Scottish Premier": ["20", "scotland/premiership/", 12],
                     "21 Scottish Championship": ["21", "scotland/championship/", 10],
                     "22 Scottish League One": ["22", "scotland/league-one/", 10],
                     "23 Scottish League Two": ["23", "scotland/league-two/", 10],
                     "24 Swiss Super League": ["24", "switzerland/super-league/", 10],
                     "25 Swiss Challenge League": ["25", "switzerland/challenge-league/", 10],
                     "26 Ukranian Premier League": ["26", "ukraine/premier-league/", 12],
                     "27 Ukranian Persha Liga": ["27", "ukraine/persha-liga/", 16],
                     "28 Dutch Eredivisie": ["28", "netherlands/eredivisie/", 18],
                     "29 Dutch Eerste Divisie": ["29", "netherlands/eerste-divisie/", 20],
                     "30 Greek Super League": ["30", "greece/super-league/", 16],
                     "31 Greek Football League": ["31", "greece/football-league/", 18],
                     "32 Czech Liga": ["32", "czech-republic/czech-liga/", 16],
                     "33 Czech FNL": ["33", "czech-republic/fnl/", 16],
                     "34 Russian Premier League": ["34", "russia/premier-league/", 16],
                     "35 Russian FNL": ["35", "russia/fnl/", 20],
                     "36 Turkish Super Lig": ["36", "turkey/super-lig/", 18],
                     "37 Turkish 1 Lig": ["37", "turkey/1.-lig/", 18],
                     "38 Belgian Pro League": ["38", "belgium/pro-league/", 16],
                     "39 Belgian Second Division": ["39", "belgium/second-division/", 8],
                     "40 Danish Superliga": ["40", "denmark/superliga/", 14],
                     "41 Danish 1st Division": ["41", "denmark/1st-division/", 12],
                     "42 Norwegian Eliteserien": ["42", "norway/eliteserien/", 16],
                     "43 Norwegian 1. Division": ["43", "norway/1.-division/", 16],
                     "44 Polish Ekstraklasa": ["44", "poland/ekstraklasa/", 16],
                     "45 Polish I Liga": ["45", "poland/i-liga/", 18],
                     "46 Lithuanian 1 Lyga": ["46", "lithuania/1-lyga/", 14],
                     "47 Croatian 1. HNL": ["47", "croatia/1.-hnl/", 10],
                     "48 Croatian 2. HNL": ["48", "croatia/2.-hnl/", 14],
                     "49 Indonesian ISL": ["49", "indonesia/isl/", 18],
                     "50 Swedish Allsvenskan": ["50", "sweden/allsvenskan/", 16],
                     "51 Swedish Superettan": ["51", "sweden/superettan/", 16],
                    }  

def display_selection(selection, league_data, fixtures):
    """ Takes in the key value of the selected league.
    Prints the league name.
    Gives the option of confirming the selection of that league or returning
    to the main menu.
    """
    choice = ""
    print("You selected " + selection + ".")
    
    # Debug code: display the URL that will be used to obtain the league data
    # print("This will use the following url: " + availableLeagues[selection][1] + "\n")

    while choice != "1" or choice != "2":
        choice = input("Type 1 to download this data or 2 to go back to the main menu.")
        if choice == "1":
            league_data_and_fixtures = get_league_data(selection, league_data, fixtures)
            return league_data_and_fixtures
        elif choice == "2":
            return False


def get_league_data(selection, league_data, fixtures):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from bedstudy.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    
    Scrapes the next 15 fixtures of the selected league.
    Adds therm to the fixtures list.
    
    Future upgrades to this function may include:
        * Separate the calculation of additional data to an additional function.
        * Add more calculations (for example, average goals per game) to this
        function or the additional function.
        * Accept an option for previous seasons (other functionality of
        the program would need to be built around that).
    """
    bet_study_main = "https://www.betstudy.com/soccer-stats/"
    season = "c/"  # c is current
    full_url = bet_study_main + season + available_leagues[selection][1]
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("Cannot retrieve data, webpage is down")
        return
    web_html = web_client.read()
    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("div", {"id": "tab03_"})

    for i in range(1, available_leagues[selection][2] + 1):
        position = int(table.select('td')[((i-1)*16)].text)
        team_name = table.select('td')[((i-1)*16)+1].text
        home_played = int(table.select('td')[((i-1)*16)+2].text)
        home_won = int(table.select('td')[((i-1)*16)+3].text)
        home_drew = int(table.select('td')[((i-1)*16)+4].text)
        home_lost = int(table.select('td')[((i-1)*16)+5].text)
        home_for = int(table.select('td')[((i-1)*16)+6].text)
        home_against = int(table.select('td')[((i-1)*16)+7].text)
        home_points = int(table.select('td')[((i-1)*16)+8].text)
        away_played = int(table.select('td')[((i-1)*16)+9].text)
        away_won = int(table.select('td')[((i-1)*16)+10].text)
        away_drew = int(table.select('td')[((i-1)*16)+11].text)
        away_lost = int(table.select('td')[((i-1)*16)+12].text)
        away_for = int(table.select('td')[((i-1)*16)+13].text)
        away_against = int(table.select('td')[((i-1)*16)+14].text)
        away_points = int(table.select('td')[((i-1)*16)+15].text)
        total_played = home_played + away_played
        total_won = home_won + away_won
        total_drew = home_drew + away_drew
        total_lost = home_lost + away_lost
        total_for = home_for + away_for
        total_against = home_against + away_against
        total_points = home_points + away_points

        # Add league to the leagueData dictionary if the league does not already exist within it.
        # Any additional stats calculated above must be added to the dictionary generator here.
        if selection not in league_data:
            league_data[selection] = {
                team_name:
                    {"Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                              "For": home_for, "Against": home_against, "Points": home_points},
                     "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                              "For": away_for, "Against": away_against, "Points": away_points},
                     "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                               "For": total_for, "Against": total_against, "Points": total_points}
                     }
                }

        # If the league does already exist, just update the teams and statistics.
        else:
            league_data[selection][team_name] = {

                 "Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                          "For": home_for, "Against": home_against, "Points": home_points},
                 "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                          "For": away_for, "Against": away_against, "Points": away_points},
                 "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                           "For": total_for, "Against": total_against, "Points": total_points}
                 }
    # Get fixtures
    fixtures_url = "d/fixtures/"
    full_url = bet_study_main + season + available_leagues[selection][1] + fixtures_url
    
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("Cannot retrieve data, webpage is down.")
        return
    web_html = web_client.read()

    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("table", {"class": "schedule-table"})
    
    number_of_games = 15 # Enough games to include the next game for each team
    
    #fixture list 0.text date, 2.text time, 1.text home team, 3.text away team
    #fixture list 5            7            6                 8
    fixture = []
    
    while True:
        try:
            # Scrape the nunmber of requested fixtures and then break out of the loop.
            
            # Each fixture contains 5 cells
            # Multiply the number of games required by 5
            # Produce a list of the 4 of 5 cells needed for each game
            # Add list to fixture list
            for i in range(0,number_of_games * 5, 5):
                fixture = ["", "", "", ""]
                #print(str(i) + " " + str(table.select('td')[i]) + "\n")
                fixture[0] = str(table.select('td')[i].text) # date
                fixture[1] = str(table.select('td')[i + 2].text) # time
                fixture[2] = str(table.select('td')[i + 1].text) # home team
                fixture[3] = str(table.select('td')[i + 3].text) # away team
                
                # Only add the fixture to the fixtures list if it's not already present.
                if not fixture in fixtures:
                    fixtures.append(fixture[:]) # add fixture details to fixtures                    
            break
        except:
            # Number of requested fixtures exceeds the number of requested fixtures, break.
            break
    return (league_data, fixtures)


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
    Takes the leagueData dictionary.
    Returns a list of all teams within it.
    """
    team_list = []
    for league in league_data:
        for team in league_data[league]:
            team_list.append(team)
    return team_list


def manual_game_analysis(league_data, predictions):
    """
    Takes the leagueData dictionary.
    Asks the user to select the home and away teams from the available
    teams.
    Provides a comparison and a comparison.
    Returns the prediction as a list: [homeTeam, predictedHomeScore, awayTeam, predictedAwayScore]
    """

    team_list = []
    selection1 = ""
    selection2 = ""
    team_list_display = []
    if league_data == {}:
        print("You can't run manual game analysis until you have selected the appropriate league(s).")
        print("Please select a league or import a JSON file first.")
        input("Press enter to continue")
        return False

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
        
    print("\nHome Team is: ", home_team)
    print("Home game stats:")
    for stat in league_data[home_team_league][home_team]["Home"]:
        print(stat, league_data[home_team_league][home_team]["Home"][stat], end=" ")
    print("\nTotal game stats:")

    for stat in league_data[home_team_league][home_team]["Total"]:
        print(stat, league_data[home_team_league][home_team]["Total"][stat], end=" ")
            
    print("\n\nAway Team is: ", away_team)
    print("Away game stats:")
    for stat in league_data[away_team_league][away_team]["Away"]:
        print(stat, league_data[away_team_league][away_team]["Away"][stat], end=" ")
    print("\nTotal game stats")
    for stat in league_data[away_team_league][away_team]["Total"]:
        print(stat, league_data[away_team_league][away_team]["Total"][stat], end=" ")

        
    comparison = compare(home_team, away_team, league_data)
    print("\n\nComparison")
    print("==========")
    print("\nPositive numbers indicate Home team statistic is higher."
          " \nNegative numbers indicate Away team statistic is higher.\n")
    comparison_index_count = 0
        
    print("Home / Away Game Statistical Differences")
    print("========================================")

    for stat in league_data[home_team_league][home_team]["Home"]:
        print(stat, comparison[0][comparison_index_count], end=" ")
        comparison_index_count += 1
        
    print("\n\nTotal Game Statistical Differences")
    print("==================================")
    comparison_index_count = 0
    for stat in league_data[away_team_league][away_team]["Away"]:
        print(stat, comparison[0][comparison_index_count], end=" ")
        comparison_index_count += 1

    home_team_avg_gpg_f = int(league_data[home_team_league][home_team]["Home"]["For"] / league_data[home_team_league][home_team]["Home"]["Played"])  # Home team average gaols per for per game
    
    away_team_avg_gpg_f =int(league_data[away_team_league][away_team]["Away"]["For"] / league_data[away_team_league][away_team]["Away"]["Played"])  # Away teamverage goals per for per game
    
    home_team_avg_gpg_a = int(league_data[home_team_league][home_team]["Home"]["Against"] / league_data[home_team_league][home_team]["Home"]["Played"]) # Away team average goals against per game
    
    away_team_avg_gpg_a = int(league_data[away_team_league][away_team]["Away"]["Against"] / league_data[away_team_league][away_team]["Away"]["Played"])  # Away team average goals against per game
    
    home_team_max_goals = home_team_avg_gpg_f * 2.5
    away_team_max_goals = away_team_avg_gpg_f * 2.5
    
    home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a))
    away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))
    
    if home_team_goals > home_team_max_goals:
        home_team_goals = home_team_max_goals
    
    if away_team_goals > away_team_max_goals:
        away_team_goals = away_team_max_goals
    
    
    print("\n" + "Predicted Outcome" + "\n=================\n" + home_team + " " + str(home_team_goals) + " - " + away_team + " " + str(away_team_goals))

    # Save current prediction as a list item. First two empty items are where fixtured games store the fixture date and time.
    prediction = [league, "", "", home_team, home_team_goals, away_team, away_team_goals, "Home team home stats", league_data[home_team_league][home_team]["Home"], "Home team home stats", league_data[home_team_league][home_team]["Total"], "Away team away stats", league_data[away_team_league][away_team]["Away"], "Away team total stats", league_data[away_team_league][away_team]["Total"]]
    
    # If the prediction is not already in the predictions list, add it.
    if not prediction in predictions:
        predictions.append(prediction)
    
    return predictions

def upcoming_fixture_predictions(fixtures, predictions, league_data):
    """
    Takes in the fixtures and predictions lists.
    Runs predictions on all upcoming fixtures.
    Adds each prediction to the predictions list.
    Returns the updated predictions list.
    """
    
    for fixture in fixtures:
        fixture_date = fixture[0]
        fixture_time = fixture[1]
        home_team = fixture[2]
        away_team = fixture[3]
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
    
        home_team_avg_gpg_f = int(league_data[home_team_league][home_team]["Home"]["For"] / league_data[home_team_league][home_team]["Home"]["Played"])  # Home team average gaols per for per game
        
        away_team_avg_gpg_f =int(league_data[away_team_league][away_team]["Away"]["For"] / league_data[away_team_league][away_team]["Away"]["Played"])  # Away teamverage goals per for per game
        
        home_team_avg_gpg_a = int(league_data[home_team_league][home_team]["Home"]["Against"] / league_data[home_team_league][home_team]["Home"]["Played"]) # Away team average goals against per game
        
        away_team_avg_gpg_a = int(league_data[away_team_league][away_team]["Away"]["Against"] / league_data[away_team_league][away_team]["Away"]["Played"])  # Away team average goals against per game
        
        home_team_max_goals = home_team_avg_gpg_f * 2.5
        away_team_max_goals = away_team_avg_gpg_f * 2.5
        
        home_team_goals = int((home_team_avg_gpg_f * 1.25) * (away_team_avg_gpg_a))
        away_team_goals = int((away_team_avg_gpg_f * 1.25) * (home_team_avg_gpg_a))
        
        if home_team_goals > home_team_max_goals:
            home_team_goals = home_team_max_goals
        
        if away_team_goals > away_team_max_goals:
            away_team_goals = away_team_max_goals
        
        # Save current prediction as a list item.
        prediction = [league, fixture_date, fixture_time, home_team, home_team_goals, away_team, away_team_goals, "Home team home stats", league_data[home_team_league][home_team]["Home"], "Home team home stats", league_data[home_team_league][home_team]["Total"], "Away team away stats", league_data[away_team_league][away_team]["Away"], "Away team total stats", league_data[away_team_league][away_team]["Total"]]
        
        # If the prediction is not already in the predictions list, add it.
        if not prediction in predictions:
            predictions.append(prediction)
    
    # Return the new predictions list
    return predictions
