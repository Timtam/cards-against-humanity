from collections import Counter
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
      self.client.loseConnection()
      self.client = None
      self.games = []
      self.users = []
      self.card_database = CardDatabaseManager()

  def addUser(self, id, name):
    self.users.append({
      'name': name,
      'id': id
    })

  def findUsername(self, id):
    if id == self.client.user_id:
      return self.display.login_name

    user = [u for u in self.users if u['id'] == id]
    if len(user)==0:
      return ''
    return user[0]['name']

  def removeUser(self, id):
    self.users = [u for u in self.users if u['id'] != id]

  def addGame(self, id, name, creator, users = 0, rounds = 0):
    self.games.append({
      'id': id,
      'name': name,
      'points': {},
      'creator': creator,
      'users': users,
      'rounds': rounds
    })

  def findGame(self, id):
    game = [g for g in self.games if g['id'] == id]
    if len(game) != 1:
      return None
    return game[0]

  def findGamename(self, id):
    game = self.findGame(id)

    if game is None:
      return ''
    return game['name']

  def removeGame(self, id):
    self.games = [g for g in self.games if g['id'] != id]

  def updateGamePoints(self, id, points):
    game = self.findGame(id)
    if game is None:
      return

    for p in points:
      try:
        game['points'][p[0]] += p[1]
      except KeyError:
        game['points'][p[0]] = p[1]

  def getGamePoints(self, id):
    game = self.findGame(id)
    if game is None:
      return {}
    return game['points']

  def resetGamePoints(self, id):
    game = self.findGame(id)
    if game is None:
      return
    game['points'] = {}

  def getAllGames(self):
    return self.games

  def isCreator(self, id):

    game = self.findGame(id)

    if game is None:
      return False

    return game['creator']

  def getWinners(self, id):

    game = self.findGame(id)

    if game is None:
      return {}

    table = Counter(game['points'])

    # we'll have to find out how many people have the highest amount of points
    # that's why we'll have to revert the counter

    reverted_table = Counter(table.values())

    winners = {}

    for pair in table.most_common(reverted_table.most_common(1)[0][0]):
      winners[pair[0]] = pair[1]

    return winners


  def incrementUsers(self, id):

    game = self.findGame(id)

    if game is None:
      return

    game['users'] += 1


  def decrementUsers(self, id):

    game = self.findGame(id)

    if game is None:
      return

    game['users'] -= 1


  def decrementRounds(self, id):

    game = self.findGame(id)

    if game is None:
      return

    game['rounds'] -= 1
