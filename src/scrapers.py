#Scrapers
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import commonFunctions as cf
from datetime import datetime
import threading

# Threading locks prevent multiple threads from accessing variables at the same time.
league_data_lock = threading.Lock()
fixtures_lock = threading.Lock()
results_lock = threading.Lock()

def get_league_data_bet_study(selection, league_data, fixtures, results, available_leagues):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from bedstudy.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    
    Scrapes the all available fixtures of the selected league.
    Adds them to the fixtures list.
    
    Scrapes all available results for the selected league.
    Adds them to the results list.
    """
    today = datetime.today()
    def format_datetime(dt, mode = "fixture"):
        """
        Helper function to convert date and time value for a
        game from the BetStudy scraper and converts it into
        a valid datetime object. The object is returned.
        
        Takes the scraped date (and time if available) and an
        optional string for mode (default "fixture").
        
        Behaves differently for each mode.
        """       
        if mode == "fixture":
            # Game date day (1-31) number
            game_date_day = int(dt[:2])
            
            # Month number
            game_date_month = int(dt[3:5])
            
            # Year number
            game_date_year = int(dt[6:10])
            
            # Time
            # Default time 0000 when no time present
            if "-" in dt[12:14]:
                game_hour = 00
                game_min = 00
            else:
                game_hour = int(dt[12:14]) 
                game_min = int(dt[15:17])

            game_date = datetime(game_date_year, game_date_month,
                                 game_date_day, game_hour, game_min)
                          
        elif mode == "result":
        
            date = dt.split(".")
            
            # Game date day (1-31) number
            game_date_day = int(date[0])
            
            # Month number
            game_date_month = int(date[1])
            
            # Year number
            game_date_year = int(date[2])

            game_date = datetime(game_date_year, game_date_month,
                                 game_date_day)
        return game_date

    bet_study_main = "https://www.betstudy.com/soccer-stats/"
    season = "c/"  # c is current
    full_url = bet_study_main + season + available_leagues[selection]
    web_client = uReq(full_url)
    #print(full_url)
    if web_client.getcode() != 200:
        print("\n" + selection + " league data error: Cannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.read()
    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("div", {"id": "tab03_"})

    for i in range(1, 50): # Support for leagues of up to 50 teams.
        try:
            # Initial scrape also determines if another team is present in the current league
            # Variable only currently used for this error check purpose.
            position = int(table.select('td')[((i-1)*16)].text)
        except:
            # If no teams have yet been added, there is an error.
            if i == 1:
                print("\n" + "\nError scraping "+ selection + "\nThe league may be in group or playoff stages or the web site could be experiencing problems.")
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
        home_won_per_game = 0 if not home_played else round(home_won / home_played, 3)
        home_drew_per_game = 0 if not home_played else round(home_drew / home_played, 3)
        home_lost_per_game = 0 if not home_played else round(home_lost / home_played, 3)
        home_for_per_game = 0 if not home_played else round(home_for / home_played, 3)
        home_against_per_game = 0 if not home_played else round(home_against / home_played, 3)
        home_points_per_game = 0 if not home_played else round(home_points / home_played, 3)
        away_won_per_game = 0 if not away_played else round(away_won / away_played, 3)
        away_drew_per_game = 0 if not away_played else round(away_drew / away_played, 3)
        away_lost_per_game = 0 if not away_played else round(away_lost / away_played, 3)
        away_for_per_game = 0 if not away_played else round(away_for / away_played, 3)
        away_against_per_game = 0 if not away_played else round(away_against / away_played, 3)
        away_points_per_game = 0 if not away_played else round(away_points / away_played, 3)
        total_won_per_game = 0 if not total_played else round(total_won / total_played, 3)
        total_drew_per_game = 0 if not total_played else round(total_drew / total_played, 3)
        total_lost_per_game = 0 if not total_played else round(total_lost / total_played, 3)
        total_for_per_game = 0 if not total_played else round(total_for / total_played, 3)
        total_against_per_game = 0 if not total_played else round(total_against / total_played, 3)
        total_points_per_game = 0 if not total_played else round(total_points / total_played, 3)

        # Add league to the leagueData dictionary if the league does not already exist within it.
        # Any additional stats calculated above must be added to the dictionary generator here.
        
        if selection not in league_data:
            with league_data_lock:
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
                                  "Lost per Game": total_lost_per_game, "For per Game": total_for_per_game,
                                  "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                         }
                    }
        # If the league does already exist, just update the teams and statistics.
        else:
            with league_data_lock:
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

    # Get fixtures
    fixtures_url = "d/fixtures/"
    full_url = bet_study_main + season + available_leagues[selection] + fixtures_url
    
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("\n" + selection + " fixtures error: Cannot retrieve data, webpage is down")
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
                
                # Only add the fixture to the fixtures list if it's not already present and it is still to be played.
                if fixture not in fixtures and fixture[4] >= today:
                    with fixtures_lock:
                        fixtures.append(fixture[:]) # add fixture details to fixtures                    
            break
        except IndexError:
            # Number of requested fixtures exceeds the number of available fixtures, break.
            break
            
    # Get results
    results_url = "d/results/"
    full_url = bet_study_main + season + available_leagues[selection] + results_url
    
    web_client = uReq(full_url)

    if web_client.getcode() != 200:
        print("\n" + selection + " results error: Cannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.read()
    web_client.close()
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find("table", {"class": "schedule-table"})
    number_of_games = 500 # Enough games to include the rest of each season's results
    #result list 0.text date 04.11.2018, 2.text home team, 1.text score (1 - 0), 3.text away team, 4 icon/link (not used)
    #fixture list 5              7                     6                 8
    result = []
    
    # DEBUG CODE
    #print("Getting results")
    
    while True:
        try:
            # Scrape the number of requested results and then break out of the loop.
            
            # Each result contains 5 cells
            # Multiply the number of games required by 5
            # Produce a list of the 4 of 5 cells needed for each game
            # Add list to results list
            for i in range(0, number_of_games * 5, 5):
                
                #DEBUG CODE
                #print(str(table.select('td')[i].text))
                
                game_date = format_datetime(table.select('td')[i].text, mode = "result") # Correct date format for function?
                
                """
                Sorting the scores
                The scores are not always num - num ( eg. 1 - 1).
                Eg. if a game is postponed, it's Pstp.
                This code checks if a "-" is present and confirms that both scores 
                are numbers.
                If not, it just stores the strings in the most suitable way.
                """
                score_combined = table.select('td')[i + 2].text
                if "-" in score_combined:
                    if cf.is_number(score_combined.split("-")[0]) and cf.is_number(score_combined.split("-")[1]):
                        home_score = int(score_combined.split("-")[0])
                        away_score = int(score_combined.split("-")[1])
                    else:
                        home_score = score_combined.split("-")[0]
                        away_score = score_combined.split("-")[1]
                else:
                    home_score = score_combined
                    away_score = score_combined
                
                result = [selection, #League
                    game_date.strftime("%d %b %Y"), # Date as string
                    str(table.select('td')[i + 1].text), # Home team
                    home_score, # Home score
                    str(table.select('td')[i + 3].text), # Away team
                    away_score, # Away score
                    game_date] # Date as datetime object.
                
                #print(result) # DEBUG CODE
                
                # Only add the result to the results list if it's not already present.
                if not result in results:
                    
                    #DEBUG CODE
                    #print(str(i) + " added.")
                    
                    with results_lock:
                        results.append(result[:]) # add result details to results.                    
            break
        except IndexError:
            # Number of requested results exceeds the number of available results, break.
            break

    #print(results) # DEBUG CODE
    
    return "Success"

def get_league_data_soccer_stats(selection, league_data, fixtures, results, available_leagues):
    """
    Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from soccerstats.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    
    Scrapes all results and fixtures of the current season.
    """
    today = datetime.today()
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
        
    def format_datetime(dt, mode = "rounds"):
        """
        Helper function to convert date and time value for a
        game from the SoccerStats scraper and converts it into
        a valid datetime object. The object is returned.
        
        Runs in rounds mode by default but can be run in mode = "results" for
        the two forms of fixtures founf on the site.
        """
        today = datetime.today()
        date_months = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.",
            "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
        days = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]
        days1 = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        date_months1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        if mode == "rounds":
            
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
        elif mode == "results":
            # Game date day (1-31) number
            if cf.is_number(dt[4]):
                game_date_day = dt[3:5]
                month_index = 6
            else:
                game_date_day = dt[3]
                month_index = 5
            game_date_day = int(game_date_day)
            
            # Game day (0-6) number
            game_day = dt[0:2]
            for day in days1:
                if game_day == day:
                    game_day_number = days1.index(day)
                    break
            
            # Month number
            for date_month in date_months1:
                if dt[month_index : month_index + 3] == date_month:
                    game_month = date_months1.index(date_month) + 1
                    break
            
            # Time
            game_hour = int(dt[-5:-3])
            game_min = int(dt[-2:])
            
            # Year number
            game_date = datetime(today.year, game_month, game_date_day,
                                          game_hour, game_min)
            
            if days1[game_date.weekday()] != game_day:
                game_date = datetime(today.year - 1 , game_month, game_date_day,
                                              game_hour, game_min)
            if days1[game_date.weekday()] != game_day:
                game_date = datetime(today.year + 1 , game_month, game_date_day,
                                              game_hour, game_min)
            if days1[game_date.weekday()] != game_day:
                game_date = datetime(1111 , game_month, game_date_day,
                                              game_hour, game_min)
            """DEBUG CODE
            print("Game day = " + str(game_day))
            print("Date day number = " + str(game_date_day))
            print("Week day number = " + str(game_day_number))
            print("Month number " + str(game_month))
            print("Hour = " + str(game_hour))
            print("Min = " + str(game_min))
            print("Year = " + str(game_date.year))
            """
            
        return game_date
    soccer_stats_main = "https://www.soccerstats.com/widetable.asp?league="
    full_url = soccer_stats_main + available_leagues[selection]
    cookies = {"cookiesok": "yes"} # Required to disable the cookie popup which prevents scraping.
    web_client = requests.get(full_url, cookies = cookies)
    if web_client.status_code != 200:
        print("\n" + selection + " league data error: Cannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.content
    web_soup = soup(web_html, "html.parser")
    """
    Table
    Pos-Team-Pld-W-D-L-F-A-GD-PTS--Wh-Dh-Lh-GFh-GAh--Wa-Da-La-GFa-GAa
    0  - 1  - 2 -3-4-5-6-7-8 - 9 --13-14-15-16 -17 --24-25-26-27 -28
    """
    
    table = web_soup.find("tbody")
    for i in range(1, 50): # Support for leagues of up to 50 teams.
        try:
            # Initial scrape also determines if another team is present in the
            #current league
            # Variable is currently only used for this error check purpose.
            position = int(table.select('td')[((i-1)*29)].text)
        except:
            # If no teams have yet been added, there is an error.
            if i == 1:
                print("\n" + "\nError scraping "+ selection + "\nThe league may be in group or playoff stages or the website could be experiencing problems.")
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
        home_won_per_game = 0 if not home_played else round(home_won / home_played, 3)
        home_drew_per_game = 0 if not home_played else round(home_drew / home_played, 3)
        home_lost_per_game = 0 if not home_played else round(home_lost / home_played, 3)
        home_for_per_game = 0 if not home_played else round(home_for / home_played, 3)
        home_against_per_game = 0 if not home_played else round(home_against / home_played, 3)
        home_points_per_game = 0 if not home_played else round(home_points / home_played, 3)
        away_won_per_game = 0 if not away_played else round(away_won / away_played, 3)
        away_drew_per_game = 0 if not away_played else round(away_drew / away_played, 3)
        away_lost_per_game = 0 if not away_played else round(away_lost / away_played, 3)
        away_for_per_game = 0 if not away_played else round(away_for / away_played, 3)
        away_against_per_game = 0 if not away_played else round(away_against / away_played, 3)
        away_points_per_game = 0 if not away_played else round(away_points / away_played, 3)
        total_won_per_game = 0 if not total_played else round(total_won / total_played, 3)
        total_drew_per_game = 0 if not total_played else round(total_drew / total_played, 3)
        total_lost_per_game = 0 if not total_played else round(total_lost / total_played, 3)
        total_for_per_game = 0 if not total_played else round(total_for / total_played, 3)
        total_against_per_game = 0 if not total_played else round(total_against / total_played, 3)
        total_points_per_game = 0 if not total_played else round(total_points / total_played, 3)

        # Add league to the leagueData dictionary if the league does not already exist within it.
        # Any additional stats calculated above must be added to the dictionary generator here.
        if selection not in league_data:
            with league_data_lock:
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
                                  "Lost per Game": total_lost_per_game, "For per Game": total_for_per_game,
                                  "Against per Game": total_against_per_game, "Points per Game": total_points_per_game}
                         }
                    }

        # If the league does already exist, just update the teams and statistics.
        else:
            with league_data_lock:
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

    # Get fixtures and results
    
    fixtures_url = "&tid=a"
    soccer_stats_main = "https://www.soccerstats.com/table.asp?league="
    full_url = soccer_stats_main + available_leagues[selection] + fixtures_url
    cookies = {"cookiesok": "yes"} # Required to disable the cookie popup which prevents scraping.
    web_client = requests.get(full_url, cookies = cookies)
    if web_client.status_code != 200:
        print("\n" + selection + " fixtures error: Cannot retrieve data, webpage is down")
        return "Scrape error"
    web_html = web_client.content
    web_soup = soup(web_html, "html.parser")
    table = web_soup.find_all("div", {"class", "twelve columns"})[1] 
    
    """
    Data Hunting!
    table2r = web_soup.find_all("div", {"class", "six columns"})[2] # results
    table2f = web_soup.find_all("div", {"class", "six columns"})[3] # fixtures

    #tablex1 = web_soup.find_all("div", {"class", "six columns"})[0] # Nothing here
    #tablex2 = web_soup.find_all("div", {"class", "six columns"})[1] # Nothing here
    tablex3 = web_soup.find_all("div", {"class", "six columns"})[2] # Results
    tablex4 = web_soup.find_all("div", {"class", "six columns"})[3] # Fixtures
    
    #print("\n\n===Tablex 1 ===\n\n)")
    #print(tablex1)
    
    #print("\n\n===Tablex 2 ===\n\n)")
    #print(tablex2)
    
    #print("\n\n===Tablex 3 ===\n\n)")
    #print(tablex3)
    
    #print("\n\n===Tablex 4 ===\n\n)")
    #print(tablex4)
    
    cell = tablex4.select('td')
    
    for i in range(len(cell)):
        print("Length of cell" + str(i) + " is " + str(len(cell[i].text)))
        if len(cell[i].text) > 100:
            continue
        print(str(i) + str(cell[i]))
    
    quit()
    """
    # When studying the source; be aware that the site uses both types of quotes!
    
    #print(table2) # DEBUG CODE
    #print(table) # DEBUG CODE
    
    # Create an empty list to store each result as an external list doesn't yet exist
    
    days = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]
    days1 = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"]
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
    #print("CONTENT OF CELL 1 = " + clear_whitespace_characters(cell[1].text)) # DEBUG CODE
    if clear_whitespace_characters(cell[1].text) == "All results":
        #print("All results mode") # DEBUG CODE
        all_results_mode = True
    else:
        #print("Rounds") # DEBUG CODE
        all_results_mode = False
            
    if all_results_mode:
        # Alternative tables for the second formatting found on s.stats site.
        table2r = web_soup.find_all("div", {"class", "six columns"})[2] # results
        table2f = web_soup.find_all("div", {"class", "six columns"})[3] # fixtures
        for t in [table2f, table2r]:
            cell2 = t.select('td') # Switch table for results mode
            #print("Working all results mode") # DEBUG CODE
            
            for i in range(0,(len(cell2) - 3)): # Cycle through all but the last 3 cells (as they are accessed through addition)
                #print(str(i) + " - " + str(cell[i])) # DEBUG CODE
                # Avoid the major content carrying <td> tags.
                if len(str(cell2[i].text)) > 100:
                    continue
        
                #print(str(i) + " - " + str(cell2[i])) # DEBUG CODE display index and content of each cell
                
                #print("Date catch on: " + str(cell[i].text) + "Checking day: " + clear_whitespace_characters(cell[i].text)[:2] + ". Checking month: " + clear_whitespace_characters(cell[i].text)[-4:-1] + ".")
                
                if cell2[i].text[:2] in days1 and cell2[i].text[-4:-1] in months and cell2[i].text[2] == " ":#Result
                    #print("RESULT") # DEBUG CODE
                    date_timea = clear_whitespace_characters(str(cell2[i].text))
                    date_timeb = clear_whitespace_characters(str(cell2[i+1].text))
                    #print("DATE = " + str(date_timea) + "TIME = " + str(date_timeb)) # DEBUG CODE
                    date_time = date_timea + date_timeb
                    #print("DATETIME STRING = " + date_time) # DEBUG CODE
                    teams = str(cell2[i+2].text).split(" - ") # Strip leading space
                    if len(teams) < 2:
                        teams.append(teams[0])
                        print("Teams error in Results Mode Cell: " + str(i) + " content: " + str(cell2[i])) # Identification for new errors
                        
                    #print("HOME TEAM = " + teams[0] + " AWAY TEAM = " + teams[1]) # DEBUG CODE
    
                    #print("PLAYED") # DEBUG CODE
                    # Game has been played
                    played = True
                    
                    score = clear_whitespace_characters(str(cell2[i+3].text)).split(" - ") # Split into list removing separator.
                    
                    # If a score is not displayed (Eg. game postponed) add a second value to prevent error.
                    if len(score) < 2:
                        score.append(score[0])
                    
                    home_team_score = score[0]
                    away_team_score = score[1]
                    
                    game_date_time = format_datetime(date_time, mode = "results")
                    #print("HOME SCORE = " + str(home_team_score) + " AWAY TEAM SCORE = " + str(away_team_score)) # DEBUG CODE
                    # Commented out below code because this data is not available from all leagues. Workaround to be implemented.
                    #ht_score = clear_whitespace_characters(str(cell[i+3].text))
                    #ht_score = ((ht_score.lstrip("(")).rstrip(")")).split("-") # Strip brackets and split into list removing spearator.
                    #home_team_ht_score = ht_score[0]
                    #away_team_ht_score = ht_score[1]
                    
                elif cell2[i].text[:2] in days1 and cell2[i].text[-4:-1] in months and cell2[i].text[2] != " ":# Fixture
                    #print("FIXTURE") # DEBUG CODE
                    date_timea = clear_whitespace_characters(str(cell2[i].text))
                    date_timeb = clear_whitespace_characters(str(cell2[i+1].text))
                    #print("DATE = " + str(date_timea) + "TIME = " + str(date_timeb)) # DEBUG CODE
                    date_time = date_timea + date_timeb
                    #print("1st DATETIME STRING = |" + str(date_time)) # DEBUG CODE
                    date_time = date_time[:2] + " " + date_time[4:] # Convert so that a valid datetime object can be created.
                    #print("2nd DATETIME STRING = |" + str(date_time)) # DEBUG CODE
                    #res mode res = res mode fix [0:2] + " " + res mode fix [4:]
                    #print("DATETIME STRING = " + date_time) # DEBUG CODE
                    teams = str(cell2[i+2].text)[1:].split(" - ")# Strip leading space
                    if len(teams) < 2:
                        teams.append(teams[0])
                        print("Teams error in Results Mode Cell: " + str(i) + " content: " + str(cell2[i])) # Identification for new errors
                        
                    #print("HOME TEAM = " + teams[0] + " AWAY TEAM = " + teams[1]) # DEBUG CODE

                    # Game hasn't yet played
                    #print("NOT PLAYED") # DEBUG CODE
                    played = False
                
                    game_date_time = format_datetime(date_time, mode = "results")
                else: # Cell2[i] is neither a result or fixture start point.
                    continue
                
                # Run this code for played and unplayed games.
                # Separate home and away data.
                home_team = limit_characters(teams[0])
                away_team = limit_characters(teams[1])
            
                # Package results and fixtures.
                
              
                if played:
                    result = [selection, game_date_time.strftime("%d %b %Y"), home_team, home_team_score, away_team, away_team_score, game_date_time]
                    # Omitted home_team_ht_score, away_team_ht_score
                    # Only add the fixture to the fixtures list if it's not already present.
                    if result not in results:
                        with results_lock:
                            results.append(result[:]) # add result details to results
                else:
                    fixture = [selection, game_date_time.strftime("%d %b %Y %H:%M"), home_team, away_team, game_date_time]
                    # Only add the fixture to the fixtures list if it's not already present.
                    if fixture not in fixtures and fixture[4] >= today:
                        with fixtures_lock:
                            fixtures.append(fixture[:]) # add fixture details to fixtures
    # Not all results mode    
    else:  
        #print("Non results mode") # DEBUG CODE
        for i in range(0,(len(cell) - 3)): # Cycle through all but the last 3 cells (as they are accessed through addition)
            # Avoid the major content carrying <td> tags.
            if len(str(cell[i].text)) > 100:
                continue
            #print(str(i) + " - " + str(cell[i])) # DEBUG CODE
            #print("LENGTH OF CELL " + str(i) + " is " + str(len(cell[i])))
            if "Round" in str(cell[i].text):
                round_number = clear_whitespace_characters(str(cell[i].text))
        
            if round_number == "": # Skip to next iteration if no round number has been found.
                continue
            
            # If the first four characters of the cell are a day and last chars are a month.    
            if str(cell[i].text)[:4] in days:
                date_time = clear_whitespace_characters(str(cell[i].text))
                
                teams = str(cell[i+1].text)[1:].split(" - ")# Remove the first character of the first team as non usable character.
                    
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
                    
                    # Commented out below code because this data is not available from all leagues. Workaround to be implemented.
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
                #print("DATE TIME = |" + date_time + "|") # DEBUG CODE
                game_date_time = format_datetime(date_time)
              
                if played:
                    result = [selection, game_date_time.strftime("%d %b %Y"), home_team, home_team_score, away_team, away_team_score, game_date_time]
                    # Omitted home_team_ht_score, away_team_ht_score
                    # Only add the fixture to the fixtures list if it's not already present.
                    if result not in results:
                        with results_lock:
                            results.append(result[:]) # add result details to results
                else:
                    fixture = [selection, game_date_time.strftime("%d %b %Y %H:%M"), home_team, away_team, game_date_time]
                    # Only add the fixture to the fixtures list if it's not already present and it is still to be played.
                    if fixture not in fixtures and fixture[4] >= today:
                        with fixtures_lock:
                            fixtures.append(fixture[:]) # add fixture details to fixtures
                        
    # DEBUG CODE
    #print(fixtures)
    #print(results)
    
    return "Success"