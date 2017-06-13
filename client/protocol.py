from . import version
from .constants import *
from shared.messages import *
from shared.protocol import JSONReceiver

import random

class ClientProtocol(JSONReceiver):
  def __init__(self, factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_ACCEPTED, self.clientAccepted)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_REFUSED, self.clientRefused)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_SERVER_AUTHENTIFICATION, self.serverAuthentification)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_LOGIN, self.userLogin)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_REGISTRATION, self.userRegistration)
    self.addCallback(MODE_INITIAL_SYNC, MSG_CURRENT_GAMES, self.currentGames)
    self.addCallback(MODE_INITIAL_SYNC, MSG_CURRENT_USERS, self.currentUsers)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_QUERY, self.databaseQuery)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_PUSH, self.databasePush)
    self.addCallback(MODE_INITIAL_SYNC, MSG_SYNC_FINISHED, self.syncFinished)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_JOIN_GAME, self.joinGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_JOINED_GAME, self.joinedGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LOGGED_IN, self.loggedIn)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LOGGED_OFF, self.loggedOff)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_DISCONNECTED_FROM_GAME, self.disconnectedFromGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LEFT_GAME, self.leftGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_DELETED_GAME, self.deletedGame)
    self.addCallback(MODE_IN_GAME, MSG_START_GAME, self.startGame)
    self.addCallback(MODE_IN_GAME, MSG_STARTED_GAME, self.startedGame)
    self.addCallback(MODE_IN_GAME, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_IN_GAME, MSG_DRAW_CARDS, self.drawCards)
    self.addCallback(MODE_IN_GAME, MSG_CZAR_CHANGE, self.czarChange)
    self.addCallback(MODE_IN_GAME, MSG_JOINED_GAME, self.joinedGame)
    self.addCallback(MODE_IN_GAME, MSG_LOGGED_IN, self.loggedIn)
    self.addCallback(MODE_IN_GAME, MSG_LOGGED_OFF, self.loggedOff)
    self.addCallback(MODE_IN_GAME, MSG_LEFT_GAME, self.leftGame)
    self.addCallback(MODE_IN_GAME, MSG_DISCONNECTED_FROM_GAME, self.disconnectedFromGame)
    self.addCallback(MODE_IN_GAME, MSG_DELETED_GAME, self.deletedGame)
    self.addCallback(MODE_IN_GAME, MSG_CHOOSE_CARDS, self.chooseCards)
    self.addCallback(MODE_IN_GAME, MSG_CHOICES_REMAINING, self.choicesRemaining)
    self.addCallback(MODE_IN_GAME, MSG_CHOICES, self.choices)
    self.addCallback(MODE_IN_GAME, MSG_CZAR_DECISION, self.czarDecision)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.database_hash = None
    self.identification = 'server'
    self.server_version = {'MAJOR': 0, 'MINOR': 0, 'REVISION': 0}
    self.factory.client = self
    self.user_id = 0
    self.game_id = 0

  def connectionMade(self):
    self.sendMessage(MSG_CLIENT_AUTHENTIFICATION, major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)

  def serverAuthentification(self, major, minor, revision):
    self.server_version = {'MAJOR': major, 'MINOR': minor, 'REVISION': revision}

  def clientRefused(self, reason):
    self.factory.display.view.clientRefusedMessage(reason)

  def clientAccepted(self):
    username, password = self.factory.display.getLoginCredentials()
    self.sendMessage(MSG_USER_AUTHENTIFICATION, username=username, password=password)
    self.setMode(MODE_USER_AUTHENTIFICATION)
    self.factory.display.view.loginMessage()

  def userLogin(self, success, message, user_id = 0):
    if success:
      self.user_id = user_id
      self.factory.display.view.syncMessage()
      self.setMode(MODE_INITIAL_SYNC)
      self.sendMessage(MSG_DATABASE_QUERY)
    else:
      self.factory.display.view.errorMessage(message)

  def userRegistration(self, success, message):
    if not success:
      self.factory.display.view.errorMessage(message)

  def databaseQuery(self, hash):
    self.factory.card_database.loadPath(self.factory.display.server_name, hash)
    if not self.factory.card_database.loaded:
      self.sendMessage(MSG_DATABASE_PULL)
      self.database_hash = hash
    else:
      self.factory.card_database.loadCards()
      self.sendMessage(MSG_DATABASE_KNOWN)

  def databasePush(self, size):
    self.receiveRawData(size, self.databaseKnown)

  def databaseKnown(self):
    self.factory.card_database.loadData(self.raw_data, self.factory.display.server_name, self.database_hash)
    self.factory.card_database.loadCards()
    self.sendMessage(MSG_DATABASE_KNOWN)

  def syncFinished(self):
    self.factory.display.view.loggedInMessage()
    self.setMode(MODE_FREE_TO_JOIN)
    if len(self.factory.games)>0:
      self.sendMessage(MSG_JOIN_GAME, game_id = self.factory.games[0]['id'])
    else:
      self.sendMessage(MSG_CREATE_GAME, game_name='test')

  def createGame(self, success=True, game_id = '', message = '', name = '', user_id = ''):
    if success:
      self.factory.addGame(game_id, name)
      if self.getMode() == MODE_FREE_TO_JOIN and user_id == self.user_id:
        self.sendMessage(MSG_JOIN_GAME, game_id=game_id)
    else:
      self.factory.display.setView('ConnectionView')
      self.factory.display.callFunction('self.view.errorMessage', message = message)

  def joinGame(self, success, message = '', game_id = 0, users = []):
    if success:
      self.game_id = game_id
      self.setMode(MODE_IN_GAME)
      self.factory.display.setView('GameView')
      self.factory.display.callFunction('self.view.player_indicators.addPlayer', self.user_id)
      for user in users:
        self.factory.display.callFunction('self.view.player_indicators.addPlayer', user)
      self.factory.display.join_game_sound.stop()
      self.factory.display.join_game_sound.play()
    else:
      self.factory.display.setView('ConnectionView')
      self.factory.display.callFunction('self.view.errorMessage', message = message)

  def startGame(self, success, message=''):
    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)

  def joinedGame(self, user_id, game_id):
    if self.getMode() == MODE_IN_GAME and game_id == self.game_id:
      self.factory.display.callFunction('self.view.writeLog', '%s joined the game'%self.factory.findUsername(user_id))
      self.factory.display.callFunction('self.view.player_indicators.addPlayer', user_id)
      self.factory.display.join_game_sound.stop()
      self.factory.display.join_game_sound.play()

  def loggedIn(self, user_id, user_name):
    self.factory.addUser(user_id, user_name)
    print user_name+ ' logged in'

  def loggedOff(self, user_id):
    self.factory.removeUser(user_id)

  def startedGame(self, user_id, points):
    if user_id == self.user_id:
      user = 'you'
    else:
      user = self.factory.findUsername(user_id)

    self.factory.display.callFunction('self.view.writeLog', '%s started the game'%user)

    self.factory.updateGamePoints(self.game_id, points)

  def drawCards(self, cards):
    cards = [self.factory.card_database.getCard(c) for c in cards]
    self.factory.display.callFunction('self.view.setCards', *cards)

    self.factory.display.draw_sounds[random.randint(0, len(self.factory.display.draw_sounds)-1)].play()

  def czarChange(self, user_id, card):
    if user_id == self.user_id:
      self.factory.display.callFunction('self.view.writeLog', 'you were chosen the new czar and therefore flip a black card open. You won\'t be able to play any white card until the next player will be chosen to be the czar.')
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_CZAR_WAITING)
    else:
      self.factory.display.callFunction('self.view.writeLog', '%s was chosen the new czar and therefore flips a new black card open'%self.factory.findUsername(user_id))
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_PLAYER)
    card = self.factory.card_database.getCard(card)
    self.factory.display.callFunction('self.view.setBlackCard', card)
    
  def currentUsers(self, users):
    for u in users:
      self.factory.addUser(**u)

  def currentGames(self, games):
    for g in games:
      self.factory.addGame(**g)

  def leftGame(self, game_id, user_id):
    if self.getMode() == MODE_IN_GAME and game_id == self.game_id:
      if user_id != self.user_id:
        self.factory.display.callFunction('self.view.writeLog', '%s left the game'%self.factory.findUsername(user_id))
        self.factory.display.callFunction('self.view.player_indicators.delPlayer', user_id)
      else:
        # TODO: going back to overview screen
        self.setMode(MODE_FREE_TO_JOIN)
      self.factory.display.leave_game_sound.stop()
      self.factory.display.leave_game_sound.play()

  def disconnectedFromGame(self, user_id, game_id):
    if self.getMode() == MODE_IN_GAME and game_id == self.game_id:
      if user_id != self.user_id:
        self.factory.display.callFunction('self.view.writeLog', '%s disconnected, thus this game paused.'%self.factory.findUsername(user_id))
        self.factory.display.callFunction('self.view.setMode', GAME_MODE_PAUSED)
        self.factory.display.callFunction('self.view.player_indicators.delPlayer', user_id)

  def deletedGame(self, game_id):
    self.factory.removeGame(game_id)

  def sendStartGame(self):
    self.sendMessage(MSG_START_GAME)

  def chooseCards(self, success, message = ""):
    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)

  def choicesRemaining(self, remaining, out_of):
    self.factory.display.callFunction('self.view.writeLog', 'A selection was submitted. %d out of %d remaining'%(remaining, out_of))

  def choices(self, choices):

    choices = [[self.factory.card_database.getCard(c) for c in o] for o in choices]

    if self.factory.display.view.mode == GAME_MODE_CZAR_WAITING:
      self.factory.display.callFunction('self.view.writeLog', 'All players confirmed their choices. You now have to select the choice which you think is the best.')
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_CZAR_DECIDING)
    else:
      self.factory.display.callFunction('self.view.writeLog', 'All players confirmed their choices and the czar now has to select the best one out of them.')

    self.factory.display.callFunction('self.view.setChoices', choices)

  def czarDecision(self, success = True, winner = 0, message = '', end = False):

    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)
      return

    user = 'you' if winner == self.user_id else self.factory.findUsername(winner)

    self.factory.display.callFunction('self.view.writeLog', ('you' if winner == self.user_id else self.factory.findUsername(winner)) + " " + ('win' if self.user_id == winner else 'wins') + ' this round and ' + ('gain' if winner == self.user_id else 'gains' ) + ' a point.')

    self.factory.updateGamePoints(self.game_id, [[winner, 1]])

    self.updateGameStatistics()

    if end == True:
      self.factory.display.callFunction('self.view.writeLog', 'this ends the game. Yay!')
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_PAUSED)

  def sendChooseCards(self, cards):
    self.sendMessage(MSG_CHOOSE_CARDS, cards = [c.id for c in cards])

  def sendCzarDecision(self, cards):
    self.sendMessage(MSG_CZAR_DECISION, cards = [c.id for c in cards])

  def updateGameStatistics(self):

    text = ''
    points = self.factory.getGamePoints(self.game_id)

    for p in points.keys():
      user = 'you' if p == self.user_id else self.factory.findUsername(p)
      text += user + ": %d\n"%(points[p])

    self.factory.display.callFunction('self.view.writeLog', text)
