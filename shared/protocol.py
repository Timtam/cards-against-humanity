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
    self.raw_args = []
    self.raw_callback = None
    self.raw_data = ''
    self.raw_remaining = 0

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

  def getMode(self):
    return self.mode

  def sendRawData(self, data):
    while len(data):
      self.transport.write(data[:self.MAX_LENGTH])
      data = data[self.MAX_LENGTH:]

  def receiveRawData(self, length, callback, *args):
    self.raw_args = args
    self.raw_callback = callback
    self.raw_data = ''
    self.raw_remaining = length
    self.setRawMode()

  def rawDataReceived(self, data):
    self.raw_remaining -= len(data)
    self.raw_data += data
    if self.raw_remaining == 0:
      self.setLineMode()
      self.raw_callback(*self.raw_args)
