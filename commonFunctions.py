#Useful functions


def is_number(s) -> bool:
    """
    Tests if the value passed is a number.
    Returns True or False.
    """
    if isinstance(s, str):
        return s.isnumeric()
    return isinstance(s, int) or isinstance(s, float)


def valid_input(selection, options) -> bool:
    """
    Takes the user's selection and a list of valid options.
    Returns True if the selection is in the list.
    Returns False if it's not.
    """
    if isinstance(selection, str):
        if selection.isnumeric():
            selection = int(selection)
    return selection in options
