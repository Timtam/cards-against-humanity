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
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
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
      self.factory.display.view.loggedInMessage(message)
    else:
      self.factory.display.view.errorMessage(message)

  def userRegistration(self, success, message):
    if not success:
      self.factory.display.view.errorMessage(message)
