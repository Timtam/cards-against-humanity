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
