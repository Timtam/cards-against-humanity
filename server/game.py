import random
import uuid

from twisted.logger import Logger

class Game(object):
  log = Logger()

  def __init__(self, factory, name, password_hash = None):
    self.black_cards = []
    self.database_hash = factory.card_database.hash
    self.factory = factory
    self.id = uuid.uuid4().int
    self.name = name
    self.open = True
    self.password_hash = password_hash
    self.running = False
    self.users = []
    self.white_cards = []

    self.loadCards()

  def loadCards(self):

    self.black_cards = self.factory.card_database.getBlackCards()
    random.shuffle(self.black_cards)

    self.white_cards = self.factory.card_database.getWhiteCards()
    random.shuffle(self.white_cards)

  def mayJoin(self, user):
    if user.getGame() is not None:
      return self.formatted(success = False, message = 'already in another game')
    if self.running:
      return self.formatted(success = False, message = 'game already running')
    if self.open:
      if len(self.users) + 1 > self.factory.card_database.max_players_per_game:
        return self.formatted(join=False, message='no more players allowed', password=self.password_hash != None)
      return self.formatted(join=True, password=self.password_hash != None)
    else:
      possible_users = [u for u in self.users if u['user'] == user.id]

      if len(possible_users) != 1:
        return self.formatted(success = False, message = 'you are no member of this paused game')

      if possible_users[0]['joined']:
        return self.formatted(success = False, message = 'already joined this game')

      return self.formatted(success = True)

  def join(self, user, password):
    joinable = self.mayJoin(user)
    if not joinable['join']:
      return self.formatted(success=False, message=joinable['message'])
    if joinable['password'] and password != self.password_hash:
      return self.formatted(success=False, message='wrong password supplied')

    if self.open:
      self.users.append(self.userdict(user))
      user.setGame(self)
    else:
      possible_users = [u for u in self.users if u['user'] == user.id and not u['joined']]
      possible_users[0]['joined'] = True
      user.setGame(self)

    return self.formatted(success=True, game_id = self.id)

  def getAllUsers(self):
    return [self.factory.findUser(u['user']) for u in self.users if u['joined']]

  def start(self):
    if len(self.getAllUsers())<3:
      return self.formatted(success=False, message='not enough players in this game')

    if self.running:
      return self.formatted(success=False, message='already running')

    # if the game is currently open, we need to shuffle the users
    if self.open:
      random.shuffle(self.users)
      self.open = False

    self.open = False
    self.running = True

    # all users need to get 10 cards
    for i in range(len(self.users)*10):
      self.users[i/10]['white_cards'].append(self.white_cards[i])
    self.white_cards=self.white_cards[len(self.users)*10:]

    # determine the one with the black card
    # index at 0 will always be the czar
    # and black_cards 0 will always be the current black card

    return self.formatted(success=True)

  def getCurrentBlackCard(self):
    return self.black_cards[0]

  def getAllWhiteCardsForUsers(self):
    return [(self.factory.findUser(self.users[i]['user']), self.users[i]['white_cards']) for i in range(len(self.users))]

  def disconnect(self, user):

    self.pause()

    if user.getGame() is not self:
      self.log.warn('user {user} not in game {game}', user = user.id, game = self.id)
      return

    possible_users = [u for u in self.users if u['id'] == user.id and u['joined']]
    if len(possible_users) != 1:
      self.log.warn('found {count} users in game {game} while disconnecting user {user}', count = len(possible_users), game = self.id, user = user.id)
    else:
      possible_users[0]['joined'] = False
      user.setGame(None)
      self.log.info('user {user} disconnected from game {game}', user = user.id, game = self.id)

  def leave(self, user):
    # forces the user to leave
    # users which are the current czar in this running game can't leave

    if user.getGame() is not self:
      return self.formatted(success = False, message = 'user is not in this game')

    users = self.getAllUsers()
    if len(users) == 0:
      self.log.warn('no users in this game, {user} tried to leave', user = user.id)
      return self.formatted(success = False, message = 'no users found in this game')

    if users[0] == user:
      self.log.info('czar {user} tried to leave the game, but this is not possible', user = user.id)
      return self.formatted(success = False, message = 'the czar cannot leave the game')

    possible_users = [u for u in self.users if u['id'] == user.id and u['joined']]

    if len(possible_users) != 1:
      self.log.warn('{user} tried to leave game {game}, but found {count} possible users', user = user.id, game = self.id, count = len(possible_users))
      return self.formatted(success = False, message = 'unable to find user in this game')

    del self.users[self.users.index(possible_users[0])]
    user.setGame(None)
    self.log.info('user {user} left game {game}', user = user.id, game = self.id)

    return self.formatted(success = True)

  def pause(self):
    self.running = False
    self.log.info('game {game} paused', game = self.id)

  @staticmethod
  def userdict(user):
    return {
            'user': user.id,
            'joined': True,
            'black_cards': [],
            'white_cards': []
           }

  @staticmethod
  def formatted(**kwargs):
    return kwargs
