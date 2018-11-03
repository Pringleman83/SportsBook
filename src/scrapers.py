#Scrapers

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import commonFunctions as cf
from datetime import datetime

def get_league_data_bet_study(selection, league_data, fixtures, available_leagues):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from bedstudy.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    
    Scrapes the next 15 fixtures of the selected league.
    Adds them to the fixtures list.
    """
    
    def format_datetime(dt):
        """
        Helper function to convert date and time value for a
        game from the SoccerStats scraper and converts it into
        a valid datetime object. The object is returned.
        """

        # Game date day (1-31) number
        game_date_day = int(dt[:2])
        
        # Month number
        game_date_month = int(dt[3:5])
        
        # Year number
        game_date_year = int(dt[6:10])
        # Time
        game_hour = int(dt[12:14])
        game_min = int(dt[15:17])

        game_date = datetime(game_date_year, game_date_month,
                             game_date_day, game_hour, game_min)
        
        return game_date

    bet_study_main = "https://www.betstudy.com/soccer-stats/"
    season = "c/"  # c is current
    full_url = bet_study_main + season + available_leagues[selection]
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("\nCannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.read()
    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("div", {"id": "tab03_"})
    
    team_count = 0 # Keep a count of how many teams have been detected in the league

    for i in range(1, 50): # Support for leagues of up to 50 teams.
        try:
            # Initial scrape also determines if another team is present in the current league
            position = int(table.select('td')[((i-1)*16)].text)
        except:
            # If no teams have yet been added, there is an error.
            if team_count == 0:
                print("\n" + selection + "\nWeb page error - Check url integrity and website status.")
                return "Scrape error"
            # If teams have been added, the loop has reached the end of the table
            else:
                break
                
        # Another team is present as "break" hasn't been called - continue scrape
        
        #position = int(table.select('td')[((i-1)*16)].text) # Commented out as this is now the test for the presence of a team.
        team_name = table.select('td')[((i-1)*16)+1].text
        home_played = int(table.select('td')[((i-1)*16)+2].text)
        home_won = int(table.select('td')[((i-1)*16)+3].text)
        home_drew = int(table.select('td')[((i-1)*16)+4].text)
        home_lost = int(table.select('td')[((i-1)*16)+5].text)
        home_for = int(table.select('td')[((i-1)*16)+6].text)
        home_against = int(table.select('td')[((i-1)*16)+7].text)
        home_points = int(table.select('td')[((i-1)*16)+8].text)
        away_played = int(table.select('td')[((i-1)*16)+9].text)
        away_won = int(table.select('td')[((i-1)*16)+10].text)
        away_drew = int(table.select('td')[((i-1)*16)+11].text)
        away_lost = int(table.select('td')[((i-1)*16)+12].text)
        away_for = int(table.select('td')[((i-1)*16)+13].text)
        away_against = int(table.select('td')[((i-1)*16)+14].text)
        away_points = int(table.select('td')[((i-1)*16)+15].text)
        
        # Calculated values
        total_played = home_played + away_played
        total_won = home_won + away_won
        total_drew = home_drew + away_drew
        total_lost = home_lost + away_lost
        total_for = home_for + away_for
        total_against = home_against + away_against
        total_points = home_points + away_points
        
        # Inline code to tidily avoid division by zero errors
        home_won_per_game = 0 if home_played == 0 else round(home_won / home_played, 3)
        home_drew_per_game = 0 if home_played == 0 else round(home_drew / home_played, 3)
        home_lost_per_game = 0 if home_played == 0 else round(home_lost / home_played, 3)
        home_for_per_game = 0 if home_played == 0 else round(home_for / home_played, 3)
        home_against_per_game = 0 if home_played == 0 else round(home_against / home_played, 3)
        home_points_per_game = 0 if home_played == 0 else round(home_points / home_played, 3)
        away_won_per_game = 0 if away_played == 0 else round(away_won / away_played, 3)
        away_drew_per_game = 0 if away_played == 0 else round(away_drew / away_played, 3)
        away_lost_per_game = 0 if away_played == 0 else round(away_lost / away_played, 3)
        away_for_per_game = 0 if away_played == 0 else round(away_for / away_played, 3)
        away_against_per_game = 0 if away_played == 0 else round(away_against / away_played, 3)
        away_points_per_game = 0 if away_played == 0 else round(away_points / away_played, 3)
        total_won_per_game = 0 if total_played == 0 else round(total_won / total_played, 3)
        total_drew_per_game = 0 if total_played == 0 else round(total_drew / total_played, 3)
        total_lost_per_game = 0 if total_played == 0 else round(total_lost / total_played, 3)
        total_for_per_game = 0 if total_played == 0 else round(total_for / total_played, 3)
        total_against_per_game = 0 if total_played == 0 else round(total_against / total_played, 3)
        total_points_per_game = 0 if total_played == 0 else round(total_points / total_played, 3)

        # Add league to the leagueData dictionary if the league does not already exist within it.
        # Any additional stats calculated above must be added to the dictionary generator here.
        if selection not in league_data:
            league_data[selection] = {
                team_name:
                    {"Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                              "For": home_for, "Against": home_against, "Points": home_points,
                              "Won per Game": home_won_per_game, "Drew per Game": home_drew_per_game,
                              "Lost per Game": home_lost_per_game, "For per Game": home_for_per_game,
                              "Against per Game": home_against_per_game, "Points per Game": home_points_per_game},
                     "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                              "For": away_for, "Against": away_against, "Points": away_points,
                              "Won per Game": away_won_per_game, "Drew per Game": away_drew_per_game,
                              "Lost per Game": away_lost_per_game, "For per Game": away_for_per_game,
                              "Against per Game": away_against_per_game, "Points per Game": away_points_per_game},
                     "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                              "For": total_for, "Against": total_against, "Points": total_points,
                              "Won per Game": total_won_per_game, "Drew per Game": total_drew_per_game,
                              "Lost per Game": total_lost_per_game, "For per game": total_for_per_game,
                              "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                     }
                }

        # If the league does already exist, just update the teams and statistics.
        else:
            league_data[selection][team_name] = {

                 "Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                          "For": home_for, "Against": home_against, "Points": home_points,
                          "Won per Game": home_won_per_game, "Drew per Game": home_drew_per_game,
                          "Lost per Game": home_lost_per_game, "For per Game": home_for_per_game,
                          "Against per Game": home_against_per_game, "Points per Game": home_points_per_game},
                 "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                          "For": away_for, "Against": away_against, "Points": away_points,
                          "Won per Game": away_won_per_game, "Drew per Game": away_drew_per_game,
                          "Lost per Game": away_lost_per_game, "For per Game": away_for_per_game,
                          "Against per Game": away_against_per_game, "Points per Game": away_points_per_game},
                 "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                           "For": total_for, "Against": total_against, "Points": total_points,
                           "Won per Game": total_won_per_game, "Drew per Game": total_drew_per_game,
                           "Lost per Game": total_lost_per_game, "For per Game": total_for_per_game,
                           "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                 }
        team_count += 1

    # Get fixtures
    fixtures_url = "d/fixtures/"
    full_url = bet_study_main + season + available_leagues[selection] + fixtures_url
    
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("Cannot retrieve data, webpage is down.")
        return "Scrape error"
    web_html = web_client.read()

    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("table", {"class": "schedule-table"})
    
    number_of_games = 500 # Enough games to include the rest of each season's fixtures
    
    #fixture list 0.text league, 2.text date and time, 1.text home team, 3.text away team
    #fixture list 5              7                     6                 8
    fixture = []
    
    while True:
        try:
            # Scrape the number of requested fixtures and then break out of the loop.
            
            # Each fixture contains 5 cells
            # Multiply the number of games required by 5
            # Produce a list of the 4 of 5 cells needed for each game
            # Add list to fixture list
            for i in range(0,number_of_games * 5, 5):
                date_time_str = str(table.select('td')[i].text)\
                + "  " + str(table.select('td')[i + 2].text)
                
                game_date_time = format_datetime(date_time_str)
                
                fixture = [selection,
                    game_date_time.strftime("%d %b %Y %H:%M"),
                    str(table.select('td')[i + 1].text),
                    str(table.select('td')[i + 3].text),
                    game_date_time]
                
                # Only add the fixture to the fixtures list if it's not already present.
                if not fixture in fixtures:
                    fixtures.append(fixture[:]) # add fixture details to fixtures                    
            break
        except IndexError:
            # Number of requested fixtures exceeds the number of available fixtures, break.
            break
    return "Success"

def get_league_data_soccer_stats(selection, league_data, fixtures, available_leagues):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from soccerstats.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    
    Scrapes all results and fixtures of the current season.
    """
    #print("===" + str(selection) + "===") #DEBUG CODE
    
    def clean_string(st):
        """
        Helper function to clean the team name strings.
        """
        new_string = st.replace("\u00a0","")
        return new_string
        
    def clear_whitespace_characters(st):
        """
        Helper function to strip whitespace characters leaving spaces.
        """
        new_string = st.replace("\xa0", "")
        new_string = new_string.replace("\r", "")
        new_string = new_string.replace("\n", "")
        return new_string
    
    def limit_characters(st):
        """
        Helper function to convert all various forms punctuation to one common type.
        Code being added as problems arise.
        This helps to ensure teams in fixture lists match those in leagues.
        """
        new_string = st.replace("`", "'")
        new_string = new_string.replace("´", "'")
        new_string = new_string.replace("\x8a", "")
        return new_string
        
    def format_datetime(dt):
        """
        Helper function to convert date and time value for a
        game from the SoccerStats scraper and converts it into
        a valid datetime object. The object is returned.
        """
        
        today = datetime.today()
        date_months = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.",
            "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
        days = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

        # Game date day (1-31) number
        if cf.is_number(dt[5]):
            game_date_day = dt[5]
            if cf.is_number(dt[6]):
                game_date_day += dt[6]
                month_index = 8
            else:
                month_index = 7
        game_date_day = int(game_date_day)

        # Game day (0 - 6) number
        game_day = dt[0:4]
        for day in days:
            if game_day == day:
                game_day_number = days.index(day)
                break
        
        # Month number
        for date_month in date_months:
            if dt[month_index:month_index + 4] == date_month:
                game_month = date_months.index(date_month) + 1
                break

        # Time
        game_hour = int(dt[month_index + 6:month_index + 8])
        game_min = int(dt[month_index + 10:month_index + 12])
        
        # Year number
        game_date = datetime(today.year, game_month, game_date_day,
                                      game_hour, game_min)
        
        if days[game_date.weekday()] != game_day:
            game_date = datetime(today.year - 1 , game_month, game_date_day,
                                          game_hour, game_min)
        if days[game_date.weekday()] != game_day:
            game_date = datetime(today.year + 1 , game_month, game_date_day,
                                          game_hour, game_min)
        if days[game_date.weekday()] != game_day:
            game_date = datetime(1111 , game_month, game_date_day,
                                          game_hour, game_min)
        return game_date

    soccer_stats_main = "https://www.soccerstats.com/widetable.asp?league="
    full_url = soccer_stats_main + available_leagues[selection]
    cookies = {"cookiesok": "yes"} # Required to disable the cookie popup which prevents scraping.
    web_client = requests.get(full_url, cookies = cookies)
    if web_client.status_code != 200:
        print("\nCannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.content
    web_soup = soup(web_html, "html.parser")
    """
    Table
    Pos-Team-Pld-W-D-L-F-A-GD-PTS--Wh-Dh-Lh-GFh-GAh--Wa-Da-La-GFa-GAa
    0  - 1  - 2 -3-4-5-6-7-8 - 9 --13-14-15-16 -17 --24-25-26-27 -28
    """
    
    table = web_soup.find("tbody")
 
    team_count = 0 # Keep a count of how many teams have been detected in the league

    for i in range(1, 50): # Support for leagues of up to 50 teams.
        try:
            # Initial scrape also determines if another team is present in the current league
            position = int(table.select('td')[((i-1)*29)].text)
        except:
            # If no teams have yet been added, there is an error.
            if team_count == 0:
                print("\n" + selection + "\nWeb page error - Check url integrity and website status.")
                return "Scrape error"
            # If teams have been added, the loop has reached the end of the table
            else:
                break
              
        # Another team is present as "break" hasn't been called - continue scrape
        
        #position = int(table.select('td')[((i-1)*22)].text) # Commented out as this is now the test for the presence of a team.
        team_name = limit_characters(clean_string(table.select('td')[((i-1)*29)+1].text))

        home_won = int(table.select('td')[((i-1)*29)+13].text)
        home_drew = int(table.select('td')[((i-1)*29)+14].text)
        home_lost = int(table.select('td')[((i-1)*29)+15].text)
        home_for = int(table.select('td')[((i-1)*29)+16].text)
        home_against = int(table.select('td')[((i-1)*29)+17].text)

        away_won = int(table.select('td')[((i-1)*29)+24].text)
        away_drew = int(table.select('td')[((i-1)*29)+25].text)
        away_lost = int(table.select('td')[((i-1)*29)+26].text)
        away_for = int(table.select('td')[((i-1)*29)+27].text)
        away_against = int(table.select('td')[((i-1)*29)+28].text)
        
        # Calculated values
        home_played = home_won + home_drew + home_lost
        home_points = (home_won * 3) + home_drew
        away_played = away_won + away_drew + away_lost
        away_points = (away_won * 3) + away_drew
        total_played = home_played + away_played
        total_won = home_won + away_won
        total_drew = home_drew + away_drew
        total_lost = home_lost + away_lost
        total_for = home_for + away_for
        total_against = home_against + away_against
        total_points = home_points + away_points
        
        # Inline code to tidily avoid division by zero errors
        home_won_per_game = 0 if home_played == 0 else round(home_won / home_played, 3)
        home_drew_per_game = 0 if home_played == 0 else round(home_drew / home_played, 3)
        home_lost_per_game = 0 if home_played == 0 else round(home_lost / home_played, 3)
        home_for_per_game = 0 if home_played == 0 else round(home_for / home_played, 3)
        home_against_per_game = 0 if home_played == 0 else round(home_against / home_played, 3)
        home_points_per_game = 0 if home_played == 0 else round(home_points / home_played, 3)
        away_won_per_game = 0 if away_played == 0 else round(away_won / away_played, 3)
        away_drew_per_game = 0 if away_played == 0 else round(away_drew / away_played, 3)
        away_lost_per_game = 0 if away_played == 0 else round(away_lost / away_played, 3)
        away_for_per_game = 0 if away_played == 0 else round(away_for / away_played, 3)
        away_against_per_game = 0 if away_played == 0 else round(away_against / away_played, 3)
        away_points_per_game = 0 if away_played == 0 else round(away_points / away_played, 3)
        total_won_per_game = 0 if total_played == 0 else round(total_won / total_played, 3)
        total_drew_per_game = 0 if total_played == 0 else round(total_drew / total_played, 3)
        total_lost_per_game = 0 if total_played == 0 else round(total_lost / total_played, 3)
        total_for_per_game = 0 if total_played == 0 else round(total_for / total_played, 3)
        total_against_per_game = 0 if total_played == 0 else round(total_against / total_played, 3)
        total_points_per_game = 0 if total_played == 0 else round(total_points / total_played, 3)

        # Add league to the leagueData dictionary if the league does not already exist within it.
        # Any additional stats calculated above must be added to the dictionary generator here.
        if selection not in league_data:
            league_data[selection] = {
                team_name:
                    {"Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                              "For": home_for, "Against": home_against, "Points": home_points,
                              "Won per Game": home_won_per_game, "Drew per Game": home_drew_per_game,
                              "Lost per Game": home_lost_per_game, "For per Game": home_for_per_game,
                              "Against per Game": home_against_per_game, "Points per Game": home_points_per_game},
                     "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                              "For": away_for, "Against": away_against, "Points": away_points,
                              "Won per Game": away_won_per_game, "Drew per Game": away_drew_per_game,
                              "Lost per Game": away_lost_per_game, "For per Game": away_for_per_game,
                              "Against per Game": away_against_per_game, "Points per Game": away_points_per_game},
                     "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                              "For": total_for, "Against": total_against, "Points": total_points,
                              "Won per Game": total_won_per_game, "Drew per Game": total_drew_per_game,
                              "Lost per Game": total_lost_per_game, "For per game": total_for_per_game,
                              "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                     }
                }

        # If the league does already exist, just update the teams and statistics.
        else:
            league_data[selection][team_name] = {

                 "Home": {"Played": home_played, "Won": home_won, "Drew": home_drew, "Lost": home_lost,
                          "For": home_for, "Against": home_against, "Points": home_points,
                          "Won per Game": home_won_per_game, "Drew per Game": home_drew_per_game,
                          "Lost per Game": home_lost_per_game, "For per Game": home_for_per_game,
                          "Against per Game": home_against_per_game, "Points per Game": home_points_per_game},
                 "Away": {"Played": away_played, "Won": away_won, "Drew": away_drew, "Lost": away_lost,
                          "For": away_for, "Against": away_against, "Points": away_points,
                          "Won per Game": away_won_per_game, "Drew per Game": away_drew_per_game,
                          "Lost per Game": away_lost_per_game, "For per Game": away_for_per_game,
                          "Against per Game": away_against_per_game, "Points per Game": away_points_per_game},
                 "Total": {"Played": total_played, "Won": total_won, "Drew": total_drew, "Lost": total_lost,
                           "For": total_for, "Against": total_against, "Points": total_points,
                           "Won per Game": total_won_per_game, "Drew per Game": total_drew_per_game,
                           "Lost per Game": total_lost_per_game, "For per Game": total_for_per_game,
                           "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                 }
        team_count += 1


    # Get fixtures and results
    
    fixtures_url = "&tid=a"
    soccer_stats_main = "https://www.soccerstats.com/table.asp?league="
    full_url = soccer_stats_main + available_leagues[selection] + fixtures_url
    cookies = {"cookiesok": "yes"} # Required to disable the cookie popup which prevents scraping.
    web_client = requests.get(full_url, cookies = cookies)
    if web_client.status_code != 200:
        print("\nCannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.content
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find_all("div", {"class", "twelve columns"})[1]   
    
    # Create an empty list to store each result as an external list doesn't yet exist
    results = []
    
    days = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]
    played = ""
    cell = table.select('td')
    round_number = ""
    """
    #DEBUG CODE
    for i in range(0,(len(cell) - 3)):
        # Avoid the major content carrying <td> tags.
        if len(str(table.select('td')[i].text)) > 100:
            continue
        print("==="+str(i)+"===")
        print(cell[i].text)
        print("==========\n")
    """
    
    for i in range(0,(len(cell) - 3)): # Cycle through all but the last 3 cells (as they are accessed through addition)
        #print(str(i)) # DEBUG CODE
        # Avoid the major content carrying <td> tags.
        if len(str(table.select('td')[i].text)) > 100:
            continue
        if "Round" in str(cell[i].text):
            round_number = clear_whitespace_characters(str(cell[i].text))
        
        if round_number == "": # Skip to next iteration if no round number has been found.
            continue
            
        if str(cell[i].text)[:4] in days: # If the first four characters of the cell are a day.
            #print("TEST") # DEBUG CODE
            date_time = clear_whitespace_characters(str(cell[i].text))
            teams = str(cell[i+1].text)[1:].split(" - ") # Remove first character for tidying and split into a list removing the separator.
            #print(type(cell[i+2].text)) # DEBUG CODE
            if clear_whitespace_characters(cell[i+2].text) != "":
                #print("PLAYED") # DEBUG CODE
                # Game has been played
                played = True
                score = clear_whitespace_characters(str(cell[i+2].text)).split(" - ") # Split into list removing separator.
                
                # If a score is not displayed (Eg. game postponed) add a second value to prevent error.
                if len(score) < 2:
                    score.append(score[0])
                
                home_team_score = score[0]
                away_team_score = score[1]
                
                # Commented out below code because this data is not available from all leagues Workaround to be implemented.
                #ht_score = clear_whitespace_characters(str(cell[i+3].text))
                #ht_score = ((ht_score.lstrip("(")).rstrip(")")).split("-") # Strip brackets and split into list removing spearator.
                #home_team_ht_score = ht_score[0]
                #away_team_ht_score = ht_score[1]
                

            else:
                # Game hasn't yet played
                #print("NOT PLAYED") # DEBUG CODE
                played = False
            
            # Run this code for played and unplayed games.
            # Separate home and away data.
            home_team = limit_characters(teams[0])
            away_team = limit_characters(teams[1])
    
            # Package results and fixtures.
            game_date_time = format_datetime(date_time)
  
            if played:
                result = [selection, game_date_time.strftime("%d %b %Y %H:%M"), home_team, home_team_score, away_team, away_team_score, game_date_time]
                # Omitted home_team_ht_score, away_team_ht_score
                # Only add the fixture to the fixtures list if it's not already present.
                if result not in results:
                    results.append(result[:]) # add result details to results
            else:
                fixture = [selection, game_date_time.strftime("%d %b %Y %H:%M"), home_team, away_team, game_date_time]
                # Only add the fixture to the fixtures list if it's not already present.
                if fixture not in fixtures:
                    fixtures.append(fixture[:]) # add fixture details to fixtures
    return "Success"