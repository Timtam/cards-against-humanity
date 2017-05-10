from pywintypes import com_error
import win32com.client

from main import OutputError, ScreenreaderSpeechOutput

class Virgo (ScreenreaderSpeechOutput):
 """Speech output supporting the Virgo screen reader."""

 name = 'Virgo'

 def __init__(self, *args, **kwargs):
  super (Virgo, self).__init__(*args, **kwargs)
  try:
   self.object = win32com.client.Dispatch("phoenix.PHX_Func_Class")
  except com_error: #try jfwapi
   raise OutputError

 def speak(self, text, interrupt=True):
  self.object.saycommand(text)

 def canSpeak(self):
  return True
 def silence(self):
  self.object.saycommand('')