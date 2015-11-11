#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import contextlib


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    """
    return psycopg2.connect("dbname=tournament")

@contextlib.contextmanager
def getCursor():
    """
    Generator function that connects to the PostgreSQL database and yields a cursor.
    The cursor and database connection are closed after this generator is consumed.
    """
    connection = connect()
    cursor = connection.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def deleteMatches():
    """
    Remove all the match records from the database.
    """
    with getCursor() as cursor:
        cursor.execute("DELETE FROM MatchPlayers;")
        cursor.execute("DELETE FROM Matches;")

def deletePlayers():
    """
    Remove all the player records from the database.
    """
    with getCursor() as cursor:
        cursor.execute("DELETE FROM Players;")

def countPlayers():
    """
    Returns the number of players currently registered.
    """
    with getCursor() as cursor:
        cursor.execute("SELECT count(*) FROM Players;")
        result = cursor.fetchone()
        return result[0] 

def registerPlayer(name):
    """
    Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with getCursor() as cursor:
        cursor.execute("INSERT INTO Players (name) VALUES(%s)", (name,))

def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with getCursor() as cursor:
        cursor.execute("SELECT player.id, player.name, count(matches_won.id) as wins, count(matches_played.id) as matches\
                        FROM Players as player\
                        LEFT JOIN MatchPlayers\
                        ON player.id = MatchPlayers.player\
                        LEFT JOIN Matches AS matches_played\
                        ON matches_played.id = MatchPlayers.match\
                        LEFT JOIN Matches AS matches_won\
                        ON matches_won.id = MatchPlayers.match\
                        AND matches_won.winner = player.id\
                        GROUP BY player.id, player.name\
                        ORDER BY wins DESC;")
        result = cursor.fetchall()
        return result

def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with getCursor() as cursor:
        cursor.execute(" INSERT INTO Matches (winner)\
                         VALUES(%s)", (winner,))
        cursor.execute(" INSERT INTO MatchPlayers (player, match)\
                         VALUES(%s, lastval()), (%s, lastval());", (winner, loser,))
 
def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    with getCursor() as cursor:
        #First, retrieve the list of all players by ID and name, in order of number of wins
        #We retrieve the number of wins by joining to the Matches table
        cursor.execute(" SELECT player.id, player.name, count(match.id) as wins\
                         FROM Players as player\
                         LEFT JOIN Matches as match\
                         ON player.id = match.winner\
                         GROUP BY player.id, player.name\
                         ORDER BY wins DESC;")
        result = cursor.fetchall()

        #Next, pair players 0 & 1, 2 & 3, 4 & 5 etc, since the players are already ordered by wins
        #This is done by iterating over the player list 2 at a time
        pairings = []
        for index in xrange(0, len(result), 2):
            pairings.append((result[index][0], result[index][1], result[index+1][0], result[index+1][1]))
        return pairings