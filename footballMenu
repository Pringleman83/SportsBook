#Football menu system

# temporary, placeholder functions:

def leagueSelect():
    print("leagueSelect")

def downloadFixtures():
    print("downloadFixtures")

def displayFixtures():
    print("displayFixtures")

def analyseFixtures():
    print("analyseFixtures")

def displayAnalysis():
    print("displayAnalysis")

def singleGameAnalysis():
    print("singleGameAnalysis")

def manualGameAnalysis():
    print("manualGameAnalysis")

def reports():
    print("reports")

def leave():
    print("leave")
                   
def footballMenu(footballOptions):
    selectedLeagues = ""
    exitMenu = False
    availableOptions = []
    selection = ""
    while exitMenu == False:
        
        if selectedLeagues != "":
            print("Selected league(s): " )
            for league in selectedLeagues:
                print(league)
        else:
            print("No league currently selected. Please start by selecting a league.")
            
        for option in footballOptions:
            print(option[0])
            availableOptions.append(option[1])

        while selection not in availableOptions:
            selection = input()

        for option in footballOptions:
            if selection == "m":
                exitMenu = True
                break
            if selection == option[1]:
                option[2]()
                selection = ""

footballOptions = [["(1) League select*", "1", leagueSelect],#The leagueSelect function needs to return a list of leagues
                   ["(2) Download upcoming fixtures*", "2", downloadFixtures],
                   ["(3) Display upcoming fixtures*", "3", displayFixtures],
                   ["(4) Run analytics on upcoming fixtures*", "4", analyseFixtures],
                   ["(5) Display analytics in upcoming fixtures*", "5", displayAnalysis],
                   ["(6) Single game analysis from fixture list*", "6", singleGameAnalysis],
                   ["(7) Manual single game analysis*", "7", manualGameAnalysis],
                   ["(8) Reports*", "8", reports],
                   ["(M) Main menu*", "m", leave]
                   ]

footballMenu(footballOptions)
        
