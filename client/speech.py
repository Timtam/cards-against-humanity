import platform
if platform.system() == 'Windows' or platform.system().startswith('CYGWIN'):
  from accessible_output.speech import Speaker
elif platform.system() == 'Linux':
  import speechd

  class Speaker(object):
    def __init__(self):
      self.Client=speechd.SSIPClient('cah-speech-client')


    def output(self,text,interrupt=False):
      if interrupt: self.Client.stop()
      self.Client.speak(text)
