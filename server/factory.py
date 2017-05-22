import os.path
from twisted.internet.protocol import Factory
from twisted.logger import Logger
import sqlite3

from .protocol import ServerProtocol
from shared.card_database_manager import CardDatabaseManager
from shared.path import getScriptDirectory

class ServerFactory(Factory):
  card_database = None
  log = Logger()
  serverDatabase = None
  users=[]

  def buildProtocol(self, addr):
    return ServerProtocol(self)

  def openServerDatabase(self):
    self.serverDatabase = sqlite3.connect(os.path.join(getScriptDirectory(), "server.db"))
    cursor = self.serverDatabase.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY, 'name' VARCHAR(30), 'password' CHAR(128))")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'games' ('id' BIGINT NOT NULL, 'players' TEXT, 'cards' TEXT, 'password_hash' CHAR(128), 'database_hash' CHAR(128))")
    self.serverDatabase.commit()
    self.log.info("Loaded server database")

  def startFactory(self):
    self.card_database = CardDatabaseManager()
    self.card_database.loadPath('cards.db')
    self.log.info("Loaded card database")

    self.openServerDatabase()

    # after doing all the startup stuff
    self.log.info("Server up and running, waiting for incoming connections")
