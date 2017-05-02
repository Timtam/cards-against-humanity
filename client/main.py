import sys

from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from twisted.logger import globalLogBeginner, Logger, textFileLogObserver

from .factory import ClientFactory

def main():
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

  reactor.run()
