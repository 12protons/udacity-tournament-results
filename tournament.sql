-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

-- Players Table
-- Each row stores a player name and a unique ID
CREATE TABLE Players (
   id SERIAL  PRIMARY KEY,
 name varchar NOT NULL
);

-- Matches Table
-- Each row stores a match id and the ID of the winning player
-- For a bye game, a row will contain the ID of the player in the bye
CREATE TABLE Matches (
    id SERIAL  PRIMARY KEY,
winner integer REFERENCES Players(id)
);

-- MatchPlayers Table
-- Each row stores a specific player that played in a specific match
-- For a match containing two players, there will be two rows in this
-- table with that match id.
-- For a bye, there will be one row in this table with the match id
-- of the bye and the player that got the bye.
-- A player cannot be in the same match more than once.
CREATE TABLE MatchPlayers (
player integer REFERENCES Players(id),
 match integer REFERENCES Matches(id),
UNIQUE (player, match)
);

