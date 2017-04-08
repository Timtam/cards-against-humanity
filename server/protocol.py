from .user import User
from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):

  def __init__(self,factory):
    self.callbacks = {
                       MSG_CLIENT_AUTHENTIFICATION: self.clientAuthentification
                     }
    self.factory = factory
    self.user = User(self)

  def connectionMade(self):
    self.log.info("Connection established from {connection}", connection=self.transport.getPeer())
    self.sendMessage(MSG_SERVER_AUTHENTIFICATION, version={"major": version.MAJOR, "minor": version.MINOR, "revision": version.REVISION}, databaseVersion=self.factory.cardsDatabaseVersion)

  def messageReceived(self, code, data):
    if not code in self.callbacks:
      self.log.warn("Received unsupported message {message} with code {code} from {connection}", message=data, connection=self.transport.getPeer(), code=code)
    else:
      self.callbacks[code](**data)

  def clientAuthentification(self, username, password):
    if self.user.exists():
      self.sendMessage(MSG_CLIENT_LOGIN, success=self.user.login(username, password))
    else:
      self.sendMessage(MSG_CLIENT_REGISTRATION, success=self.user.register(username, password))
