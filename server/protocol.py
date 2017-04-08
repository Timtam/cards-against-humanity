from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):
  callbacks = {}

  def __init__(self,factory):
    self.callbacks = {
                     }
    self.factory = factory

  def connectionMade(self):
    self.log.info("Connection established from {connection}", connection=self.transport.getPeer())
    self.sendMessage(MSG_SERVER_AUTHENTIFICATION, version={"major": version.MAJOR, "minor": version.MINOR, "revision": version.REVISION}, databaseVersion=self.factory.databaseVersion)

  def messageReceived(self, code, data):
    if not code in self.callbacks:
      self.log.warn("Received unsupported message {message} with code {code} from {connection}", message=data, connection=self.transport.getPeer(), code=code)
    else:
      self.callbacks[code](**data)
