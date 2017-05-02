import sys

from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.logger import globalLogBeginner, Logger, textFileLogObserver

from .display import Display
from .factory import ClientFactory

def main():
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

  display = Display()

  game_ticker = LoopingCall(display.process)
  game_ticker.start(1.0 / 30.0) # 30 fps

  reactor.run()
