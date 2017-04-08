from twisted.logger import Logger

class User(object):
  log = Logger()

  def __init__(self, protocol):
    self.id = 0
    self.name = ""
    self.protocol = protocol

  def exists(self, name):
    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("SELECT count(*) FROM users WHERE name = ?", (name, ))
    return bool(cursor.fetchone()[0])

  def loggedIn(self):
    return id > 0

  def login(self, name, password):
    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("SELECT id FROM users WHERE name = ? AND password = ?", (name, password, ))
    result = cursor.fetchone()
    if len(result)==0:
      self.log.info("wrong login credentials supplied for user {name} or user not registered yet", name=name)
      return False

    self.name = name
    self.id = int(result[0])

    self.log.info("user {log_source.name!r} logged on for id {log_source.id!r}")

    return True

  def register(self, name, password):

    if self.exists(name):
      self.log.warn("user {name} already exists, so no registration possible", name=name)
      return False

    cursor = self.protocol.factory.serverDatabase.cursor()
    cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password, ))

    self.protocol.factory.serverDatabase.commit()

    self.log.info("user {name} registered successfully, continuing logging in", name=name)

    return self.login(name, password)
