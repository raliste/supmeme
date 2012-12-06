from flask import Flask, render_template

import pymongo


DB_NAME = 'supmeme2'
_connection = []
def get_connection():
  if not _connection:
    _connection.append(pymongo.MongoClient()[DB_NAME])
  return _connection[0]


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  c = get_connection()
  return render_template('index.html', entries=c.entries.find())
