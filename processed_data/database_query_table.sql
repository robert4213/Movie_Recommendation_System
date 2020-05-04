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
	id int NOT NULL,
	imdb_id varchar(255),
	overview text,
	popularity float,
	poster_path varchar(255),
	release_date varchar(255),
	tagline text,
	title varchar(255),
	vote_average DECIMAL(20, 10),
	vote_count int,
	collection int
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






