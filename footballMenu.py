#Football menu system
from commonFunctions import isNumber
from football import *
import pprint

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

# temporary, placeholder functions:

def downloadFixtures(x):
    print("\nThe download fixtures feature is not yet available.\n")

def displayFixtures(x):
    print("\nThe display fixtures feature is not yet available.\n")

def analyseFixtures(x):
    print("\nThe analyse fixtures feature is not yet available.\n")

def displayAnalysis(x):
    print("\nThe display analysis feature is not yet available.\n")

def singleGameAnalysis(x):
    print("\nThe single game analysis feature is not yet available.\n")

def leave(x):
    print("\nExit to previous menu.\n")
    
def chooseLeagues(leagueData):
    leagueData = selectLeague(leagueData)

def displaySelectedLeagues(leagueData):
    pprint.pprint(leagueData)

def reports(leagueData):
    print("\nReports Menu\n")
    
    reportOptions = [["(1) Export JSON data", "1"],
                    ["(2) Display currently loaded league data", "2"],
                    ["(M) Return to previous menu", "m"]
                    ]
    
    exitMenu = False
    availableOptions = []
    selection = ""
    
    # Gather a list of availableOption numbers for input recognition
    for option in reportOptions:
        availableOptions.append(option[1])
    
    while exitMenu == False:
        
        selectedLeagues = []
        
        for option in reportOptions:
            print(option[0])
            
        while selection not in availableOptions:
            selection = input()
            selection = selection.lower()
        
        # Menu selection conditionals
        if selection.lower() == "m":
                exitMenu = True
                return leagueData
        if  selection == reportOptions[0][1]:
            exportJSONFile(leagueData)
        if selection == reportOptions[1][1]:
            displaySelectedLeagues(leagueData)
        selection = ""

def footballMenu(leagueData):
    footballOptions = [["(1) League select", "1", chooseLeagues],#The selectLeague function from football.py
                   ["(2) Download upcoming fixtures*", "2", downloadFixtures],
                   ["(3) Display upcoming fixtures*", "3", displayFixtures],
                   ["(4) Run analytics on upcoming fixtures*", "4", analyseFixtures],
                   ["(5) Display analytics in upcoming fixtures*", "5", displayAnalysis],
                   ["(6) Single game analysis from fixture list*", "6", singleGameAnalysis],
                   ["(7) Manual single game analysis", "7", manualGameAnalysis],
                   ["(8) Reports", "8", reports],
                   ["(9) Import data from JSON file", "9"],
                   ["(10) Clear currently loaded league data", "10"],
                   ["(M) Previous menu", "m", leave]
                   ]
    selectedLeagues = []
    exitMenu = False
    availableOptions = []
    selection = ""

    # Gather a list of availableOption numbers for input recognition
    for option in footballOptions:
        availableOptions.append(option[1])
    
    while exitMenu == False:
        
        selectedLeagues = []

        #If there are leages selected in LeagueData, add them to the selectedLeagues
        #list and display the list.
        if leagueData != {}:
            for league in leagueData:
                selectedLeagues.append(league)
            print("\n Selected league(s):\n" )
            for league in selectedLeagues:
                print(league)
            print()
        else:
            print("\n No league currently selected. Please start by selecting a league.\n")

        # Display the available options 
        for option in footballOptions:
            print(option[0])
            
        # Display any additional information
        print("\nItems marked with a * are not available in this version.")

        # Keep asking for a selection while the selection provided is not in the availableOptions list.
        while selection not in availableOptions:
            selection = input()
            selection = selection.lower()

        # If the seleciton is in the list, check if it is "m". If it's not, run it's function,
        #passing the leagueData dictionary.
        for option in footballOptions:
            if selection.lower() == "m":
                exitMenu = True
                break
            if selection == "9":
                leagueData = importJSONFile()
                selection = ""
                continue
            if selection == "10":
                leagueData = {}
                selection = ""
                continue
            if selection == option[1]:
                option[2](leagueData)
                selection = ""
