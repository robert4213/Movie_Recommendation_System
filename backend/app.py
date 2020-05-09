from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import MySQLdb
import json
from flask_cors import cross_origin


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'springuser'
app.config['MYSQL_PASSWORD'] = 'ThePassword'
app.config['MYSQL_DB'] = 'database255'

mysql = MySQL(app)

@app.route('/movieSearch')
@cross_origin()
def search(search=None):
	search = request.args.get('search')
	print(search)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("select id,title,poster_path from movies_metadata where title like \'%{0}%\'"
		.format(search))
	result = cur.fetchall()
	print('result: ',json.dumps(result,indent=2))
	return json.dumps(result)

# @app.route('/movieSuggestion')
# @cross_origin()
# def Recommendation(userId=None):
# 	userId = request.args.get('userId') 
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute("select R.userId, M.title, M.poster_path from ratings as P left join movies_metadata as M on P.movieId=M.id where userId={0}"
# 		.format(userId))
# 	result = cur.fetchall()
# 	print(json.dumps(result,indent=2))
# 	return json.dumps(result)

@app.route('/moviesRating')
@cross_origin()
def RatingRecord(userId=None):
	userId=request.args.get('userId') 
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("select M.id, M.title, M.poster_path, P.rating from ratings as P inner join movies_metadata as M on M.id=P.movieId where userId = {0}"
		.format(userId))
	result = cur.fetchall()
	print(json.dumps(result,indent=2))
	return json.dumps(result)



@app.route('/movie')
@cross_origin()
def MovieDetail(movieId=None,userId=None):
	userId = request.args.get('userId')
	movieId = request.args.get('movieId') 
	
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("Select M.id, M.title, G.genre, M.poster_path, C.name, Cr.name, M.vote_average, M.release_date, M.overview, R.rating from movies_metadata as M left join movie_genre as G on G.id=M.id left join cast_info as C on C.id=G.id left join crew_info as Cr on Cr.id=C.id left join ratings as R on R.movieId=CR.id where userId={0} and movieId={1} "
		.format(movieId,userId))
	result = cur.fetchall()
	print(json.dumps(result[0],indent=2))
	return json.dumps(result)



if __name__ == "__main__":
	app.run()




