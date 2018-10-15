#Class experimentation
from footballMenu import football_menu
import commonFunctions as cf

class Menu:
    """
    A general purpose menu class for creating menus.
    Takes at least a title and a list. Each item in the list is a second list of option name,
    function and individual arguments (up to 3).
    Eg. menu = Menu("Main Menu",[["Football", football_menu, league_data, fixtures, predictions],
                                 ["Tennis", tennis]])
    Can take the following optional arguments:
    
    intro_string - A string to introduce the menu.
    
    main_menu - A boolean value to determine whether this is the top level menu.
    
    multi_choice - A boolean value to determine whether the user should be allowed to select
    multiple options.
    
    
    """
    
    def __init__(self, title, menu_list, intro_string = "", main_menu = False, multi_choice = False):
    
        self.title = title
        self.menu_list = menu_list
        self.intro_string = intro_string
        self.main_menu = main_menu
        self.multi_choice = multi_choice
        
    def display_menu(self):
        """
        Main menu function
        Offers all options in the menu_dictionary.
        Returns the selected function to run.
        """
        print("\n" + self.title)
        print("=" * len(self.title) + "\n")
        item_number = 1
        for item in self.menu_list:
            print(f"{item_number} : {item[0]}")
            item_number += 1
        
        if self.main_menu:
            print("Q : Quit")
        else:
            print("M : Previous menu")
        
        if self.multi_choice:
            # Necessary loop for input validation
            #print("Please select all of the required above options separating each choice with a comma.")
            choices = input()
            # Some code to make a list of numbers from the input
            print(choices) # For debugging / testing
        else:
            # Necessary loop for input validation
            print("Please select one of the above options")
            choice = input()
            #print(choice) # For debugging / testing
            
            # This is ugly. It's the only way I know to pass arguments to a listed function from a list.
            # It means that the function in the menu_list list can have from 0 to 3 arguments.
            # If we need a menu object to deal with larger functions, this can easily be grown.
            # There has to be a better way!
            
            if cf.is_number(choice):
                choice = int(choice) - 1 # As the list displayed starts at one and the list index starts at 0.
            if len(self.menu_list[choice]) == 2:
                self.menu_list[choice][1]()# Run the assigned function with no arguments
            if len(self.menu_list[choice]) == 3:
                self.menu_list[choice][1](self.menu_list[choice][2])# Run the assigned action with one argument
            if len(self.menu_list[choice]) == 4:
                self.menu_list[choice][1](self.menu_list[choice][2], self.menu_list[choice][3])# Run the assigned action with two arguments
            if len(self.menu_list[choice]) == 5:
                self.menu_list[choice][1](self.menu_list[choice][2], self.menu_list[choice][3], self.menu_list[choice][4])# Run the assigned action with three arguments
                
#Example creation of a menu object:
#First insure access to functions (either by importing relevant files or declaration)
def tennis():
    """
    Placeholder for Tennis selection.
    Serves no function except for menu testing.
    """
    print("The tennis option is a placeholder for testing.")
    print("The option is not supported in this build. \n\n")

# Ensure access to the necessary variables.
league_data = {}
fixtures = []
predictions = []

# Create a list of menu items. Each item is itself a list as follows:
#["Item name", function, argument1, argument2, argument3] to a maximum of 3 arguments (for now)
main_menu_list = [["Football", football_menu, league_data, fixtures, predictions],
                 ["Tennis", tennis]]

# Print any pretext
print("Welcome to SportsBook")
print("=====================")

#Create a menu item
main_menu = Menu("Main Menu", main_menu_list, main_menu = True)

# Display the menu
main_menu.display_menu()