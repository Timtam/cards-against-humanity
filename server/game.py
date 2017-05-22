import uuid

class Game(object):

  def __init__(self, factory, name, password_hash = None):
    self.factory = factory
    self.id = uuid.uuid4().int
    self.name = name
    self.open = True
    self.password_hash = password_hash
    self.users = []

  def mayJoin(self, user):
    if self.open:
      return self.formatted(join=True, password=self.password_hash != None)
    return self.formatted(join=False)

  def join(self, user, password):
    joinable = self.mayJoin(user)
    if not joinable['join']:
      return self.formatted(success=False, message='unable to join')
    if joinable['password'] and password != self.password_hash:
      return self.formatted(success=False, message='wrong password supplied')
    if user in self.users:
      return self.formatted(success=False, message='user joined already')
    self.users.append(user)
    return self.formatted(success=True)

  @staticmethod
  def formatted(**kwargs):
    return kwargs
