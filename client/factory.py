from twisted.internet.protocol import Factory
from twisted.logger import Logger

from .protocol import ClientProtocol
from shared.card_database_manager import CardDatabaseManager

class ClientFactory(Factory):
  log = Logger()

  def __init__(self, display):
    self.card_database = CardDatabaseManager()
    self.client = None
    self.display = display
    self.games = []
    self.users = []

  def buildProtocol(self, addr):
    self.client = ClientProtocol(self)
    return self.client

  def closeClient(self):
    if self.client:
      self.client.transport.loseConnection()
      self.client = None

  def addUser(self, id, name):
    self.users.append({
      'name': name,
      'id': id
    })

  def findUsername(self, id):
    user = [u for u in self.users if u['id'] == id]
    if len(user)==0:
      return ''
    return user[0]['name']

  def removeUser(self, id):
    i = -1
    for j in range(len(self.users)):
      if self.users[i]['id'] == id:
        i = j
        return

    if i == -1:
      self.log.warn('no user with id {id} found to remove', id = id)
    else:
      del self.users[i]

  def addGame(self, id, name):
    self.games.append({
      'id': id,
      'name': name
    })

  def findGamename(self, id):
    game = [g for g in self.games if g['id'] == id]
    if len(game)==0:
      return ''
    return game[0]['name']

  def removeGame(self, id):
    self.games = [g for g in self.games if g['id'] != id]
