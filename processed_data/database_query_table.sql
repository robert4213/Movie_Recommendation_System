CREATE DATABASE 255database ;

use 255database;

CREATE TABLE cast_info (
id INT NOT NULL PRIMARY KEY,
name VARCHAR(100)
);


CREATE TABLE crew_info (
id INT NOT NULL PRIMARY KEY,
name VARCHAR(100)
);

CREATE TABLE movie_cast (
cast_id INT NOT NULL PRIMARY KEY,
movie_id INT
);
CREATE TABLE movie_crew (
crew_id INT NOT NULL PRIMARY KEY,
movie_id INT,
job VARCHAR(100)
);
CREATE TABLE movies_genre (
id INT NOT NULL PRIMARY KEY,
genre VARCHAR(100)
);
CREATE TABLE movies_metadata_processed(
id INT NOT NULL PRIMARY KEY,
imdb_id INT,
overview VARCHAR(100),
popularity VARCHAR(100),
poster_path VARCHAR(100),
release_data VARCHAR(100),
tagline VARCHAR(100),
title VARCHAR(100),
vote_average VARCHAR(100),
vote_count VARCHAR(100),
collection VARCHAR(100)
);

LOAD DATA INFILE '/Users/yifanliu/cast_info.csv' INTO TABLE cast_info
  FIELDS TERMINATED BY ',' ;
LOAD DATA INFILE '‎⁨/Desktop⁩/cast_info.csv' INTO TABLE crew_info
  FIELDS TERMINATED BY ',' ;
LOAD DATA INFILE '‎⁨/Desktop⁩/cast_info.csv' INTO TABLE movie_cast
  FIELDS TERMINATED BY ',' ;
LOAD DATA INFILE '‎⁨/Desktop⁩/cast_info.csv' INTO TABLE movie_crew
  FIELDS TERMINATED BY ',' ;
LOAD DATA INFILE '‎⁨/Desktop⁩/cast_info.csv' INTO TABLE movies_genre
  FIELDS TERMINATED BY ',' ;
LOAD DATA INFILE '‎⁨/Desktop⁩/cast_info.csv' INTO TABLE movies_metadata_processed
  FIELDS TERMINATED BY ',' ;






