import sys

import pygame
from twisted.logger import globalLogBeginner, textFileLogObserver

from .display import Display



def main(accessibility=False):
  pygame.init()
  pygame.font.init()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])
  
  display = Display()
  display.init(accessibility)
