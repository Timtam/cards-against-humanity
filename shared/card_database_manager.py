import hashlib
import os
import os.path
import sqlite3

from .card import *
from .path import getScriptDirectory

MAX_PLAYERS_PER_GAME = 10

class CardDatabaseManager(object):

  cards = []
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

  def loadCards(self):

    if not self.loaded:
      return

    self.cards = []

    cursor = self.database.cursor()
    cursor.execute('SELECT id, text, type FROM cards')

    for card in cursor.fetchall():
      self.cards.append(Card(card[0], card[1], card[2]))

  def getBlackCards(self):
    return [c for c in self.cards if c.type == CARD_BLACK]

  def getWhiteCards(self):
    return [c for c in self.cards if c.type == CARD_WHITE]

  def getCard(self, id):
    card = [c for c in self.cards if c.id == id]
    if len(card) != 1:
      return None
    return card[0]

  @property
  def max_players_per_game(self):
    return min(MAX_PLAYERS_PER_GAME, len(self.getWhiteCards())/10, len(self.getBlackCards()))
