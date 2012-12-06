from flask import Flask, render_template

import pymongo
import datetime


DB_NAME = 'supmeme2'


_connection = []
def get_connection():
  if not _connection:
    _connection.append(pymongo.MongoClient()[DB_NAME])
  return _connection[0]


app = Flask(__name__)

@app.route('/')
def index():
  c = get_connection()
  now = datetime.datetime.now()

  def compute_score(entry, points=1, gravity=1.8):
    delta = now - entry['published_at']
    hours_since = delta.days * 24 + delta.seconds / 3600.0
    return points / ((hours_since + 2) ** gravity)

  entries = [(compute_score(entry), entry) for entry in c.entries.find()]
  sorted_entries = sorted(entries, key=lambda s: s[0], reverse=True)
  return render_template('index.html', entries=sorted_entries)
