import os.path
from twisted.internet.protocol import Factory
from twisted.logger import Logger
import sqlite3

from .game import Game
from .protocol import ServerProtocol
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
    cursor.execute("CREATE TABLE IF NOT EXISTS 'games' ('id' BIGINT NOT NULL, 'name' VARCHAR(30), 'players' TEXT, 'cards' TEXT, 'password_hash' CHAR(128), 'database_hash' CHAR(128), 'server_version_major' TINYINT, 'server_version_minor' TINYINT, 'server_version_revision' TINYINT)")
    self.serverDatabase.commit()
    self.log.info("Loaded server database")

  def startFactory(self):
    self.card_database = CardDatabaseManager()
    self.card_database.loadPath('cards.db')
    self.card_database.loadCards()
    self.log.info("Loaded card database")

    self.openServerDatabase()

    # after doing all the startup stuff
    self.log.info("Server up and running, waiting for incoming connections")

  def createGame(self, name, password = None):
    game = Game(self, name = name, password_hash = password)
    self.games.append(game)
    return game

  def findGame(self, id):
    possible_games = [g for g in self.games if g.id == id]
    if len(possible_games) != 1:
      return None
    return possible_games[0]
