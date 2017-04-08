import os.path
from twisted.internet.protocol import Factory
from twisted.logger import Logger
import sqlite3

from .protocol import ServerProtocol
from shared.path import getScriptDirectory

class ServerFactory(Factory):
  cardsDatabaseVersion = 0
  log = Logger()
  serverDatabase = None

  def buildProtocol(self, addr):
    return ServerProtocol(self)

  def openServerDatabase(self):
    self.serverDatabase = sqlite3.connect(os.path.join(getScriptDirectory(), "server.db"))
    self.serverDatabase.cursor().execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY, 'name' VARCHAR(30), 'password' CHAR(128))")
    self.serverDatabase.commit()
    self.log.info("Opened server database")

  def startFactory(self):
    database = sqlite3.connect(os.path.join(getScriptDirectory(), "cards.db"))
    cursor = database.cursor()
    cursor.execute("SELECT value FROM config WHERE key = ?", ("version",))
    self.cardsDatabaseVersion=int(cursor.fetchone()[0])
    database.close()
    self.log.info("Loaded database version {log_source.cardsDatabaseVersion!r}")

    self.openServerDatabase()

    # after doing all the startup stuff
    self.log.info("Server up and running, waiting for incoming connections")
