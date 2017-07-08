import sys
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.logger import globalLogBeginner, Logger, textFileLogObserver

from .argumentparser import ArgumentParser
from .factory import ServerFactory
from . import version
from shared.path import getScriptDirectory

def main():
  parser = ArgumentParser()
  parser.execute()

  log = Logger()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

  log.info("Starting cards-against-humanity server version {major}.{minor}.{revision}", major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)

  endpoint = TCP4ServerEndpoint(reactor, parser.port)
  endpoint.listen(ServerFactory(parser.black_cards, parser.database))
  reactor.run()
