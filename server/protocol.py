from .user import User
from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):

  def __init__(self,factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_AUTHENTIFICATION, self.clientAuthentification)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_AUTHENTIFICATION, self.userAuthentification)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_QUERY, self.databaseQuery)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_PULL, self.databasePull)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_KNOWN, self.databaseKnown)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.user = User(self)

  def connectionMade(self):
    self.identification = self.transport.getPeer().host
    self.log.info("{log_source.identification!r} established connection")

  def userAuthentification(self, username, password):
    if len(username)<6 or len(username)>30 or len(password)!=128:
      self.log.warn('{log_source.identification!r} username or password with incorrect length specified')
      self.sendMessage(MSG_USER_LOGIN, success=False, message='invalid username or password specified')
      return
    if not self.user.exists(username):
      registration = True
      result = self.user.register(username, password)
      self.log.info('{log_source.identification!r} {message}', message=result['message'])
      self.sendMessage(MSG_USER_REGISTRATION, **result)
      if not result['success']:
        self.transport.loseConnection()
        return
    result = self.user.login(username, password)
    if result['success']:
      self.identification = self.user.name
      self.setMode(MODE_INITIAL_SYNC)
    self.log.info('{log_source.identification!r} {message}', message=result['message'])
    self.sendMessage(MSG_USER_LOGIN, **result)
    if not result['success']:
      self.transport.loseConnection()
 
  def clientAuthentification(self, major, minor, revision):
    self.log.info('{log_source.identification!r} using client version {major}.{minor}.{revision}', major=major, minor=minor, revision=revision)
    if major < version.MAJOR or minor < version.MINOR:
      self.log.info('incompatible client version, connection refused')
      self.sendMessage(MSG_CLIENT_REFUSED, reason='incompatible client and server versions')
      self.transport.loseConnection()
    else:
      self.sendMessage(MSG_CLIENT_ACCEPTED)
      self.setMode(MODE_USER_AUTHENTIFICATION)

  def databaseQuery(self):
    self.sendMessage(MSG_DATABASE_QUERY, hash=self.factory.card_database.hash)

  def databasePull(self):
    self.log.info("{log_source.identification!r} requests card database")
    self.sendMessage(MSG_DATABASE_PUSH, size=self.factory.card_database.size)
    self.sendRawData(self.factory.card_database.data)

  def databaseKnown(self):
    self.log.info("{log_source.identification!r} knows current card database")
    self.sendMessage(MSG_SYNC_FINISHED)

  def connectionLost(self, reason):
    self.log.info('{log_source.identification!r} lost connection')
    self.log.debug(reason.getErrorMessage())
    self.user.unlink()
