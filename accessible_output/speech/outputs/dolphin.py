from ctypes import windll
from ... import output
from accessible_output import paths

from main import OutputError, ScreenreaderSpeechOutput

class Dolphin (ScreenreaderSpeechOutput):
 """Supports dolphin products."""

 name = 'Dolphin'

 def __init__(self, *args, **kwargs):
  super(Dolphin, self).__init__(*args, **kwargs)
  try:
   self.dll = windll.LoadLibrary(paths.root('lib\\dolapi.dll'))
  except:
   raise OutputError

 def speak(self, text, interrupt=0):
  if interrupt:
   self.silence()
#If we don't call this, the API won't let us speak.
  if self.canSpeak():
   self.dll.DolAccess_Command(unicode(text), (len(text)*2)+2, 1)

 def silence(self):
  self.dll.DolAccess_Action(141)

 def canSpeak(self):
  try:
   return self.dll.DolAccess_GetSystem() in (1, 4, 8) and super(Dolphin, self).canSpeak()
  except:
   return False
