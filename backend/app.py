from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import MySQLdb
import json
from flask_cors import cross_origin
import config
from movie_recommender import movie_recommend_update
from movie_statistics import MovieStatistics
from metadata_similarity.movie_similarity import MovieSimilarity
import datetime
import random

app = Flask(__name__)
mysql = MySQL()

m = MovieStatistics()
sm = MovieSimilarity()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config.user
app.config['MYSQL_PASSWORD'] = config.password
app.config['MYSQL_DB'] = 'database255'
app.config['autocommit'] = True

mysql = MySQL(app)


# Search for movie(s)
@app.route('/movieSearch')
@cross_origin()
def search(search=None):
    search = request.args.get('search')
    print(search)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select id,title,poster_path from movies_metadata where title like \'%{0}%\'".format(search))
    result = cur.fetchall()
    cur.close()
    return json.dumps(result)


# Add/update user's new rating
@app.route('/movieRating', methods=['POST'])
@cross_origin()
def user_rating_upd():
    print('post rating update')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.headers['CONTENT_TYPE'] == 'application/json':
        print('post rating data retrieve')
        movieId = request.json['movieId']
        userId = int(request.json['userId'])
        rating = request.json['rating']
        print('movie id:', movieId, 'user id:', userId, 'rating:', rating)
        current = datetime.datetime.now()
        cur_date_obj = datetime.datetime(current.year, current.month, current.day)
        timestamp = int(datetime.datetime.timestamp(cur_date_obj))
        
        sql = "INSERT INTO ratings (userid, movieid, rating, timestamp) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s, timestamp = %s;"
        try:
            cur.execute(sql, (userId, movieId, rating, timestamp, rating, timestamp,))
            mysql.connection.commit()
            print("successfully executed rating update sql")
        except Exception as e:
            print("Error while executing SQL", e)
        
        movie_recommend_update(userId, m)
        return 'Success'


# Get a list of recommended movies
@app.route('/movieSuggestion')
@cross_origin()
def recommendation(user_id=None):
    user_id = request.args.get('userId')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    rows = []

    try:
        sql = "SELECT movie_list,tag FROM recommend_list where userid = %s" % int(user_id)
        print("Start to get recommend list", user_id)
        mysql.connection.commit()
        cur.execute(sql)
        rows = cur.fetchall()
        print("successfully get recommend list", rows)
    except ValueError as e:
        print("ValueError while executing SQL", e)
    except Exception as e:
        print("Error while executing SQL", e)

    result = {}
    rec_list = ''
    rec_mov_list = []
    user_tags = set()

    if not rows or len(rows) == 0:
        rec_mov_list, user_tags = movie_recommend_update(user_id, m)
    else:
        for tup in rows:
            rec_list = tup['movie_list']
            if tup['tag']:
                user_tags = set(tup['tag'].split(","))
        rec_str = rec_list.split(",")
        for movie in rec_str:
            if movie:
                rec_mov_list.append(int(movie))
    if len(rec_mov_list) <= 0:
        rec_mov_list, user_tags = movie_recommend_update(user_id, m)

    movieid_list_sql = '(' + ','.join(map(str, rec_mov_list)) + ')'
    print('retrieve movie list', movieid_list_sql)
    print('retrieve tag list', user_tags)
    sql = "SELECT id, title, poster_path FROM movies_metadata WHERE id in %s" % movieid_list_sql
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        x = {'id': row['id'], 'title': row['title'], 'poster': row['poster_path'], 'tag': set()}
        result[row['id']] = x

    sql = "SELECT id, genre FROM movie_genre " \
          "WHERE id in %s" % movieid_list_sql
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        if row['id'] in result:
            result[row['id']]['tag'] |= user_tags & set([row['genre']])

    sql = "SELECT movie_id,name FROM movie_cast INNER JOIN cast_info " \
          "WHERE cast_id = id AND movie_id in %s" % movieid_list_sql
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        if row['movie_id'] in result:
            result[row['movie_id']]['tag'] |= user_tags & set([row['name']])

    sql = "SELECT movie_id,name FROM movie_crew INNER JOIN crew_info " \
          "WHERE crew_id = id AND job = 'Director' AND movie_id in %s " % movieid_list_sql
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        if row['movie_id'] in result:
            result[row['movie_id']]['tag'] |= user_tags & set([row['name']])

    result = [val for k, val in result.items()]
    if len(result) > 8:
        result = random.sample(result, 8)
    print("Here is the final recommended result")
    for _movie in result:
        _movie['tag'] = ', '.join(list(_movie['tag']))
        print(_movie['title'], _movie['tag'])

    return json.dumps(result)

# Get user's rating history
@app.route('/moviesRating')
@cross_origin()
def rating_record(user_id=None):
    user_id = request.args.get('userId')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        "select M.id, M.title, M.poster_path, P.rating from ratings as P inner join movies_metadata as M on M.id=P.movieId where userId = {0}"
            .format(user_id))
    result = cur.fetchall()
    cur.close()
    return json.dumps(result)

# Get movie detail information and user interested tag
@app.route('/movie')
@cross_origin()
def movie_detail(movie_id=None, user_id=None):
    movie_id = request.args.get('movieId')
    user_id = request.args.get('userId')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # initialization
    id = ''
    title = ''
    poster = ''
    release_date = ''
    description = ''
    genres_str = ''
    ave_rating = ''
    actors_str = ''
    director_str = ''
    tag = ''
    taste_set = set()
    common_test = set()
    user_rating = -1
    
    mysql.connection.commit()
    # get user tag
    if user_id != 'null':
        sql = "SELECT tag FROM recommend_list WHERE userid = %s"
        cur.execute(sql, (int(user_id),))
        tag_dr = cur.fetchall()
        if tag_dr and tag_dr[0] and tag_dr[0]['tag']:
            taste_set = set(tag_dr[0]['tag'].split(','))
        print("taste_set", taste_set)
        
        # get user rating
        sql = "SELECT rating " \
              "FROM ratings " \
              "WHERE movieid = %s " \
              "AND userid = %s"
        cur.execute(sql, (movie_id, int(user_id),))
        user_rating_dr = cur.fetchone()
        user_rating = None if (user_rating_dr == None) else user_rating_dr['rating']
    
    # get movie meta info
    sql = "SELECT id, title, poster_path, release_date, overview, vote_average " \
          "FROM movies_metadata " \
          "WHERE id = %s"
    cur.execute(sql, (movie_id,))
    row = cur.fetchone()
    if row != None:
        id = row['id']
        title = row['title']
        poster = row['poster_path']
        release_date = row['release_date']
        description = row['overview']
        ave_rating = "%.2f" % row['vote_average']
    
    # get movie genres
    sql = "SELECT genre " \
          "FROM movie_genre " \
          "WHERE id = %s"
    cur.execute(sql, (movie_id,))
    genres_dr = cur.fetchall()
    if genres_dr:
        genres_str = ','.join(map(lambda x: x['genre'], genres_dr))
        common_test |= set(map(lambda x: x['genre'], genres_dr)) & taste_set
        print(taste_set, set(map(lambda x: x['genre'], genres_dr)))
    
    # get actors (cast)
    sql = "SELECT name " \
          "FROM cast_info " \
          "INNER JOIN movie_cast " \
          "ON cast_info.id = movie_cast.cast_id " \
          "WHERE movie_id = %s"
    cur.execute(sql, (int(movie_id),))
    actors_dr = cur.fetchall()
    if actors_dr:
        actors_str = ','.join(map(lambda x: x['name'], actors_dr))
        common_test |= set(map(lambda x: x['name'], actors_dr)) & taste_set
    
    # get director (crew)
    sql = "SELECT name " \
          "FROM crew_info " \
          "INNER JOIN movie_crew " \
          "ON crew_info.id = movie_crew.crew_id " \
          "WHERE movie_id = %s " \
          "AND job = 'director'"
    cur.execute(sql, (int(movie_id),))
    director_dr = cur.fetchall()
    if director_dr:
        director_str = ','.join(map(lambda x: x['name'], director_dr))
        common_test |= set(map(lambda x: x['name'], director_dr)) & taste_set
    
    if common_test:
        print('Movie common taste', common_test)
        tag = ','.join(list(common_test))
    
    data = {
        'id': id,
        'title': title,
        'genre': genres_str,
        'poster': poster,
        'director': director_str,
        'actor': actors_str,
        'avg_rating': ave_rating,
        'released': release_date,
        'description': description,
        'user_rating': user_rating,
        'tag': tag
    }
    
    return json.dumps(data)

# Get movie's similar movies
@app.route('/similarMovie')
@cross_origin()
def similar_movie(movie_id=None):
    try:
        movie_id = request.args.get('movieId')
        print('Looking for similar movie', movie_id)
        if not movie_id:
            return json.dumps([])
        
        movie_id_list = sm.data.loc[int(movie_id)].tolist()
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
        cur.execute("select id,title,poster_path from movies_metadata where id in {0}"
                    .format('(' + ','.join(map(str, movie_id_list)) + ')'))
        result = cur.fetchall()
        cur.close()
        for item in result:
            print(item['title'])
        return json.dumps(result)
    except Exception:
        return []
    

if __name__ == "__main__":
    app.run(debug=True)
