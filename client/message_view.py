import pygame

from .tools import *
from .view import View

class MessageView(View):
  def __init__(self, display):
    View.__init__(self, display)


  # setting some automatically formatted and rendered text onto the screen
  def setText(self, text):
    pass


  # may display a button (not needed)
  # window may also exist without any button
  # if callback is None, the button will be removed
  # otherwise it will be created
  def setButton(self, text='', callback=None):
    pass


  def render(self):
    pass


  def handleEvent(self, event):
    pass

