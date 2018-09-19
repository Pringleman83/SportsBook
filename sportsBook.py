from footballMenu import footballMenu

def isNumber(s):
    """
    Tests if the value passed is a number.
    Returns True or False.
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def tennis():
    """
    Placeholder for Tennis selection.
    Serves no function except for menu testing.
    """
    print("The tennis option is a placeholder for testing. The option is not currently available. \n\n")

# options list can only now be declared (after its functions have been)
options = [[1, "Football", footballMenu],[2, "Tennis", tennis], ["Q", "Quit"]]

def mainMenu(options):
    """
    Main menu function
    Offers all options in the options list (no need to edit this function)
    Returns the selected funtion to run.
    """ 
    while True:
        print("Welcome to SportsBook - A sports analysis tool.")
        print("Please select from one of the following sports:")
        # Display all options
        for option in options:
            print(str(option[0]) + " " + str(option[1]))
        # Take user selection
        while True:
            print("Enter option: ")
            selected = input()
            # Quit option
            if selected.lower() == "q":
                exit()
            # If a number has been entered, convert the string to an integer
            if isNumber(selected):
                selected = int(selected)
                # If the selection is in the list break out of the infinite loop
                if selected in range(len(options)) and selected != 0:
                    break
        # Having broken out of the loop, run the selected function
        for option in options:
            if selected == option[0]:
                option[2]()

# As this is the main file, call up the main menu    
mainMenu(options)


