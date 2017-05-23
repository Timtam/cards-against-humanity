import random
import uuid

class Game(object):

  def __init__(self, factory, name, password_hash = None):
    self.black_cards = []
    self.database_hash = self.factory.card_database.hash
    self.factory = factory
    self.id = uuid.uuid4().int
    self.name = name
    self.open = True
    self.password_hash = password_hash
    self.users = []
    self.white_cards = []

    self.loadCards()

  def loadCards(self):

    self.black_cards = self.factory.card_database.getBlackCards()
    random.shuffle(self.black_cards)

    self.white_cards = self.factory.card_database.getWhiteCards()
    random.shuffle(self.white_cards)

  def mayJoin(self, user):
    if self.open:
      if len(self.users) + 1 > self.factory.card_database.max_players_per_game:
        return self.formatted(join=False, message='no more players allowed', password=self.password_hash != None)
      return self.formatted(join=True, password=self.password_hash != None)
    return self.formatted(join=False, message='game not open to join')

  def join(self, user, password):
    joinable = self.mayJoin(user)
    if not joinable['join']:
      return self.formatted(success=False, message=joinable['message'])
    if joinable['password'] and password != self.password_hash:
      return self.formatted(success=False, message='wrong password supplied')
    if user in self.users:
      return self.formatted(success=False, message='user joined already')
    self.users.append(user)
    return self.formatted(success=True)

  @staticmethod
  def formatted(**kwargs):
    return kwargs
