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
		.format(search),)
	result = cur.fetchall()
	print(json.dumps(result,indent=2))
	return json.dumps(result)


@app.route('/moviesRating')
def search2(search2=None):
	userId = request.args.get('userId')
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("select M.id,M.title,M.poster_path, R.rating from rating_processed as R left join movies_metadata_processed as M on R.movieId = M.id "
		.format(search),)
	result = cur.fetchall()
	print(json.dumps(result,indent=2))
	return json.dumps(result)

@app.route('/movie')
def search3(search3=None):
	movieId = request.args.get('movieId') && userId = request.args.get('userId')
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("select M.id, M.title, G.genre, M.poster_path, P.rating from rating_processed as P left join movies_metadata_processed as M left join movies_genre as G on R.movieId = M.id on M.id=G.id "
		.format(search),)
	result = cur.fetchall()
	print(json.dumps(result,indent=2))
	return json.dumps(result)



if __name__ == "__main__":
	app.run()