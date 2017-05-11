import json
from twisted.logger import Logger
from twisted.protocols.basic import LineReceiver

from .messages import MODE_NONE

class JSONReceiver(LineReceiver):
  log = Logger()

  def __init__(self, factory):
    self.callbacks = {}
    self.factory = factory
    self.identification = '' # should be shadowed for proper usage
    self.mode = MODE_NONE

  def lineReceived(self, line):
    data = json.loads(line)
    code = int(data["code"])
    del(data["code"])
    self.messageReceived(code, data)

  def messageReceived(self, code, data):
    if not code in self.callbacks[self.mode]:
      self.log.warn('{log_source.identification!r} sent message {code}:{message}, but message not known or not parseable in current mode {log_source.mode!r}', code=code, message=data)
    else:
      self.callbacks[self.mode][code](**data)

  def sendMessage(self, code, **data):
    data["code"] = int(code)
    self.sendLine(json.dumps(data))

  def addCallback(self, mode, code, callback):
    if not mode in self.callbacks:
      self.callbacks[mode]={}
    self.callbacks[mode][code]=callback

  def setMode(self, mode):
    self.mode = mode
