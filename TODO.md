For ease and quick communication I've set up a "Slack" workspace for contributors.
The invite link is: https://join.slack.com/t/sportsbookgroup/shared_invite/enQtNDQ5MDMyMTIwNzA2LWRhY2YxOGY0NWYzNTE2ZDMyNGI3NWQzMTk0YTkxODMyNzEyM2UyMjlkMTVlYmU3NDMzNTVlNWVmZDM4YTNjMjE

Please be sure that your forks are up to date before continuing development as it causes problems when merging new code that has some older features than the existing code.
If there's something I can do to make this easier, let me know.

To Do:

This is a list of what I'd like to do next. However, if any contributors have other ideas please feel free to share them and discuss.

(1)

DONE

Tidy the league select and team select screen so that 3 or 4 leagues / teams appear on each line.
For example:

1) English Premier   2) English Championship    3) English League 1 (Done)

DONE

(2)
Design a fixture list scraper.
This is a relatively big task. I'm hoping to get started on this Monday 8 October and have it working by Saturday 13.
Once complete:
  (2b)
  Develop an automated prediction process so that the user can run predictions for all upcoming fixtures in all selected leagues. (Done)
  (2c)
  Develop an option for the user to view upcoming fixtures and select from them which games to predict.
  
(3)
Develop some alternative prediction algorithms (even if they are just placeholders for now).
One example would be to have a prediction based on goals conceded only.
  (3b)
  Develop an option to choose the type of prediction to use, including the option to run all prediction types.
  (3c)
  Upgrade the predictions list object so that, for each game, all stats are stored along with the prediction.
  (3d)
  Develop an option to export the predictions list object to a spreadsheet.
  Future plan with this is to develop an option to read this spreadsheet, insert results and check how accurate the predictions       were. However, results would also need to be scraped and a method of considering fixture dates would need to be developed.
