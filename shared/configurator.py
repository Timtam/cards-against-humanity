import os.path
import cPickle

from .path import getScriptDirectory
from .translator import Translator

# name of the save file
SAVE_FILENAME = 'config.dat'

# not containing all methods, but instead properties which will be pickled and saved
class DataSafe(object):
  def __init__(self):
    pass

class Configurator(object):

  options = {
    'client': {
      'language': Translator.getDefaultLanguage()
    },
    'editor': {
      'language': Translator.getDefaultLanguage()
    }
  }

  def __init__(self, node):
    self.node = node
    self.save_path = os.path.join(getScriptDirectory(), SAVE_FILENAME)
    if os.path.isfile(self.save_path):
      with open(self.save_path, 'rb') as f:
        self.__save = cPickle.loads(f.read())
    else:
      self.__save = DataSafe()
    self.init()

  def init(self):
    # this function initializes all options
    # this will be needed if we load an old save file which doesn't contain some new options
    # in this case we will add them with some default value
    # if no save file exists, we'll just add all values brand new
    if not self.node in self.options:
      self.options[self.node] = {}

    for key in self.options.keys():
      if not key in self.__save.__dict__:
        self.__save.__dict__[key]={}
      for k in self.options[key].keys():
        if not k in self.__save.__dict__[key]:
          self.__save.__dict__[key][k] = self.options[key][k]

  def save(self):
    with open(self.save_path, 'wb') as f:
      f.write(cPickle.dumps(self.__save, cPickle.HIGHEST_PROTOCOL))

  def set(self, option, value):
    self.__save.__dict__[self.node][option] = value

  def get(self, option):
    return self.__save.__dict__[self.node][option]
