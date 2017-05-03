import pygame
import sys

from twisted.logger import globalLogBeginner, Logger, textFileLogObserver

from .display import Display
from .factory import ClientFactory

def main():
  pygame.init()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

  display = Display()
  display.init()
