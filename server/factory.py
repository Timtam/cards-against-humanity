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
    self.serverDatabase.cursor().execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY, 'name' VARCHAR(30), 'password' CHAR(128))")
    self.serverDatabase.commit()
    self.log.info("Opened server database")

  def startFactory(self):
    self.card_database = CardDatabaseManager('cards.db')
    self.log.info("Loaded card database version {log_source.card_database.version!r}")

    self.openServerDatabase()

    # after doing all the startup stuff
    self.log.info("Server up and running, waiting for incoming connections")
