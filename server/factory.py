import os.path
from twisted.internet.protocol import Factory
from twisted.logger import Logger
import sqlite3

from .game import Game
from .protocol import ServerProtocol
from . import version
from shared.card_database_manager import CardDatabaseManager
from shared.path import getScriptDirectory

class ServerFactory(Factory):
  card_database = None
  games = []
  log = Logger()
  serverDatabase = None
  users=[]

  def buildProtocol(self, addr):
    return ServerProtocol(self)

  def openServerDatabase(self):
    self.serverDatabase = sqlite3.connect(os.path.join(getScriptDirectory(), "server.db"))
    cursor = self.serverDatabase.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY, 'name' VARCHAR(30), 'password' CHAR(128))")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'games' ('id' CHAR(32), 'name' VARCHAR(30), 'users' TEXT, 'cards' TEXT, 'password_hash' CHAR(128), 'database_hash' CHAR(128), 'server_version_major' TINYINT, 'server_version_minor' TINYINT, 'server_version_revision' TINYINT)")
    self.serverDatabase.commit()
    self.log.info("Loaded server database")

  def loadGames(self):
    cursor = self.serverDatabase.cursor()
    cursor.execute('SELECT * FROM games where database_hash = ? and server_version_major = ? and server_version_minor = ?', (self.card_database.hash, version.MAJOR, version.MINOR, ))
    
    game_rows = cursor.fetchall()

    for row in game_rows:
      game = {}
      for colid in range(len(row)):
        game[cursor.description[colid][0]] = row[colid]
      game = Game.load(self, **game)
      self.games.append(game)

    cursor.execute('DELETE FROM games')
    cursor.execute('VACUUM')
    self.serverDatabase.commit()
    self.log.info('loaded {count} games from database', count = len(self.games))

  def startFactory(self):
    self.card_database = CardDatabaseManager()
    self.card_database.loadPath('cards.db')
    self.card_database.loadCards()
    self.log.info("Loaded card database")

    self.openServerDatabase()
    self.loadGames()

    # after doing all the startup stuff
    self.log.info("Server up and running, waiting for incoming connections")

  def stopFactory(self):
    self.log.info('saving games...')
    cursor = self.serverDatabase.cursor()
    c = 0
    for game in self.games:
      if not game.open:
        data = game.pack()
        cursor.execute('INSERT INTO games ('+','.join(data.keys())+') VALUES ('+('?,'*len(data.keys()))[:-1]+')', tuple(data.values()))
        c += 1
    if c > 0:
      self.serverDatabase.commit()
    self.log.info('saved {count} games into database', count = c)

  def createGame(self, name, password = None):
    game = Game.create(self, name = name, password_hash = password)
    self.games.append(game)
    return game

  def unlinkGame(self, game):
    del self.games[self.games.index(game)]

  def findGame(self, id):
    possible_games = [g for g in self.games if g.id == id]
    if len(possible_games) != 1:
      return None
    return possible_games[0]

  def findUser(self, id):
    possible_users = [u for u in self.users if u.id == id]

    if len(possible_users)!=1:
      return None

    return possible_users[0]

  def getAllUsers(self):
    return self.users

  def getAllGames(self):
    return self.games

  def gameExists(self, name):
    for game in self.games:
      if game.name == name:
        return True
    return False

