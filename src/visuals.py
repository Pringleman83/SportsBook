import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

def visual_comparison(fixture, league_data):
    """
    Takes a fixture and the league_data dict.
    Provides a visual comparison of the teams in the fixture.
    fixture format:
    [0-League, 1-date+time, 2-home team, 3-away team, 4-datetime object]
    """
    # Compare (WPG, DPG, LPG, FPG, APG, PtsPG)
    
    # Data prep
    # Wins per game
    home_team_home_wpg = league_data[fixture[0]][fixture[2]]["Home"]["Won per Game"]
    away_team_away_wpg = league_data[fixture[0]][fixture[3]]["Away"]["Won per Game"]
    home_team_total_wpg = league_data[fixture[0]][fixture[2]]["Total"]["Won per Game"]
    away_team_total_wpg = league_data[fixture[0]][fixture[3]]["Total"]["Won per Game"]
    
    # Draws per game
    home_team_home_dpg = league_data[fixture[0]][fixture[2]]["Home"]["Drew per Game"]
    away_team_away_dpg = league_data[fixture[0]][fixture[3]]["Away"]["Drew per Game"]
    home_team_total_dpg = league_data[fixture[0]][fixture[2]]["Total"]["Drew per Game"]
    away_team_total_dpg = league_data[fixture[0]][fixture[3]]["Total"]["Drew per Game"]
    
    # Losses per game
    home_team_home_lpg = league_data[fixture[0]][fixture[2]]["Home"]["Lost per Game"]
    away_team_away_lpg = league_data[fixture[0]][fixture[3]]["Away"]["Lost per Game"]
    home_team_total_lpg = league_data[fixture[0]][fixture[2]]["Total"]["Lost per Game"]
    away_team_total_lpg = league_data[fixture[0]][fixture[3]]["Total"]["Lost per Game"]
    
    # Pts per game
    home_team_home_ptpg = league_data[fixture[0]][fixture[2]]["Home"]["Points per Game"]
    away_team_away_ptpg = league_data[fixture[0]][fixture[3]]["Away"]["Points per Game"]
    home_team_total_ptpg = league_data[fixture[0]][fixture[2]]["Total"]["Points per Game"]
    away_team_total_ptpg = league_data[fixture[0]][fixture[3]]["Total"]["Points per Game"]
    
    home_team_home_gfpg = league_data[fixture[0]][fixture[2]]["Home"]["For per Game"]
    away_team_away_gfpg = league_data[fixture[0]][fixture[3]]["Away"]["For per Game"]
    home_team_total_gfpg = league_data[fixture[0]][fixture[2]]["Total"]["For per Game"]
    away_team_total_gfpg = league_data[fixture[0]][fixture[3]]["Total"]["For per Game"]
    
    home_team_home_gapg = league_data[fixture[0]][fixture[2]]["Home"]["Against per Game"]
    away_team_away_gapg = league_data[fixture[0]][fixture[3]]["Away"]["Against per Game"]
    home_team_total_gapg = league_data[fixture[0]][fixture[2]]["Total"]["Against per Game"]
    away_team_total_gapg = league_data[fixture[0]][fixture[3]]["Total"]["Against per Game"]
    
    # Bar chart prep
    home_team_home = [home_team_home_wpg, home_team_home_dpg, home_team_home_lpg, home_team_home_gfpg,home_team_home_gapg, home_team_home_ptpg]
    
    home_team_total = [home_team_total_wpg, home_team_total_dpg, home_team_total_lpg, home_team_total_gfpg, home_team_total_gapg, home_team_total_ptpg]
    
    away_team_away = [away_team_away_wpg, away_team_away_dpg, away_team_away_lpg, away_team_away_gfpg,away_team_away_gapg, away_team_away_ptpg]
    
    away_team_total = [away_team_total_wpg, away_team_total_dpg, away_team_total_lpg, away_team_total_gfpg, away_team_total_gapg, away_team_total_ptpg ]
    x = numpy.arange(len(home_team_home))
    
    # plot data
    bar_width = 0.22
    plt.bar(x, home_team_home, width = bar_width, color = "#dd0202", zorder = 2)
    plt.bar(x + bar_width, home_team_total, width = bar_width, color = "#f90202", zorder = 2)
    plt.bar(x + bar_width * 2, away_team_total, width = bar_width, color = "#2001d6", zorder = 2)
    plt.bar(x + bar_width * 3, away_team_away, width = bar_width, color = "#170191", zorder = 2)

    # labels
    plt.xticks(x + 0.22, ["Wins\nper\nGame", "Draws\nper\nGame", "Losses\nper\nGame", "Goals (F)\nper\nGame", "Goals (A)\nper\nGame", "Points\nper\nGame"])
    plt.title(fixture[1] + ": " + fixture[2] + " - " + fixture[3])

    # legend
    home_home_patch = mpatches.Patch(color = "#dd0202", label = fixture[2] + " home games")
    home_total_patch = mpatches.Patch(color = "#f90202", label = fixture[2] + " all games")
    away_total_patch = mpatches.Patch(color = "#2001d6", label = fixture[3] + " all games")
    away_away_patch = mpatches.Patch(color = "#170191", label = fixture[3] + " away games")
    plt.legend(handles = [home_home_patch, home_total_patch, away_total_patch, away_away_patch])

    # grid
    plt.grid(axis = "y")

    plt.show()
    
    return 0