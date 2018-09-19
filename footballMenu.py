#Football menu system

from football import *

# Initialise the leagueData dictionary
leagueData = {}

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

def manualGameAnalysis(x):
    print("\nThe manual game analysis feature is coming soon!\n")

def reports(x):
    print("\nThe reports feature is not yet available.\n")

def leave(x):
    print("\nExit to main menu.\n")

def footballMenu():
    footballOptions = [["(1) League select*", "1", selectLeague],#The selectLeague function from football.py
                   ["(2) Download upcoming fixtures*", "2", downloadFixtures],
                   ["(3) Display upcoming fixtures*", "3", displayFixtures],
                   ["(4) Run analytics on upcoming fixtures*", "4", analyseFixtures],
                   ["(5) Display analytics in upcoming fixtures*", "5", displayAnalysis],
                   ["(6) Single game analysis from fixture list*", "6", singleGameAnalysis],
                   ["(7) Manual single game analysis*", "7", manualGameAnalysis],
                   ["(8) Reports*", "8", reports],
                   ["(M) Main menu*", "m", leave]
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
            if selection == option[1]:
                option[2](leagueData)
                selection = ""




