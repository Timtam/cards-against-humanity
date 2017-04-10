from .user import User
from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):

  def __init__(self,factory):
    self.authenticated=False
    self.callbacks = {
                       MSG_USER_AUTHENTIFICATION: self.userAuthentification
                     }
    self.factory = factory
    self.user = User(self)

  def connectionMade(self):
    self.log.info("connection established from {connection}", connection=self.transport.getPeer())
    self.sendMessage(MSG_SERVER_AUTHENTIFICATION, version={"major": version.MAJOR, "minor": version.MINOR, "revision": version.REVISION}, databaseVersion=self.factory.cardsDatabaseVersion)

  def messageReceived(self, code, data):
    if not self.authenticated and code!=MSG_CLIENT_AUTHENTIFICATION:
      self.log.warn("received message {code}:{message} before actual client authentification", code=code, message=data)
      return
    if not code in self.callbacks:
      self.log.warn("received unsupported message {message} with code {code} from {connection}", message=data, connection=self.transport.getPeer(), code=code)
    else:
      self.callbacks[code](**data)

  def userAuthentification(self, username, password):
    if len(username)>30 or len(password)!=128:
      self.sendMessage(MSG_USER_LOGIN, success=False)
      return
    if self.user.exists():
      self.sendMessage(MSG_USER_LOGIN, success=self.user.login(username, password))
    else:
      self.sendMessage(MSG_USER_REGISTRATION, success=self.user.register(username, password))
