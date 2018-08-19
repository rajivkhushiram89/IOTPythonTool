from flask import Flask, g, render_template, request
import sqlite3
import os
app = Flask(__name__)

DATABASE = "./sensehat.db"

if not os.path.exists(DATABASE):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS sensedata (datetime TEXT, temperature REAL, humidity REAL)""")
	conn.commit()
	cur.execute("INSERT INTO sensedata VALUES('11/12/18', '23', '33');")
	conn.commit()
	conn.close()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/')
def home():
	cur = get_db().cursor()
	res = cur.execute("select * from sensedata")
	return render_template('index.html', data = res)

if __name__ == '__main__':
	app.run(debug = True)
