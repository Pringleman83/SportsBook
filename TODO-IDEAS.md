# Branch OOP-B
# -Surister


The basic idea is to have a main class -> sportsBoo.py/ class MainMenu that inherits from 

AbstractUtility (AU in short, old commonFunctions), this may change in the future 
if the class AU is filled with a lot of methods and MainMenu only uses a few one, wouldn't 
make any sense to inherit these many methods and only use a few, might either make two 
utility abstract classes or have MainCLass just have those, we'll see.

MainMenu will also inherit from a Display Class that will take care of the whole menus & 
submenus display, this display class will also inherit or just get passed (will see) a sport
Class that will act differently depending a variable or something given, therefore the
Sport class could act as 'Tennis' or 'Football'. Question is, where will the whole prediction,
the actual math take place, maybe another abstract class Prediction and just have Sport class
create an instance of it depending on the sport and just have all the info Display? that's my
quickest take on it, feel free to open an issue on this branch and discuss the design pattern.


For instance as how the branch is now, experiment.py and class_sample.py will be deleted as 
it makes no sense to have different design patterns in the same branch, as every design pattern
should have its own branch.
football.py and footballMenu.py are still here on their functional form since they haven't been converted
into classes yet.

Question that I still hold myself and will think about it, about the league_and_team_classes.py
design pattern, is it really necessary to have a Team Class? maybe yeah if we want to perhaps in 
the future add some more functionalities. Surister, WED-OCT-17 - 11:44


# parse_args function has to be review to whether it is useful or not
