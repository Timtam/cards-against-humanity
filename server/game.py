import copy
import json
import random
import uuid

from twisted.logger import Logger

from . import version

class Game(object):
  log = Logger()

  def __init__(self, factory):
    self.factory = factory
    self.black_cards = []
    self.database_hash = None
    self.name = ''
    self.open = True
    self.password_hash = None
    self.running = False
    self.uuid = None
    self.users = []
    self.white_cards = []

  @classmethod
  def create(cls, factory, name, password_hash = None):
    game = cls(factory)
    game.database_hash = factory.card_database.hash
    game.name = name
    game.password_hash = password_hash
    game.uuid = uuid.uuid4()
    game.loadCards()
    return game

  @classmethod
  def load(cls, factory, **data):
    game = cls(factory)
    game.name = data['name']
    game.password_hash = data['password_hash'] if len(data['password_hash']) else None
    game.open = False
    game.database_hash = data['database_hash']
    game.uuid = uuid.UUID(data['id'])

    game.users = json.loads(data['users'])
    for user in game.users:
      user['joined'] = False
      user['chosen_cards'] = []
      user['white_cards'] = [factory.card_database.getCard(c) for c in user['white_cards']]

    game.white_cards = [factory.card_database.getCard(c) for c in json.loads(data['cards'])['white_cards']]
    game.black_cards = [factory.card_database.getCard(c) for c in json.loads(data['cards'])['black_cards']]

    return game

  def loadCards(self):

    if len(self.black_cards) == 0:
      self.black_cards = self.factory.card_database.getBlackCards()
      random.shuffle(self.black_cards)

      if self.factory.black_cards > -1:
        self.black_cards = self.black_cards[:self.factory.black_cards]

    if len(self.white_cards) == 0:
      self.white_cards = self.factory.card_database.getWhiteCards()

      # we need to strip all white cards users currently have in their pile
      for user in self.users:
        for card in user['white_cards']:
          del self.white_cards[self.white_cards.index(card)]

      random.shuffle(self.white_cards)

  def mayJoin(self, user):

    if self.running:
      return self.formatted(join = False, message = 'game already running')

    if not self.factory.gameExists(self.name):
      return self.formatted(join = False, message = "game doesn't exist anymore")

    if user.getGame() == self:
      return self.formatted(join = False, message = 'user already in this game')

    if self.open:
      if len(self.users) + 1 > self.factory.card_database.max_players_per_game:
        return self.formatted(join=False, message='no more players allowed')
      return self.formatted(join=True)
    else:
      possible_users = [u for u in self.users if u['user'] == user.id]

      if len(possible_users) != 1:
        return self.formatted(join = False, message = 'you are no member of this paused game')

      return self.formatted(join = True)

  def join(self, user, password):
    joinable = self.mayJoin(user)
    if not joinable['join']:
      return self.formatted(success=False, message=joinable['message'])
    if self.protected and password != self.password_hash or not self.protected and password != None:
      return self.formatted(success=False, message='wrong password supplied')

    if self.open:
      self.users.append(self.userdict(user, len(self.users) == 0))
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
    try:
      return self.black_cards[0]
    except IndexError:
      return None

  def getAllWhiteCardsForUsers(self):
    return [(self.factory.findUser(self.users[i]['user']), self.users[i]['white_cards']) for i in range(len(self.users))]

  def suspend(self, user):

    self.pause()

    if user.getGame() is not self:
      self.log.warn('user {user} not in game {game}', user = user.id, game = self.id)
      return

    possible_users = [u for u in self.users if u['user'] == user.id and u['joined']]
    if len(possible_users) != 1:
      self.log.warn('found {count} users in game {game} while suspending due to user {user}', count = len(possible_users), game = self.id, user = user.id)
    else:
      possible_users[0]['joined'] = False
      user.setGame(None)
      self.log.info('user {user} suspended game {game}', user = user.id, game = self.id)

  def leave(self, user):
    # forces the user to leave

    if user.getGame() is not self:
      return self.formatted(success = False, message = 'user is not in this game')

    if len(self.getAllUsers()) == 0:
      self.log.warn('no users in this game, {user} tried to leave', user = user.id)
      return self.formatted(success = False, message = 'no users found in this game')

    possible_users = [u for u in self.users if u['user'] == user.id and u['joined']]

    if len(possible_users) != 1:
      self.log.warn('{user} tried to leave game {game}, but found {count} possible users', user = user.id, game = self.id, count = len(possible_users))
      return self.formatted(success = False, message = 'unable to find user in this game')

    del self.users[self.users.index(possible_users[0])]
    user.setGame(None)

    self.log.info('user {user} left game {game}', user = user.id, game = self.id)

    self.pause()

    if len(self.users)<3 and not self.open:
      # this game will be opened up new soon
      # we will have to filter all users who aren't currently in here
      self.users = [u for u in self.users if u['joined']]

      if len(self.users)>0 :
        self.open = True
        for user in self.users:
          user['white_cards'] = []
          user['chosen_cards'] = []
          user['black_cards'] = 0
        self.white_cards = []
        self.black_cards = []
        self.loadCards()

        if possible_users[0]['creator']:
          for u in self.users:
            if u != possible_users[0] and not u['creator']:
              u['creator'] = True
              break

        self.log.info('not enough users left, game opened up all new')

    return self.formatted(success = True, unlinked = self.unlink())

  def pause(self):

    if not self.running:
      return

    white_cards = []

    self.running = False

    for user in self.users:
      user['chosen_cards'] = []
      white_cards += user['white_cards']
      user['white_cards'] = []

    white_cards += self.white_cards

    self.white_cards = white_cards
      
    self.log.info('game {game} paused', game = self.id)

  def unlink(self, force = False):
    # can only unlink if no users are left
    # as long as it is not forced (force by using the delete button)
    if len(self.users)>0 and not force:
      return False

    self.factory.unlinkGame(self)
    self.log.info('game {game} deleted', game = self.id)
    return True

  def pack(self):
    # saves the current game into the database
    # at first we construct the sql arguments dict

    args = {}

    args['id'] = self.uuid.hex
    args['name'] = self.name

    users = copy.deepcopy(self.users)
    for user in users:
      del user['joined']
      del user['chosen_cards']
      user['white_cards'] = [c.id for c in user['white_cards']]

    args['users'] = json.dumps(users)

    black_cards = [c.id for c in self.black_cards]
    white_cards = [c.id for c in self.white_cards]

    args['cards'] = json.dumps({'white_cards': white_cards, 'black_cards': black_cards})

    args['password_hash'] = self.password_hash if self.protected else ''
    args['database_hash'] = self.database_hash
    args['server_version_major'] = version.MAJOR
    args['server_version_minor'] = version.MINOR
    args['server_version_revision'] = version.REVISION

    return args

  def chooseCards(self, user, cards):
    d = [u for u in self.users if u['user'] == user.id]

    if len(d) != 1:
      self.log.warn('user {user} wants to choose cards, but user not found in game {game}', user = user.id, game = self.id)
      return self.formatted(success = False, message = 'user not in this game')

    d = d[0]

    for card in cards:
      if not card in d['white_cards']:
        return self.formatted(success = False, message = 'user doesn\'t hold this card in his hand')

    d['chosen_cards'] = cards

    return self.formatted(success = True)

  def getAllChoices(self):
    # returns all choices from all users, but in shuffled order (important)
    choices = [u['chosen_cards'] for u in self.users if self.users.index(u)>0]

    random.shuffle(choices)

    return choices

  def decide(self, cards):

    # let's see to which user those cards match
    user = [u for u in self.users if u['chosen_cards'] == cards]

    if len(user) != 1:
      return self.formatted(success = False, message = "no user found with those cards")

    # the user needs to gain one point

    user = user[0]

    user['black_cards'] += 1

    # as next we remove the current black card
    del self.black_cards[0]

    next_black_card = self.getCurrentBlackCard()

    # at next, all chosen cards must be removed from the user's white cards pile
    # and the chosen cards must be resetted
    for user in self.users:
      for card in user['chosen_cards']:
        del user['white_cards'][user['white_cards'].index(card)]
      user['chosen_cards'] = []

    # we distribute new white cards to all users
    # all users need to get the same amount
    for user in self.users:
      if self.users.index(user) == 0:
        continue # the czar didn't lose cards
      for i in range(len(cards)):
        if len(self.white_cards) == 0:
          # we need to load the white cards pile all new
          self.loadCards()

        user['white_cards'].append(self.white_cards[0])
        del self.white_cards[0]

    # and of course the current czar must be moved to the end of the line
    self.users.append(self.users[0])
    del self.users[0]

    if next_black_card is None:
      # the game finished and we can reset it
      end = True
      self.open = True
      self.running = False
      self.white_cards = []
      self.black_cards = []
      for user in self.users:
        user['white_cards'] = []
        user['black_cards'] = 0

      self.loadCards()

    else:
      end = False

    return self.formatted(success = True, winner = self.factory.findUser(user['user']), end = end)


  def isCreator(self, user):

    possible_users = [u for u in self.users if u['user'] == user.id]

    if len(possible_users) == 0:
      return False

    return possible_users[0]['creator']

  @staticmethod
  def userdict(user, creator):
    return {
            'user': user.id,
            'joined': True,
            'black_cards': 0,
            'white_cards': [],
            'chosen_cards': [],
            'creator': creator
           }

  @staticmethod
  def formatted(**kwargs):
    return kwargs

  @property
  def protected(self):
    return self.password_hash != None

  @property
  def id(self):
    return self.uuid.int

  @property
  def choices_remaining(self):
    return len([u for u in self.users if len(u['chosen_cards']) == 0 and self.users.index(u)>0])

  @property
  def points(self):
    return [(self.factory.findUser(u['user']), u['black_cards'], ) for u in self.users]
