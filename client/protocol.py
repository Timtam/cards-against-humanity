from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ClientProtocol(JSONReceiver):
  def __init__(self, factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_ACCEPTED, self.clientAccepted)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_REFUSED, self.clientRefused)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_SERVER_AUTHENTIFICATION, self.serverAuthentification)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.identification = 'server'
    self.server_version = {'MAJOR': 0, 'MINOR': 0, 'REVISION': 0}

  def connectionMade(self):
    self.sendMessage(MSG_CLIENT_AUTHENTIFICATION, major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)

  def serverAuthentification(self, major, minor, revision):
    self.server_version = {'MAJOR': major, 'MINOR': minor, 'REVISION': revision}

  def clientRefused(self, reason):
    print reason

  def clientAccepted(self):
    print 'client accepted'