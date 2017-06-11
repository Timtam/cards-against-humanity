import os.path
import sys

def getScriptDirectory():
  if hasattr(sys, "frozen") and sys.frozen in ["console_exe", "windows_exe"]:
    path=os.path.dirname(sys.executable)
  else:
    path = os.path.dirname(os.path.abspath(os.path.join(__file__,'..')))
  while not os.path.isdir(path):
    path=os.path.abspath(path+'/..')
  return path
