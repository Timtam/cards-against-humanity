from main import BrailleOutput, OutputError
from accessible_output import paths
from ctypes import windll

class SystemAccess (BrailleOutput):

 """Supports Brailling to System Access."""

 name = 'System Access'

 def __init__(self, *args, **kwargs):
  super(SystemAccess, self).__init__(*args, **kwargs)
  try:
   self.dll = windll.LoadLibrary(paths.root('lib\\SAAPI32.dll'))
  except:
   raise OutputError

 def braille(self, text):
  self.dll.SA_BrlShowTextW(unicode(text))

 def canBraille(self):
  try:
   return self.dll.SA_IsRunning() and super(SystemAccess, self).canBraille()
  except:
   return False
