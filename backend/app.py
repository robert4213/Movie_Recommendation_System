from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import MySQLdb
import json


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'springuser'
app.config['MYSQL_PASSWORD'] = 'ThePassword'
app.config['MYSQL_DB'] = 'database255'

mysql = MySQL(app)

@app.route('/movieSearch')
def search(search=None):
	search = request.args.get('search')
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("select id,title,poster_path from movies_metadata_processed where title like \'%{0}%\'"
		.format(search))
	result = cur.fetchall()
	print(json.dumps(result,indent=2))
	return json.dumps(result)

# @app.route('/movieSuggestion')
# def Recommendation(userId=None):
# 	userId = request.args.get('userId') 
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute("select R.userId, M.title, M.poster_path from rating_processed as P left join movies_metadata_processed as M on P.movieId=M.id where P.userId like \'%{0}%\'"
# 		.format(userId))
# 	result = cur.fetchall()
# 	print(json.dumps(result,indent=2))
# 	return json.dumps(result)

# @app.route('/moviesRating')
# def RatingRecord(movieId=None):
# 	userId=request.args.get('userId') 
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute("select M.Id, M.title, M.poster, P.rating from rating_processed as P left join movies_metadata_processed as M on M.id=P.movieId where userId like \'%{0}%\'"
# 		.format(userId))
# 	result = cur.fetchall()
# 	print(json.dumps(result,indent=2))
# 	return json.dumps(result)

# @app.route('/moviesRating', request.method == 'POST')
# def UpdateRatingRecord():
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute("""INSERT INTO movie_recommender (movieId, userId, rating) VALUES ('$movieId', '$userId', '$rating') """
# 		.format(userId))
# 	result = cur.fetchall()
	
# 	return json.dumps(result)



# @app.route('/movie')
# def MovieDetail(movieId=None,userId=None):
# 	movieId = request.args.get('movieId') & userId = request.args.get('userId')
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute("select M.id, M.title, G.genre, M.poster_path, C.name, I.name, M.vote_average, M.release_date,M.overview, P.rating from rating_processed as P left join movies_metadata_processed as M on P.movieId = M.idleft join movies_genre as G on M.id=G.id left join cast_info as I on I.id=G.id left join crew_info as C on C.id=I.id  userId like \'%{0}%\' and movieId like \'%{0}%\ "
# 		.format(search))
# 	result = cur.fetchall()
# 	print(json.dumps(result,indent=2))
# 	return json.dumps(result)



if __name__ == "__main__":
	app.run()




