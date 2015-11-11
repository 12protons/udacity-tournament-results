#Full Stack Web Developer Project 2: Tournament Results


###Files
- `tournament.sql`: Defines all tables used by the tournament database
- `tournament.py`: Defines various methods that use the tournament database, using psycopg2
- `tournament_test.py`: Unit tests to verify tournament.py

###Instructions

####Install VirtualBox
Download and install VirtualBox [here](https://www.virtualbox.org/wiki/Downloads).

####Clone fullstack Git repository
git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack

####Copy the tournament project files into the fullstack directory
Copy the `tournament.sql` and `tournament.py` files from this project into the fullstack/vagrant/tournament directory in the cloned repository. Note that `tournament_test.py` is unchanged.

####Start and connect to the Vagrant VM
From a terminal, go to the fullstack/vagrant directory in the cloned repository and type `vagrant up`. To connect to the newly started Vagrant VM, type `vagrant ssh`.

####Setup the tournament database
From the terminal connected to the Vagrant VM above, go to the /vagrant/tournament directory and type the following commands to connect to the Postgres database and initialize the database using tournament_test.sql.

    psql
    \i tournemant_test.sql
    \q

####Execute the tournament tests
From the terminal connected to the Vagrant VM above, again in the /vagrant/tournament directory, type `python tournament_test.py` to execute the tests and verify the output.

###Design Notes
The `Matches` and `MatchPlayers` tables allow a match to contain 1 or more players with no null values.
A match with only 1 corresponding row in the `MatchPlayers` table would represent a bye, and a match with 5 corresponding rows in the `MatchPlayers` table would represent a game with 5 players.

The `Matches` table defines a winner of the match, along with the match id. If multiple players are allowed to win a match, a `MatchWinners` table should be created, which has the same table definition as `MatchPlayers` but contains only the winners of each match.