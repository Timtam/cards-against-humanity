from .user import User
from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):

  def __init__(self,factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_AUTHENTIFICATION, self.clientAuthentification)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_AUTHENTIFICATION, self.userAuthentification)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_QUERY, self.databaseQuery)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_PULL, self.databasePull)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_KNOWN, self.databaseKnown)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_JOIN_GAME, self.joinGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_DELETE_GAME, self.deleteGame)
    self.addCallback(MODE_IN_GAME, MSG_START_GAME, self.startGame)
    self.addCallback(MODE_IN_GAME, MSG_CHOOSE_CARDS, self.chooseCards)
    self.addCallback(MODE_IN_GAME, MSG_CZAR_DECISION, self.czarDecision)
    self.addCallback(MODE_IN_GAME, MSG_SUSPEND_GAME, self.suspendGame)
    self.addCallback(MODE_IN_GAME, MSG_LEAVE_GAME, self.leaveGame)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.user = User(self)

  def connectionMade(self):
    self.identification = self.transport.getPeer().host
    self.log.info("{log_source.identification!r} established connection")

  def userAuthentification(self, username, password):
    if len(username)<6 or len(username)>30 or len(password)!=128:
      self.log.warn('{log_source.identification!r} username or password with incorrect length specified')
      self.sendMessage(MSG_USER_LOGIN, success=False, message='invalid username or password specified')
      return
    if not self.user.exists(username):
      registration = True
      result = self.user.register(username, password)
      self.log.info('{log_source.identification!r} {message}', message=result['message'])
      self.sendMessage(MSG_USER_REGISTRATION, **result)
      if not result['success']:
        self.transport.loseConnection()
        return
    result = self.user.login(username, password)
    if result['success']:
      self.identification = self.user.name
      self.setMode(MODE_INITIAL_SYNC)
      for user in self.factory.getAllUsers():
        if user is not self.user:
          user.protocol.sendMessage(MSG_LOGGED_IN, user_id = self.user.id, user_name = self.user.name)

    self.log.info('{log_source.identification!r} {message}', message=result['message'])
    self.sendMessage(MSG_USER_LOGIN, **result)
    if not result['success']:
      self.transport.loseConnection()
    else:
      users = [{'id': u.id, 'name': u.name} for u in self.factory.getAllUsers() if u.id != self.user.id]
      self.sendMessage(MSG_CURRENT_USERS, users = users)
      games = [{'id': g.id, 'name': g.name} for g in self.factory.getAllGames() if g.mayJoin(self.user)['join']]
      self.sendMessage(MSG_CURRENT_GAMES, games = games)

  def clientAuthentification(self, major, minor, revision):
    self.log.info('{log_source.identification!r} using client version {major}.{minor}.{revision}', major=major, minor=minor, revision=revision)
    if major < version.MAJOR or minor < version.MINOR:
      self.log.info('incompatible client version, connection refused')
      self.sendMessage(MSG_CLIENT_REFUSED, reason='incompatible client and server versions')
      self.transport.loseConnection()
    else:
      self.sendMessage(MSG_CLIENT_ACCEPTED)
      self.setMode(MODE_USER_AUTHENTIFICATION)

  def databaseQuery(self):
    self.sendMessage(MSG_DATABASE_QUERY, hash=self.factory.card_database.hash)

  def databasePull(self):
    self.log.info("{log_source.identification!r} requests card database")
    self.sendMessage(MSG_DATABASE_PUSH, size=self.factory.card_database.size)
    self.sendRawData(self.factory.card_database.data)

  def databaseKnown(self):
    self.log.info("{log_source.identification!r} knows current card database")
    self.sendMessage(MSG_SYNC_FINISHED)
    self.setMode(MODE_FREE_TO_JOIN)

  def createGame(self, game_name, game_password = None):
    if len(game_name)==0 or len(game_name)>30 or (game_password is not None and len(game_password)!=128):
      self.sendMessage(MSG_CREATE_GAME, success=False, message='invalid name or password')
      self.log.warn("{log_source.identification!r} tried to create game with invalid name {name} or password", name=game_name)
      return
    if self.factory.card_database.max_players_per_game < 3:
      self.sendMessage(MSG_CREATE_GAME, success=False, message='not enough cards available to create a game')
      self.log.warn("{log_source.identification!r} tried to create a game, but not enough cards available")
      return
    if self.factory.gameExists(game_name):
      self.sendMessage(MSG_CREATE_GAME, success = False, message = 'a game with this name already exists')
      self.log.info("{log_source.identification!r} tried to create a game with name {name}, but a game with this name already exists", name = game_name)
      return

    game = self.factory.createGame(game_name, game_password)
    self.log.info("{log_source.identification!r} created new game {name} with id {id}", name=game_name, id = game.id)

    for user in self.factory.getAllUsers():
      user.protocol.sendMessage(MSG_CREATE_GAME, game_id = game.id, name = game_name)

    self.joinGame(game.id, game_password)

  def joinGame(self, game_id, game_password = None):
    game = self.factory.findGame(game_id)
    if not game:
      self.sendMessage(MSG_JOIN_GAME, success = False, message='game not found')
      self.log.warn("{log_source.identification!r} tried to join non-existant game")
      return

    joinable = {}
    for user in self.factory.getAllUsers():
      joinable[user] = game.mayJoin(user)['join']

    result = game.join(self.user, game_password)
    if not result['success']:
      self.log.info("{log_source.identification!r} failed to join game {id}: {message}", id = game.id, message = result['message'])
    else:
      self.log.info("{log_source.identification!r} joined game {id}", id = game.id)
      self.setMode(MODE_IN_GAME)
      for user in game.getAllUsers():
        if user is not self.user:
          user.protocol.sendMessage(MSG_JOINED_GAME, user_id = self.user.id, game_id = game.id)
      self.sendMessage(MSG_JOIN_GAME, users = [u.id for u in game.getAllUsers() if u != self.user], **result)

      for user in self.factory.getAllUsers():
        if joinable[user] != game.mayJoin(user)['join']:
          user.protocol.sendMessage(MSG_DELETE_GAME, game_id = game.id)

  def startGame(self):
    game = self.user.getGame()

    joinable = {}
    for user in self.factory.getAllUsers():
      joinable[user] = game.mayJoin(user)['join']

    result = game.start()
    if not result['success']:
      self.log.info("{log_source.identification!r} failed to start game {id}: {message}", id = game.id, message=result['message'])
    else:
      self.log.info("{log_source.identification!r} started game {id}", id = game.id)
    self.sendMessage(MSG_START_GAME, **result)
    if not result['success']:
      return

    for user in game.getAllUsers():
      user.protocol.sendMessage(MSG_STARTED_GAME, user_id = self.user.id, points = [[p[0].id, p[1]] for p in game.points])

    for user in self.factory.getAllUsers():
      if joinable[user] != game.mayJoin(user)['join']:
        user.protocol.sendMessage(MSG_DELETE_GAME, game_id = game.id)

    self.sendTurnStarted()

  def chooseCards(self, cards):
    game = self.user.getGame()
    card = game.getCurrentBlackCard()
    if len(cards) != card.placeholders:
      self.log.warn('{log_source.identification!r} sent an invalid amount of cards for placeholders ({placeholders} placeholders, {cards} cards)', placeholders = card.placeholders, card = len(cards))
      self.sendMessage(MSG_CHOOSE_CARDS, success = False, message = 'invalid amount of cards selected')
      return

    result = game.chooseCards(self.user, [self.factory.card_database.getCard(c) for c in cards])

    if not result['success']:
      self.log.info('{log_source.identification!r} unable to choose cards: {message}', message = result['message'])
      self.sendMessage(MSG_CHOOSE_CARDS, **result)
      return

    for user in game.getAllUsers():
      user.protocol.sendMessage(MSG_CHOOSE_CARDS, user_id = self.user.id)

    # maybe we already got all choices and can send them to the players
    if game.choices_remaining == 0:
    
      choices = [[c.id for c in o] for o in game.getAllChoices()]

      for user in game.getAllUsers():
        user.protocol.sendMessage(MSG_CHOICES, choices = choices)

  def czarDecision(self, cards):

    game = self.user.getGame()

    if self.user is not game.getAllUsers()[0]:
      self.log.warn("{log_source.identification!r} tried to decide, but isn't the czar")
      self.sendMessage(MSG_CZAR_DECISION, success = False, message = "you aren't the czar")
      return

    result = game.decide([self.factory.card_database.getCard(c) for c in cards])

    if not result['success']:
      self.sendMessage(MSG_CZAR_DECISION, **result)
      return

    for user in game.getAllUsers():
      user.protocol.sendMessage(MSG_CZAR_DECISION, winner = result['winner'].id, end = result['end'])

    if not result['end']:
      self.sendTurnStarted()

  def suspendGame(self):

    game = self.user.getGame()

    if game is None:
      return

    joinable = {}
    for user in self.factory.getAllUsers():
      joinable[user] = game.mayJoin(user)['join']

    if game.open:
      code = MSG_LEAVE_GAME
      game.leave(self.user)
    else:
      code = MSG_SUSPEND_GAME
      game.suspend(self.user)

    for user in self.factory.getAllUsers():
      user.protocol.sendMessage(code, user_id = self.user.id, game_id = game.id)
      if len(game.users) == 0:
        user.protocol.sendMessage(MSG_DELETE_GAME, game_id = game.id)
      else:
        if joinable[user] != game.mayJoin(user)['join']:
          user.protocol.sendMessage(MSG_CREATE_GAME, game_id = game.id, name = game.name)

    self.setMode(MODE_FREE_TO_JOIN)

  def leaveGame(self):

    game = self.user.getGame()

    if game is None:
      self.log.warn("{log_source.identification!r} tried to leave a game, but isn't in any game")
      self.sendMessage(MSG_LEAVE_GAME, success = False, message = "you aren't in any game")
      return

    joinable = {}
    for user in self.factory.getAllUsers():
      joinable[user] = game.mayJoin(user)['join']

    result = game.leave(self.user)

    if not result['success']:
      self.sendMessage(MSG_LEAVE_GAME, **result)
      return

    self.setMode(MODE_FREE_TO_JOIN)

    for user in game.getAllUsers():
      user.protocol.sendMessage(MSG_LEAVE_GAME, game_id = game.id, user_id = self.user.id)
    self.sendMessage(MSG_LEAVE_GAME, game_id = game.id, user_id = self.user.id)

    for user in self.factory.getAllUsers():
      if joinable[user] != game.mayJoin(user)['join']:
        user.protocol.sendMessage(MSG_CREATE_GAME, game_id = game.id, name = game.name)

  def deleteGame(self, game_id):

    game = self.factory.findGame(game_id)

    if game is None:
      self.sendMessage(MSG_DELETE_GAME, success = False, message = 'game not found')
      return

    if len(game.getAllUsers()) > 0:
      self.sendMessage(MSG_DELETE_GAME, success = False, message = 'there are currently users in this game')
      return

    if not game.isCreator(self.user):
      self.sendMessage(MSG_DELETE_GAME, success = False, message = 'you are not the creator of this game')
      return

    game.unlink(True)

    for user in self.factory.getAllUsers():
      user.protocol.sendMessage(MSG_DELETE_GAME, game_id = game.id)

  def connectionLost(self, reason):
    self.log.info('{log_source.identification!r} lost connection')
    self.log.debug(reason.getErrorMessage())
    self.suspendGame()
    self.user.unlink()
    for user in self.factory.getAllUsers():
      user.protocol.sendMessage(MSG_LOGGED_OFF, user_id = self.user.id)

  def sendTurnStarted(self):
    game = self.user.getGame()

    pairs = game.getAllWhiteCardsForUsers()
    black_card = game.getCurrentBlackCard()

    for pair in pairs:
      pair[0].protocol.sendMessage(MSG_DRAW_CARDS, cards = [c.id for c in pair[1]])
      pair[0].protocol.sendMessage(MSG_CZAR_CHANGE, user_id = pairs[0][0].id, card = black_card.id)

