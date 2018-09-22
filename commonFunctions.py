#Useful functions

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
    
def validInput(selection, options):
    """
    Takes the user's selection and a list of valid options.
    Returns True if the selection is in the list.
    Returns False if it's not.
    """
    for option in options:
        if str(selection) == str(option):
            return True       
    return False
