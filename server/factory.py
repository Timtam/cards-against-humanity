import os.path
from twisted.internet.protocol import Factory
from twisted.logger import Logger
import sqlite3

from .protocol import ServerProtocol
from shared.path import getScriptDirectory

class ServerFactory(Factory):
  databaseVersion = 0
  log = Logger()

  def buildProtocol(self, addr):
    return ServerProtocol()

  def startFactory(self):
    database = sqlite3.connect(os.path.join(getScriptDirectory(), "cards.db"))
    cursor = database.cursor()
    cursor.execute("SELECT value FROM config WHERE key = ?", ("version",))
    self.databaseVersion=int(cursor.fetchone()[0])
    database.close()
    self.log.info("Loaded database version {log_source.databaseVersion!r}")
