import feedparser
import pymongo
import datetime
import time


DB_NAME = 'supmeme2'

FEED_LIST = [
  ('Webprendedor', 'http://webprendedor.com/feed/'),
  ('Andes Beat', 'http://andesbeat.com/feed/'),
  ('Diario Emprendimiento', 'http://www.diarioemprendimiento.cl/feed'),
  ('Star-Up Chile', 'http://startupchile.org/feed/')
]


_connection = []
def get_connection():
  if not _connection:
    _connection.append(pymongo.MongoClient()[DB_NAME])
  return _connection[0]


def parse_feed(feed):
  name, feed_url = feed
  d = feedparser.parse(feed_url)
  entries = d['entries']
  for entry in entries:
    if should_index(entry.link):
      index(entry, name)


def should_index(link):
  c = get_connection()
  return not c.entries.find_one({'link': link})
  

def index(entry, name):
  mongo_entry = {
    'link': entry.link,
    'title': entry.title,
    'published_at': datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)),
    'description': entry.description,
    'source': name
  }
  print '+ %s' % entry.link
  c = get_connection()
  c.entries.insert(mongo_entry)


if __name__ == '__main__':
  for feed in FEED_LIST:
    parse_feed(feed)
