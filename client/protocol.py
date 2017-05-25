from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ClientProtocol(JSONReceiver):
  def __init__(self, factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_ACCEPTED, self.clientAccepted)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_REFUSED, self.clientRefused)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_SERVER_AUTHENTIFICATION, self.serverAuthentification)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_LOGIN, self.userLogin)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_REGISTRATION, self.userRegistration)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_QUERY, self.databaseQuery)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_PUSH, self.databasePush)
    self.addCallback(MODE_INITIAL_SYNC, MSG_SYNC_FINISHED, self.syncFinished)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_JOIN_GAME, self.joinGame)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.database_hash = None
    self.identification = 'server'
    self.server_version = {'MAJOR': 0, 'MINOR': 0, 'REVISION': 0}
    self.factory.client = self

  def connectionMade(self):
    self.sendMessage(MSG_CLIENT_AUTHENTIFICATION, major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)

  def serverAuthentification(self, major, minor, revision):
    self.server_version = {'MAJOR': major, 'MINOR': minor, 'REVISION': revision}

  def clientRefused(self, reason):
    self.factory.display.view.clientRefusedMessage(reason)

  def clientAccepted(self):
    username, password = self.factory.display.getLoginCredentials()
    self.sendMessage(MSG_USER_AUTHENTIFICATION, username=username, password=password)
    self.setMode(MODE_USER_AUTHENTIFICATION)
    self.factory.display.view.loginMessage()

  def userLogin(self, success, message):
    if success:
      self.factory.display.view.syncMessage()
      self.setMode(MODE_INITIAL_SYNC)
      self.sendMessage(MSG_DATABASE_QUERY)
    else:
      self.factory.display.view.errorMessage(message)

  def userRegistration(self, success, message):
    if not success:
      self.factory.display.view.errorMessage(message)

  def databaseQuery(self, hash):
    self.factory.card_database.loadPath(self.factory.display.server_name, hash)
    if not self.factory.card_database.loaded:
      self.sendMessage(MSG_DATABASE_PULL)
      self.database_hash = hash
    else:
      self.sendMessage(MSG_DATABASE_KNOWN)

  def databasePush(self, size):
    self.receiveRawData(size, self.databaseKnown)

  def databaseKnown(self):
    self.factory.card_database.loadData(self.raw_data, self.factory.display.server_name, self.database_hash)
    self.sendMessage(MSG_DATABASE_KNOWN)

  def syncFinished(self):
    self.factory.display.view.loggedInMessage()
    self.sendMessage(MSG_CREATE_GAME, name='test')
    self.setMode(MODE_FREE_TO_JOIN)

  def createGame(self, success, id = '', message = ''):
    if success:
      self.sendMessage(MSG_JOIN_GAME, id=id)
    else:
      self.factory.display.setView('ConnectionView')
      self.factory.display.callFunction('self.view.errorMessage', message = message)

  def joinGame(self, success, message = ''):
    if success:
      self.setMode(MODE_IN_GAME)
      self.factory.display.setView('GameView')
    else:
      self.factory.display.setView('ConnectionView')
      self.factory.display.callFunction('self.view.errorMessage', message = message)
