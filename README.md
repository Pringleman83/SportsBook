# SportsBook
A sports data scraping and analysis tool

This project is in its very early days and currently only supports football (soccer).

Fearure list:

* Import leagues and fixtures from one of two available online sources.

* See a visual comparison of the teams playing in any game.

* Run a benchmark comparison on a selected fixture.
  * This allows you to see the results of games where both teams have played the same opponent.
  * It shows results where both teams faced the same opponent at home, then away and then where
  the home team have faced the opponent at home and the away team have faced the opponent away.
  * Only games where three of the above comparisons are shown. If the home team, at home, haven't
  played the same team as the awyay team have played away on three occasions, the game is ommitted
  from predictions.

* Run manual comparison of two teams from any loaded leagues generating (somewhat inaccurate) predictions.

* Run predictions on all loaded fixtures (more accurate as the teams are guaranteed to be from the same leagues).
  * Select from using all available league data to compare home and away goal scoring and conceding form or only using data from games
  where the home team has played the same team at home as the away team as played away, making the data a fairer representation of the
  team's capabilities.

* Filter predictions to show games where specific requirements are met (eg. prediction of home side winning by 2 goals).

* Filter filtered predictions further with other filters.

* Filter predictions using special filters (either produced by guest contributors or specially designed filters for specific bet types).

* Display filtered predictions and all predictions on screen.

* Change the range of dates or games the predictions cover.

* Display results from throughout the whole current season of each league.

* Change the range of dates the results cover.

* Produce a spreadsheet of all predictions or filtered predictions with a wealth of current stats for each team in each prediction.

* Export currently loaded league data to a JSON file.

* Import the league data from a JSON file.

The project is growing fairly quickly. I'd love to hear what your thoughts are and even keep you up to date with new features if you like. Join the Slack group here if you're interested:

https://join.slack.com/t/sportsbookgroup/shared_invite/enQtNDc4MjYwNzMwNzg4LTAzMDk0MDM3OWFiMGJhZWU2MzAyMzQyNGI4OTlhNjgxMWRlNTZjOTAzMTM3ODdhMDIxNDU3YjI2MzM4OTlmZjg

It'd be great to hear from you so please pop in and say hi!
