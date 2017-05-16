import hashlib
import os
import os.path
import sqlite3

from .path import getScriptDirectory

class CardDatabaseManager(object):

  data = None
  database = None
  hash = ''
  loaded = False
  size = 0

  def __init__(self):
    pass

  # if hash is None, the path will be loaded without any suffix
  # if a hash is given, the manager will try to load a database
  # with the related hash suffix
  def loadPath(self, path, hash = None):

    path = self.makePath(path, hash)

    if not os.path.exists(path):
      return

    self.data = open(path, 'rb').read()

    self.size = len(self.data)

    if hash is not None:
      self.hash = hash
    else:
      self.hash = hashlib.sha512(self.data).hexdigest()

    self.database = sqlite3.connect(path)

    self.loaded = True

  def loadData(self, data, host, hash):

    path = self.makePath(host, hash)

    db = open(path, 'wb')
    db.write(data)

    self.data = data
    self.hash = hash
    self.size = len(data)

    self.database = sqlite3.connect(path)

    self.loaded = True

  def makePath(self, path, hash=None):

    # making it absolute
    if not os.path.isabs(path):
      # if version >0 is given, we will add the database directory here
      if hash is not None:
        if not os.path.exists(os.path.join(getScriptDirectory(), 'database')):
          os.mkdir(os.path.join(getScriptDirectory(), 'database'))
        path = os.path.join('database', path)
      path = os.path.join(getScriptDirectory(), path)

    if hash is not None:
      path = path+".%s"%hash

    return path
