from pywintypes import com_error
import win32com.client

from main import OutputError, BrailleOutput

class Virgo (BrailleOutput):
 """Braille output supporting the Virgo screen reader."""

 name = 'Virgo'

 def __init__(self, *args, **kwargs):
  super (Virgo, self).__init__(*args, **kwargs)
  try:
   self.object = win32com.client.Dispatch("phoenix.BrailleSysClass")
  except com_error: 
   raise OutputError

 def braille(self, text):
  self.object.sayonbraille(True,text)

 def canBraille(self):
  return True