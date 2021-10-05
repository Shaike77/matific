Web developer home assignment

You were hired by a basketball league to develop
 a management system to monitor games statistics and rankings of a recent tournament.
A total of 16 teams played in the first qualifying round,
 8 moved to the next round, and so forth until one team was crowned as champion.
Each team consists of a coach and 10 players.
 not all players participate in every game.



There are 2 types of users in the system - a coach, and a player.
Users can view the scoreboard, which will display all games and final scores,
 and will reflect how the competition progressed and who won.	
A coach may select his team in order to view a list of the players on it.
 When one of the players in the list is selected,
 his personal details will be presented,
 including - player’s name, height, average score, 
 and the number of games he participated in. 


Notes:

The project should be developed using Django/Flask and Angular/React/Vue 
The server should expose a set of APIs which will be used by the different frontend components and services to display the data
All queries to the Database should be implemented using an ORM library
We expect you to create all supporting models, business logic and views. 
Please create a management command to generate fake users with all needed relations, and activities OR create a fixture to generate fake data.



.../api/games/
.../api/coach/<team>/
