from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from commonFunctions import *
import pprint
import json
    
def selectLeague(leagueData):
    """Takes  in the availableLeagues dictionary.
    Prompts the user to select a league.
    Returns the key value of theselected league.

    Currently has an extra function for program testing.
    This is the acceptance of options 97-100.
    This function needs to be built into a menu.
    """
    while True:
        availableOptions = []
        option = "" #Number entered by user
        selection = "" #League the option relates to
    
        print("\n Select a league to add: \n ")

        # Display the leagues available and create the availableOptions list of availble
        #option numbers for input validation later on.
        for league in availableLeagues:
            print(league)
            availableOptions.append(availableLeagues[league][0])

        # Debug code: view the availableOptions list after it is created.
        #print("Available options:")
        #pprint.pprint(availableOptions)

        # While no valid option has been entered, wait for a valid option
        #(the earlier described input validation)
        while option not in availableOptions:
            option = input()

        # Assign the league name to the selection variable
        for league in availableLeagues:
            if option == availableLeagues[league][0]:
                selection = league
                #Debug code: Display selected league string
                print("Selected league" + league)
        
        # Extra function as described in docstring
        if selection == "99 Export JSON":
            exportJSONFile(leagueData)
            
        elif selection == "98 Import JSON":
            leagueData = importJSONFile(leagueData)
            
        elif selection == "97 Display Currently Loaded Data":
            pprint.pprint(leagueData)
            input("Press enter to continue")

        elif selection == "100 Quit":
            #Debug code: indicate selection:
            print("Option 100 selected")
            return leagueData
        # End of extra function

        else:
            leagueData = displaySelection(selection, leagueData)


def importJSONFile(leagueData):
    """ Loads the leagueData.json file into the leagueData dictionary.
    Needs to return the file rather than all be actioned in the function.
    This can only be done properly once the menu system is in place because
    the importJSONFile function is currently being called from within another
    function. This would mean passing the leagueData dictionary down through
    multiple functions rather than directly to this function.
    """
    #global leagueData
    print("---LOADING...---")
    with open("leagueData.json") as infile:
        leagueData = json.load(infile)
    print("---LOADED---")
    input("Press enter to continue")
    return leagueData
        
def exportJSONFile(leagueData):
    """ Saves the leagueData dictionary to a json file called
    leagueData.json.
    Needs to return the file rather than all be actioned in the function.
    This can only be done properly once the menu system is in place because
    the exportJSONFile function is currently being called from within another
    function. This would mean passing the leagueData dictionary down through
    multiple functions rather than directly to this function.
    """
    print("---SAVING...---")
    with open("leagueData.json", "w") as outfile:
        json.dump(leagueData, outfile, indent = 1)
    print("---SAVED---")
    input("Press enter to continue")

def displaySelection(selection, leagueData):
    """ Takes in the key value of the selected league.
    Prints the league name and number of teams in that league.
    Gives the option of confirming the selection of that league or returning
    to the main menu.
    """
    choice = ""
    print("You selected " + selection + "\n")
    
    # Debug code: display the URL that will be used to obtain the league data
    #print("This will use the following url: " + availableLeagues[selection][1] + "\n")
    
    print("The league has " + str(availableLeagues[selection][2]) + " teams.")

    while choice != "1" or choice != "2":
        choice = input("Type 1 to gather this data or 2 to go back to the main menu.")
        if choice == "1":
            getLeagueData(selection, leagueData)
            return leagueData
        elif choice == "2":
            return leagueData


def getLeagueData(selection, leagueData):
    """ Takes the key of the selected league from the availableLeagues dictionary.
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
    betStudyMain = "https://www.betstudy.com/soccer-stats/"
    season = "c/" #c is current
    fullURL = betStudyMain + season + availableLeagues[selection][1]
    webClient = uReq(fullURL)
    webHTML = webClient.read()
    webClient.close()
    webSoup = soup(webHTML, "html.parser")
    table = webSoup.find("div",{"id":"tab03_"})

    for i in range(1, availableLeagues[selection][2] + 1):
        position = int(table.select('td')[((i-1)*16)].text)
        teamName = table.select('td')[((i-1)*16)+1].text
        homePlayed = int(table.select('td')[((i-1)*16)+2].text)
        homeWon = int(table.select('td')[((i-1)*16)+3].text)
        homeDrew = int(table.select('td')[((i-1)*16)+4].text)
        homeLost = int(table.select('td')[((i-1)*16)+5].text)
        homeFor = int(table.select('td')[((i-1)*16)+6].text)
        homeAgainst = int(table.select('td')[((i-1)*16)+7].text)
        homePoints = int(table.select('td')[((i-1)*16)+8].text)
        awayPlayed = int(table.select('td')[((i-1)*16)+9].text)
        awayWon = int(table.select('td')[((i-1)*16)+10].text)
        awayDrew = int(table.select('td')[((i-1)*16)+11].text)
        awayLost = int(table.select('td')[((i-1)*16)+12].text)
        awayFor = int(table.select('td')[((i-1)*16)+13].text)
        awayAgainst = int(table.select('td')[((i-1)*16)+14].text)
        awayPoints = int(table.select('td')[((i-1)*16)+15].text)
        totalPlayed = homePlayed + awayPlayed
        totalWon = homeWon + awayWon
        totalDrew = homeDrew + awayDrew
        totalLost = homeLost + awayLost
        totalFor = homeFor + awayFor
        totalAgainst = homeAgainst + awayAgainst
        totalPoints = homePoints + awayPoints

        # Add league to the leagueData dictionary if the league does not already exist within it.
        if selection not in leagueData:
            leagueData[selection] = {teamName:
            {"Home":
            {"Played":homePlayed, "Won":homeWon, "Drew":homeDrew, "Lost":homeLost, "For":homeFor, "Against":homeAgainst, "Points":homePoints}
            , "Away":
            {"Played":awayPlayed, "Won":awayWon, "Drew":awayDrew, "Lost":awayLost, "For":awayFor, "Against":awayAgainst, "Points":awayPoints}
            , "Total":
            {"Played":totalPlayed, "Won":totalWon, "Drew":totalDrew, "Lost":totalLost, "For":totalFor, "Against":totalAgainst, "Points":totalPoints}
            }
            }

        # If the league does already exist, just update the teams and statistics.
        else:
            leagueData[selection][teamName] = {"Home":
            {"Played":homePlayed, "Won":homeWon, "Drew":homeDrew, "Lost":homeLost, "For":homeFor, "Against":homeAgainst, "Points":homePoints}
            , "Away":
            {"Played":awayPlayed, "Won":awayWon, "Drew":awayDrew, "Lost":awayLost, "For":awayFor, "Against":awayAgainst, "Points":awayPoints}
            , "Total":
            {"Played":totalPlayed, "Won":totalWon, "Drew":totalDrew, "Lost":totalLost, "For":totalFor, "Against":totalAgainst, "Points":totalPoints}
            }

    input("Press enter to continue.")
    return leagueData

# The availableLeagues dictionary: "League name":["Option number", "League link from betstudy.com", "Number of teams in league"]   
availableLeagues = {"1 English Premier League":["1", "england/premier-league/", 20],
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
                    "20 Scottish Premier":["20", "scotland/premiership/", 12], #check
                    "21 Scottish Championship":["21", "scotland/championship/", 10], #check
                    "22 Scottish League One":["22", "scotland/league-one/", 10], #check
                    "23 Scottish League Two":["23", "scotland/league-two/", 10], #check
                    "97 Display Currently Loaded Data":["97", "", 0],
                    "98 Import JSON":["98", "", 0],
                    "99 Export JSON":["99", "", 0],
                    "100 Previous Menu":["100", "", 0]
                    }

def getLeague(t, leagueData):
    """
    Takes in a team name as a string and the leagueData dictionary.
    Returns the name of the league the team belongs to as a string.

    Not yet in use.
    """
    leagueTeamPairs = leagueData.items()
    for team in leagueTeamPairs:
        if t in team[1]:
            return team[0]
    print("Error: Team not found")
    return ("Error: Team not found")


def compare(homeTeam, awayTeam, leagueData):
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
    homeLeague = getLeague(homeTeam, leagueData)

    # Initialise the home team stats lists (one for home and one for total)
    homeTeamHomeStats = [homeTeam]
    homeTeamTotalStats = [homeTeam]

    # Append the value of each "Home" stat for the home team to the homeTeamHomeStats list
    # Append the value of each "Total" stat for the home team to the homeTeamTotalStats list
    for section in ["Home", "Total"]:
        for stat in leagueData[homeLeague][homeTeam][section]:
            if section == "Home":
                homeTeamHomeStats.append(leagueData[homeLeague][homeTeam][section][stat])
            if section == "Total":
                homeTeamTotalStats.append(leagueData[homeLeague][homeTeam][section][stat])

    # Check what league the away team belongs to
    awayLeague = getLeague(awayTeam, leagueData)

    # Initialise the away stats lists (one for away and one for total)
    awayTeamAwayStats = [awayTeam]
    awayTeamTotalStats = [awayTeam]

    # Append the value of each "Away" stat for the away team to the awayTeamAwayStats list
    # Append the value of each "Total" stat for the away team to the awayTeamTotalStats list
    for section in ["Away", "Total"]:
        for stat in leagueData[awayLeague][awayTeam][section]:
            if section == "Away":
                awayTeamAwayStats.append(leagueData[awayLeague][awayTeam][section][stat])
            if section == "Total":
                awayTeamTotalStats.append(leagueData[awayLeague][awayTeam][section][stat])

    # Initialise the homeAwaydifference, totalDifference and pcVariance lists
    homeAwayDifference = []
    totalDifference = []
    #pcVariance = ["Variance %"] #Omitted, see line comment below

    # For each statistic for each team calculate the home and away difference and the total difference
    # Assign the values to the appropriate list
    for stat in range(1,len(homeTeamHomeStats)):
        
        homeAwayDifference.append(homeTeamHomeStats[stat] - awayTeamAwayStats[stat])
        totalDifference.append(homeTeamTotalStats[stat] - awayTeamTotalStats[stat])

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
    #initialise comparison list for easy return of all generated lists
    comparison = [homeAwayDifference, totalDifference]
    
    return comparison

def listTeams(leagueData):
    """
	Takes the leagueData dictionary.
	Returns a list of all teams within it.
	"""
    teamList = []
    for league in leagueData:
        for team in leagueData[league]:
            teamList.append(team)
    return teamList

def manualGameAnalysis(leagueData):
    """
    Takes the leagueData dictionary.
    Asks the user to select the home and away teams from the available
    teams.
    Provides a comparison.
    """
    homeTeam = ""
    awayTeam = ""
    teamList = []
    selection1 = ""
    selection2 = ""
    
    for team in listTeams(leagueData):
        teamList.append(team)
        
    for team in teamList:
        print(teamList.index(team) + 1, team)
        
    #while homeTeam not in teamList or awayTeam not in teamList:
        
    while not validInput(selection1, range(1, len(teamList) + 1)):
        print("\n Select home team from the above list.")
        selection1 = input()
    while not validInput(selection2, range(1, len(teamList) + 1)):
        print("\n Select away team from the above list.")
        selection2 = input()
        
    homeTeam = teamList[int(selection1)-1]
    awayTeam = teamList[int(selection2)-1]
    homeTeamLeague = getLeague(homeTeam, leagueData)
    awayTeamLeague = getLeague(awayTeam, leagueData)
        
    print("\nHome Team is: ", homeTeam)
    print("Home game stats:")
    for stat in leagueData[homeTeamLeague][homeTeam]["Home"]:
        print(stat, leagueData[homeTeamLeague][homeTeam]["Home"][stat], end = " ")
    print("\nTotal game stats")
    for stat in leagueData[homeTeamLeague][homeTeam]["Total"]:
        print(stat, leagueData[homeTeamLeague][homeTeam]["Total"][stat], end = " ")
            
    print("\n\nAway Team is: ", awayTeam)
    print("Away game stats:")
    for stat in leagueData[awayTeamLeague][awayTeam]["Away"]:
        print(stat, leagueData[awayTeamLeague][awayTeam]["Away"][stat], end = " ")
    print("\nTotal game stats")
    for stat in leagueData[homeTeamLeague][awayTeam]["Total"]:
        print(stat, leagueData[homeTeamLeague][awayTeam]["Total"][stat], end = " ")
        
    comparison = compare(homeTeam, awayTeam, leagueData)
    print("\n\nComparison")
    comparisonIndexCount = 0
        
    print("Home / Away game stat differences")
    for stat in leagueData[homeTeamLeague][homeTeam]["Home"]:
        print(stat, comparison[0][comparisonIndexCount], end = " ")
        comparisonIndexCount += 1
        
    print("\n\nTotal game stat differences")
    comparisonIndexCount = 0
    for stat in leagueData[awayTeamLeague][awayTeam]["Away"]:
        print(stat, comparison[0][comparisonIndexCount], end = " ")
        comparisonIndexCount += 1
    input()
    return
