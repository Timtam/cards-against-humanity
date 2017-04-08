import json
from twisted.logger import Logger
from twisted.protocols.basic import LineReceiver

class JSONReceiver(LineReceiver):
  log = Logger()

  def lineReceived(self, line):
    data = json.loads(line)
    code = int(data["code"])
    del(data["code"])
    self.messageReceived(code, data)

  def messageReceived(self, code, data):
    pass

  def sendMessage(self, code, **data):
    data["code"] = int(code)
    self.sendLine(json.dumps(data))
