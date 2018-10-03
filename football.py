from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from commonFunctions import is_number, valid_input
import pprint
import json

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"


def select_league(league_data):
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
        for league in available_leagues:
            print(league)
            available_options.append(available_leagues[league][0])

        # Debug code: view the availableOptions list after it is created.
        # print("Available options:")
        # pprint.pprint(availableOptions)

        # While no valid option has been entered, wait for a valid option

        # (the earlier described input validation)
        while option not in available_options:
            print("\n Select a league to add: ")
            option = input()

        # Assign the league name to the selection variable
        for league in available_leagues:
            if option == available_leagues[league][0]:
                selection = league
                # Debug code: Display selected league string
                # print("Selected league: " + league)

                
        league_data = display_selection(selection, league_data)
        print("\nLeague data has been downloaded. Press enter to continue.")
        input()
        return league_data
      
# The availableLeagues dictionary: "League name":["Option number", "League link from betstudy.com",
#  "Number of teams in league"]

available_leagues = {"1 English Premier League":["1", "england/premier-league/", 20],
                     "2 English Championship":["2", "england/championship/", 24],
                     "3 English League One":["3", "england/league-one/", 24],
                     "4 English League Two":["4", "england/league-two/", 24],
                     "5 Spanish Primera":["5", "spain/primera-division/", 20],
                     "6 Spanish Segunda":["6", "spain/segunda-division/", 22],
                     "7 Spanish Segunda B":["7", "spain/segunda-b/", 20],
                     "8 French Lique 1":["8", "france/ligue-1/", 20],
                     "9 French Ligue 2":["9", "france/ligue-2/", 20],
                     "10 German Bundesliga":["10", "germany/bundesliga/", 18],
                     "11 German 2 Bundesliga":["11", "germany/2.-bundesliga/", 18],
                     "12 German Liga":["12", "germany/3.-liga/", 20],
                     "13 Italian Serie A":["13", "italy/serie-a/", 20],
                     "14 Italian Serie B":["14", "italy/serie-b/", 19],
                     "15 Brazillian Serie A":["15", "brazil/serie-a/", 20],
                     "16 Brazillian Serie B":["16", "brazil/serie-b/", 20],
                     "17 Argentinian Primera Division":["17", "argentina/primera-division/", 26],
                     "18 Argentinian Prim B Nacional":["18", "argentina/prim-b-nacional/", 25],
                     "19 Argentinian Prim B Metro":["19", "argentina/prim-b-metro/", 20],
                     "20 Scottish Premier":["20", "scotland/premiership/", 12],
                     "21 Scottish Championship":["21", "scotland/championship/", 10],
                     "22 Scottish League One":["22", "scotland/league-one/", 10],
                     "23 Scottish League Two":["23", "scotland/league-two/", 10]
                     }

            
def import_json_file():

    """
    Loads the leagueData.json file into the leagueData dictionary.
    """

    print("---LOADING...---")
    try:
        with open("leagueData.json") as infile:
            loaded_json = json.load(infile)
            print("---LOADED---")
        return loaded_json
    except FileNotFoundError:
        print('No data found')

    input("Press enter to continue")


def export_json_file(league_data):
    """ Saves the leagueData dictionary to a json file called
    leagueData.json.
    """
    print("---SAVING...---")
    with open("leagueData.json", "w") as outfile:
        json.dump(league_data, outfile, indent=1)
    print("---SAVED---")
    input("Press enter to continue")


def display_selection(selection, league_data):
    """ Takes in the key value of the selected league.
    Prints the league name and number of teams in that league.
    Gives the option of confirming the selection of that league or returning
    to the main menu.
    """
    choice = ""
    print("You selected " + selection + ".")
    
    # Debug code: display the URL that will be used to obtain the league data
    # print("This will use the following url: " + availableLeagues[selection][1] + "\n")
    
    print("The league has " + str(available_leagues[selection][2]) + " teams.")

    while choice != "1" or choice != "2":
        choice = input("Type 1 to download this data or 2 to go back to the main menu.")
        if choice == "1":
            get_league_data(selection, league_data)
            return league_data
        elif choice == "2":

            return league_data

def get_league_data(selection, league_data):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from bedstudy.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    Currently assumes the global leagueData dictionary.
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

    return league_data


def get_league(t, league_data):
    """
    Takes in a team name as a string and the leagueData dictionary.
    Returns the name of the league the team belongs to as a string.

    Not yet in use.
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

    Not yet in use.
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


def manual_game_analysis(league_data):
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
    if league_data == {}:
        print("You can't run manual game analysis until you have selected the appropriate league(s).")
        print("Please select a league or import a JSON file first.")

        return league_data
    for team in list_teams(league_data):
        team_list.append(team)

    for team in team_list:
        print(team_list.index(team) + 1, team)
        
    # while homeTeam not in teamList or awayTeam not in teamList:
        

    while not valid_input(selection1, range(1, len(team_list) + 1)):
        print("\n Select home team from the above list.")
        selection1 = input()
    while not valid_input(selection2, range(1, len(team_list) + 1)):
        print("\n Select away team from the above list.")

    home_team = team_list[int(selection1)-1]
    away_team = team_list[int(selection2)-1]
    home_team_league = get_league(home_team, league_data)
    away_team_league = get_league(away_team, league_data)
        
    print("\nHome Team is: ", home_team)
    print("Home game stats:")
    for stat in league_data[home_team_league][home_team]["Home"]:
        print(stat, league_data[home_team_league][home_team]["Home"][stat], end=" ")
    print("\nTotal game stats")
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
    print("\n\nComparison\nPositive numbers indicate Home team statistic is higher."
          " \nNegative numbers indicate Away team statistic is higher.\n")
    comparison_index_count = 0
        
    print("Home / Away Game Statistical Differences")
    for stat in league_data[home_team_league][home_team]["Home"]:
        print(stat, comparison[0][comparison_index_count], end=" ")
        comparison_index_count += 1
        
    print("\n\nTotal Game Statistical Differences")
    comparison_index_count = 0
    for stat in league_data[away_team_league][away_team]["Away"]:
        print(stat, comparison[0][comparison_index_count], end=" ")
        comparison_index_count += 1
    
    # Basic prediction based on average goals scored per game for each team at home or away respectively
    print("Predicted outcome: \n")
    home_team_predicted_score = int(league_data[home_team_league][home_team]["Home"]["For"] / league_data[home_team_league][home_team]["Home"]["Played"])  # Average gaols per for per game

    
    away_team_predicted_score = int(league_data[away_team_league][away_team]["Away"]["For"] / league_data[away_team_league][away_team]["Away"]["Played"])  # Average gaols per for per game
    
    """
    ***For possible future use***
    homeGoalsAgainstPerGame = int(leagueData[homeTeamLeague][homeTeam]["Home"]["Against"] / leagueData[homeTeamLeague][homeTeam]["Home"]["Played"]) # Average goals against per game
    awayGoalsAgainstPerGame = int(leagueData[awayTeamLeague][awayTeam]["Away"]["Against"] / leagueData[awayTeamLeague][awayTeam]["Away"]["Played"])  # Average goals against per game
    
    print(homeTeam + " " + str(homeTeamPredictedScorea) + " - " + awayTeam + " " + str(awayTeamPredictedScorea))
    """
    print(home_team + " " + str(home_team_predicted_score) + " - " + away_team + " " + str(away_team_predicted_score))

    predictions = [home_team, home_team_predicted_score, away_team, away_team_predicted_score]
    
    return predictions
