from twisted.logger import Logger

class User(object):
  log = Logger()

  def __init__(self, protocol):
    self.id = 0
    self.name = ""
    self.protocol = protocol
    self.protocol.factory.users.append(self)

  def exists(self, name):
    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("SELECT count(*) FROM users WHERE name = ?", (name, ))
    return bool(cursor.fetchone()[0])

  def loggedIn(self):
    return self.id > 0

  def login(self, name, password):

    if self.loggedIn():
      return self.formatted(success=False, message='user %s currently logged in'%username)

    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("SELECT id FROM users WHERE name = ? AND password = ?", (name, password, ))
    result = cursor.fetchone()
    if not result:
      return self.formatted(success=False, message='wrong login credentials supplied')

    self.name = name
    self.id = int(result[0])

    return self.formatted(success=True, message='login successful')

  def register(self, name, password):

    if self.exists(name):
      return self.formatted(success=False, message='username already in use')

    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password, ))

    self.protocol.factory.serverDatabase.commit()

    return self.formatted(success=True, message='registration successful')

  def unlink(self):
    del self.protocol.factory.users[self.protocol.factory.users.index(self)]

  # this is quite a dirty way
  # it just formats the keyword arguments into a dict and returns it
  # that's actually just for pretty printing purposes
  def formatted(self, **kwargs):
    return kwargs
