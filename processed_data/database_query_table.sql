CREATE database IF NOT EXISTS  database255 ;

SET default_storage_engine = InnoDB;

SET GLOBAL local_infile = 1;

use database255;

DROP TABLE IF EXISTS cast_info;
CREATE TABLE cast_info (
id INT NOT NULL PRIMARY KEY,
name VARCHAR(100)
);

DROP TABLE IF EXISTS crew_info;
CREATE TABLE crew_info (
id INT NOT NULL PRIMARY KEY,
name VARCHAR(100)
);

DROP TABLE IF EXISTS movie_cast;
CREATE TABLE movie_cast (
cast_id INT,
movie_id INT,
PRIMARY KEY (cast_id, movie_id)
);

DROP TABLE IF EXISTS movie_crew;
CREATE TABLE movie_crew (
crew_id INT,
movie_id INT,
job VARCHAR(100),
PRIMARY KEY (crew_id, movie_id, job)
);

DROP TABLE IF EXISTS movie_genre;
CREATE TABLE movie_genre (
id INT,
genre VARCHAR(100),
PRIMARY KEY (id, genre)
);

DROP TABLE IF EXISTS movies_metadata;
CREATE TABLE movies_metadata (
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
  collection int,
  PRIMARY KEY (id)
); 

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  userid int,
  movieid int,
  rating varchar(255),
  timestamp varchar(255),
  PRIMARY KEY (userid, movieid)
); 


-- load data 
LOAD DATA local INFILE  'E:/CMPE255/Movie_Recommendation_System/processed_data/cast_info.csv' INTO TABLE cast_info
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/crew_info.csv' INTO TABLE crew_info
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/movie_cast.csv' INTO TABLE movie_cast
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/movie_crew.csv' INTO TABLE movie_crew
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/movie_genre.csv' INTO TABLE movie_genre
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/movies_metadata.csv' INTO TABLE movies_metadata_processed
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;

LOAD DATA local INFILE 'E:/CMPE255/Movie_Recommendation_System/processed_data/rating_processed.csv' INTO TABLE ratings
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;





