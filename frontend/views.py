from datetime import datetime
import pymongo

from flask import Flask, render_template


app = Flask(__name__)

DB_NAME = 'supmeme2'


_connection = []
def get_connection():
  if not _connection:
    _connection.append(pymongo.MongoClient()[DB_NAME])
  return _connection[0]


@app.template_filter()
def timesince(dt, default="just now"):
  """
  Returns string representing "time since" e.g.
  3 days ago, 5 hours ago etc.
  http://flask.pocoo.org/snippets/33/
  """

  now = datetime.utcnow()
  diff = now - dt

  periods = (
    (diff.days / 365, "year", "years"),
    (diff.days / 30, "month", "months"),
    (diff.days / 7, "week", "weeks"),
    (diff.days, "day", "days"),
    (diff.seconds / 3600, "hour", "hours"),
    (diff.seconds / 60, "minute", "minutes"),
    (diff.seconds, "second", "seconds"),
  )

  for period, singular, plural in periods:
    if period:
      return "%d %s ago" % (period, singular if period == 1 else plural)

  return default


@app.route('/')
def index():
  c = get_connection()
  now = datetime.now()

  def compute_score(entry, points=1, gravity=1.8):
    delta = now - entry['published_at']
    hours_since = delta.days * 24 + delta.seconds / 3600.0
    return points / ((hours_since + 2) ** gravity)

  entries = [(compute_score(entry), entry) for entry in c.entries.find()]
  sorted_entries = sorted(entries, key=lambda s: s[0], reverse=True)
  return render_template('index.html', entries=sorted_entries)
