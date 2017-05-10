from ctypes import windll
from accessible_output import paths

from main import OutputError, ScreenreaderSpeechOutput

class SystemAccess (ScreenreaderSpeechOutput):
 """Supports System Access and System Access Mobile"""

 name = 'SystemAccess'

 def __init__(self, *args, **kwargs):
  super(SystemAccess, self).__init__(*args, **kwargs)
  try:
   self.dll = windll.LoadLibrary(paths.root('lib\\SAAPI32.dll'))
  except:
   raise OutputError

 def speak(self, text, interrupt=0):
  if self.dll.SA_IsRunning():
   self.dll.SA_SayW(unicode(text))

 def canSpeak(self):
  try:
   return self.dll.SA_IsRunning() and super(SystemAccess, self).canSpeak()
  except:
   return False
