import commonFunctions as cf

def both_to_score(predictions, applied_filters):
    """
    Takes a list of predictions and currently applied filters.
    Returns all predictions where both teams are expected to score and the updated applied filters list.
    """
    print("(Both teams to score)\n")
    filtered_predictions = []
    for p in predictions:
        if p["Home team prediction"] > 0 and p["Away team prediction"] > 0:
            filtered_predictions.append(p)
    applied_filters.append("Both to score")
    return (filtered_predictions, applied_filters)

def bore_draw(predictions, applied_filters):
    """
    Takes a list of predictions and the currently applied filters.
    Returns all predictions where the resulted is expected to be nil nil and
    the updated applied filters list.
    """
    print("(No score draws)\n")
    filtered_predictions = []
    for p in predictions:
        if p["Total goals"] == 0:
            filtered_predictions.append(p)
    applied_filters.append("0-0 draws")
    return (filtered_predictions, applied_filters)  

def win_by_x(predictions, applied_filters):
    """
    Takes a list of predictions and the currently applied filters.
    Asks the user to select home team, away team or either.
    Asks the user how many goals the filtered prediction should show that team winning by.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    filtered_predictions = []
    while True:
        print("Win by x goals\n\n Which team to win?\n(H)ome team, (A)way team or (E)ither?\n")
        print("Enter H, A, E or M to return to previous menu making no changes.")
        s = input().lower()
        if s == "h":
            team = "Home"
            break
        elif s == "a":
            team = "Away"
            break
        elif s == "e":
            team = "Either"
            break
        elif s == "m":
            return(predictions, applied_filters)
    while True:
        print("\nby how many goals? (Please enter a number)")
        x = input()
        if cf.is_number(x):
            x = int(x)
            break
        
    for p in predictions:
        if s == "h":
            if p["Home team prediction"] - p["Away team prediction"] > x:
                filtered_predictions.append(p)        
        elif s == "a":
            if p["Away team prediction"] - p["Home team prediction"] > x:
                filtered_predictions.append(p)
        elif s == "e":
            if p["Home team prediction"] - p["Away team prediction"] > x or p["Away team prediction"] - p["Home team prediction"] > x:
                filtered_predictions.append(p)
                
    applied_filters.append(team + " team to score " + str(x) + " goals more than their opponent.")
    return (filtered_predictions, applied_filters)

def x_or_more_goals_scored(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user how many goals expected to be scored at least.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    print("(x or more goals scored)\n")
    filtered_predictions = []
    while True:

        print("Enter the lowest number of goals")
        x = input()
        if cf.is_number(x):
            x = int(x)
            break
        
    for p in predictions:
        if p["Total goals expected"] >= x:
            filtered_predictions.append(p)  
    applied_filters.append("Total number of goals is " + str(x) + " or more.")    
    return (filtered_predictions, applied_filters)
    
def x_or_less_goals_scored(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Asks the user how many goals expected to be scored at most.
    Returns a list of predictions that fit the requested specification and the
    updated applied filters list.
    """
    print("(x or less goals scored)\n\n")
    filtered_predictions = []
    while True:
        print("\nX goals or less expected to be scored in each game.")
        print("Enter the highest number of goals")
        x = input()
        if cf.is_number(x):
            x = int(x)
            break
        
    for p in predictions:
        if p["Total goals expected"] >= x:
            filtered_predictions.append(p)  
    applied_filters.append("Total number of goals is " + str(x) + " or less.")
    return (filtered_predictions, applied_filters)

# Special filters

def special_james_shoemark_bts(predictions, applied_filters):
    """
    Takes a list of predictions and the list of currently applied filters.
    Returns a list of predictions where total goals expected is over 4 and both teams are expected to score at least one goal along with the updated applied filters list.
    """
    print("(x or less goals scored)\n\n")
    filtered_predictions = []
    
    for p in predictions:
        if p["Total goals expected"] > 4 and p["Home team prediction"] > 1 and p["Away team prediction"] > 1:
            filtered_predictions.append(p)
            
    applied_filters.append("James Shoemark special selection")
    return (filtered_predictions, applied_filters)