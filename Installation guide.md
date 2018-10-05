How to install sportsBook.

In order to use sportsBook you will need:

-python
-pipenv
-git (optional)

This would be the steps to follow.



1. Getting the files.


[Using git]
- Installing git 

            -> There are different ways:

                * Download and install git from https://git-scm.com/
                * run your package manager commands: 
                                        
                        $ pacman -S git 
                        $ pt-get install git 
                        ... see your package manager documentation.
                                            
                                            
- Git clone the project



           -> Open a terminal in your desired location and run this command:
                
                $ git clone https://github.com/Pringleman83/SportsBook.git
                
                
[Without git]

- Download the files from https://github.com/Pringleman83/SportsBook/archive/master.zip


2. Getting pipenv


[With pip] 

Remember that pip comes bundled with python although some linux version do not

-run          
                    $ pip install pipenv
                    
[Without pip]

- Install pipenv from your proffered package manager
        
        Mac             $ brew install pipenv
        Arch            $ pacman -S pipenv
        Fedora28        $ sudo dnf install pipenv
        Ubuntu          $ apt-install 
        ... for more 
        
3. Installing the packages.

- Once you have python, pipenv and the files, open the terminal on the files' folder and run:

                    $ pipenv sync
                    
                Now pipenv will install every package you need.
                
4. Run sportsBook.py

                    $ pipenv run python sportsBook.py