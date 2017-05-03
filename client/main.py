import sys

import pygame
from twisted.logger import globalLogBeginner, textFileLogObserver

from .display import Display



def main():
  pygame.init()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])
  
  display = Display()
  display.init()
