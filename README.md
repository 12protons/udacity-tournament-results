#Full Stack Web Developer Project 2: Tournament Results


###Files
- tournament.sql: Defines all tables used by the tournament database
- tournament.py: Defines various methods that use the tournament database, using psycopg2
- tournament_test.py: Unit tests to verify tournament.py

###Instructions
Run the tournament_test.py file to display test results.

###Design Notes
The Matches and MatchPlayers tables allow a match to contain 1 or more players with no null values.
A match with only 1 corresponding row in the MatchPlayers table would represent a bye, and a match
with 5 corresponding rows in the MatchPlayers table would represent a game with 5 players.

The Matches table defines a winner of the match, along with the match id. If multiple players are
allowed to win a match, a MatchWinners table should be created, which has the same table definition
as MatchPlayers but contains only the winners of each match.