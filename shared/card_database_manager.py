import os
import os.path
import sqlite3

from .path import getScriptDirectory

class CardDatabaseManager(object):

  database = None
  loaded = False
  version = 0

  # if version is 0, the path will be loaded without any suffix
  # if a version >0 is given, the manager will try to load a database
  # with the related version suffix
  def __init__(self, path, version = 0):

    # making it absolute
    if not os.path.isabs(path):
      # if version >0 is given, we will add the database directory here
      if version > 0:
        if not os.path.exists(os.path.join(getScriptDirectory(), 'database')):
          os.mkdir(os.path.join(getScriptDirectory(), 'database'))
        path = os.path.join('database', path)
      path = os.path.join(getScriptDirectory(), path)

    if version > 0:
      path = path+".%d"%version

    if not os.path.exists(path):
      return

    self.database = sqlite3.connect(path)

    cursor = self.database.cursor()

    cursor.execute('SELECT value FROM config WHERE key = ?', ('version', ))

    self.version = int(cursor.fetchone()[0])

    self.loaded = True
