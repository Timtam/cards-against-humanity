from . import version
from .constants import *
from shared.messages import *
from shared.protocol import JSONReceiver

from collections import Counter
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
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LOGGED_IN, self.loggedIn)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LOGGED_OFF, self.loggedOff)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_LEAVE_GAME, self.leaveGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_DELETE_GAME, self.deleteGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_SUSPEND_GAME, self.suspendGame)
    self.addCallback(MODE_IN_GAME, MSG_JOIN_GAME, self.joinGame)
    self.addCallback(MODE_IN_GAME, MSG_START_GAME, self.startGame)
    self.addCallback(MODE_IN_GAME, MSG_STARTED_GAME, self.startedGame)
    self.addCallback(MODE_IN_GAME, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_IN_GAME, MSG_DRAW_CARDS, self.drawCards)
    self.addCallback(MODE_IN_GAME, MSG_CZAR_CHANGE, self.czarChange)
    self.addCallback(MODE_IN_GAME, MSG_LOGGED_IN, self.loggedIn)
    self.addCallback(MODE_IN_GAME, MSG_LOGGED_OFF, self.loggedOff)
    self.addCallback(MODE_IN_GAME, MSG_LEAVE_GAME, self.leaveGame)
    self.addCallback(MODE_IN_GAME, MSG_SUSPEND_GAME, self.suspendGame)
    self.addCallback(MODE_IN_GAME, MSG_DELETE_GAME, self.deleteGame)
    self.addCallback(MODE_IN_GAME, MSG_CHOOSE_CARDS, self.chooseCards)
    self.addCallback(MODE_IN_GAME, MSG_CHOICES, self.choices)
    self.addCallback(MODE_IN_GAME, MSG_CZAR_DECISION, self.czarDecision)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.database_hash = None
    self.identification = 'server'
    self.server_version = {'MAJOR': 0, 'MINOR': 0, 'REVISION': 0}
    self.factory.client = self
    self.user_id = 0
    self.game_id = 0
    self.manual_close = False

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
    self.setMode(MODE_FREE_TO_JOIN)
    self.factory.display.setView('OverviewView')
    self.factory.display.login_sound.stop()
    self.factory.display.login_sound.play()

  def createGame(self, success=True, game_id = '', message = '', name = '', creator = False, users = 0, rounds = 0, protected = False):
    if success:
      self.factory.addGame(game_id, name, creator, rounds = rounds, protected = protected)
      if self.getMode() == MODE_FREE_TO_JOIN:
        self.factory.display.callFunction('self.view.addGame', game_id)
        self.factory.display.game_created_sound.stop()
        self.factory.display.game_created_sound.play()
    else:
      self.factory.display.callFunction('self.view.errorMessage', message = message)

  def joinGame(self, success=True, message = '', game_id = 0, user_id = 0, users = []):
    if success:

      self.factory.incrementUsers(game_id)
      if self.getMode() == MODE_FREE_TO_JOIN:
        if user_id == self.user_id:
          self.game_id = game_id
          self.setMode(MODE_IN_GAME)
          self.factory.display.setView('GameView')
          self.factory.display.callFunction('self.view.player_indicators.addPlayer', self.user_id)
          for user in users:
            self.factory.display.callFunction('self.view.player_indicators.addPlayer', user)
          self.factory.display.game_join_sound.stop()
          self.factory.display.game_join_sound.play()
        else:
          self.factory.display.callFunction('self.view.updateGame', game_id)
      elif self.getMode() == MODE_IN_GAME and game_id == self.game_id:
        self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('{player} joined the game').format(player = self.factory.findUsername(user_id)))
        self.factory.display.callFunction('self.view.player_indicators.addPlayer', user_id)
        self.factory.display.game_join_sound.stop()
        self.factory.display.game_join_sound.play()

    else:
      self.factory.display.callFunction('self.view.errorMessage', message = message)

  def startGame(self, success, message=''):
    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)

  def loggedIn(self, user_id, user_name):
    self.factory.addUser(user_id, user_name)

  def loggedOff(self, user_id):
    self.factory.removeUser(user_id)

  def startedGame(self, user_id, points):
    if user_id == self.user_id:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate("You started the game."))
    else:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('{player} started the game').format(player = self.factory.findUsername(user_id)))

    self.factory.updateGamePoints(self.game_id, points)
    self.factory.display.game_start_sound.stop()
    self.factory.display.game_start_sound.play()

  def drawCards(self, cards):
    cards = [self.factory.card_database.getCard(c) for c in cards]
    self.factory.display.callFunction('self.view.setCards', *cards)

    self.factory.display.game_draw_sounds[random.randint(0, len(self.factory.display.game_draw_sounds)-1)].play()

  def czarChange(self, user_id, card):
    if user_id == self.user_id:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate("You were chosen the new czar and therefore flip a black card open. You won't be able to play any white card until the next player will be chosen to be the czar."))
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_CZAR_WAITING)
    else:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate("{player} was chosen the new czar and therefore flips a new black card open.").format(player = self.factory.findUsername(user_id)))
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_PLAYER)
    card = self.factory.card_database.getCard(card)
    self.factory.display.callFunction('self.view.setBlackCard', card)
    self.factory.display.callFunction('self.view.player_indicators.setCzar', user_id)
    
  def currentUsers(self, users):
    for u in users:
      self.factory.addUser(**u)

  def currentGames(self, games):
    for g in games:
      self.factory.addGame(**g)

  def leaveGame(self, game_id, user_id):
    self.factory.decrementUsers(game_id)
    if self.getMode() == MODE_IN_GAME and game_id == self.game_id:
      self.factory.resetGamePoints(self.game_id)
      if user_id != self.user_id:
        self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('{player} left the game.').format(player = self.factory.findUsername(user_id)))
        self.factory.display.callFunction('self.view.player_indicators.delPlayer', user_id)
        self.factory.display.callFunction('self.view.setMode', GAME_MODE_PAUSED)
      else:
        self.factory.display.setView('OverviewView')
        self.setMode(MODE_FREE_TO_JOIN)
        self.game_id = 0
      self.factory.display.game_leave_sound.stop()
      self.factory.display.game_leave_sound.play()
    elif self.getMode() == MODE_FREE_TO_JOIN:
      self.factory.display.callFunction('self.view.updateGame', game_id)

  def suspendGame(self, user_id, game_id):
    self.factory.decrementUsers(game_id)
    if self.getMode() == MODE_IN_GAME and game_id == self.game_id:
      self.factory.resetGamePoints(self.game_id)
      if user_id != self.user_id:
        self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('{player} suspended the game.').format(player = self.factory.findUsername(user_id)))
        self.factory.display.callFunction('self.view.setMode', GAME_MODE_PAUSED)
        self.factory.display.callFunction('self.view.player_indicators.delPlayer', user_id)
      else:
        self.factory.display.setView('OverviewView')
        self.setMode(MODE_FREE_TO_JOIN)
        self.game_id = 0
    elif self.getMode() == MODE_FREE_TO_JOIN:
      self.factory.display.callFunction('self.view.updateGame', game_id)

  def deleteGame(self, success = True, game_id = 0, message = ''):
    if success:
      self.factory.removeGame(game_id)
      if self.getMode() == MODE_FREE_TO_JOIN:
        self.factory.display.callFunction('self.view.deleteGame', game_id)
        self.factory.display.game_deleted_sound.stop()
        self.factory.display.game_deleted_sound.play()
        self.factory.display.view.default_mode = True
    elif not success and self.getMode() == MODE_FREE_TO_JOIN:
      self.factory.display.view.errorMessage(message)


  def sendStartGame(self):
    self.sendMessage(MSG_START_GAME)

  def chooseCards(self, success = True, message = '', user_id = 0):
    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)
      return

    self.factory.display.callFunction('self.view.player_indicators.setChosen', user_id)
    self.factory.display.game_choose_sound.stop()
    self.factory.display.game_choose_sound.play()

    if user_id == self.user_id:
      text = self.factory.display.translator.translate("You put your chosen cards onto the table.")
    else:
      text = self.factory.display.translator.translate("{player} put his chosen cards onto the table.").format(player = self.factory.findUsername(user_id))

    self.factory.display.view.speak(text)

  def choices(self, choices):

    choices = [[self.factory.card_database.getCard(c) for c in o] for o in choices]

    if self.factory.display.view.mode == GAME_MODE_CZAR_WAITING:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('All players confirmed their choices. You now have to select the choice which you think is the best.'))
      self.factory.display.callFunction('self.view.setMode', GAME_MODE_CZAR_DECIDING)
    else:
      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('All players confirmed their choices and the czar now has to select the best one out of them.'))

    self.factory.display.callFunction('self.view.setChoices', choices)

  def czarDecision(self, success = True, winner = 0, message = '', end = False, rounds = 0):

    if not success:
      self.factory.display.callFunction('self.view.writeLogError', message)
      return

    if winner == self.user_id:
      text = self.factory.display.translator.translate("You win this round and therefore gain a point.")
    else:
      text = self.factory.display.translator.translate("{player} wins this round and therefore gains a point.").format(player = self.factory.findUsername(winner))
    self.factory.display.callFunction('self.view.writeLog', text)

    self.factory.updateGamePoints(self.game_id, [[winner, 1]])
    self.factory.decrementRounds(self.game_id)

    if winner == self.user_id:
      self.factory.display.game_score_sound.stop()
      self.factory.display.game_score_sound.play()
    else:
      self.factory.display.game_score_other_sound.stop()
      self.factory.display.game_score_other_sound.play()

    if end == True:

      self.factory.setRounds(self.game_id, rounds)

      fmt_winners = lambda w: ', '.join(w[:-1])+' '+self.factory.display.translator.translate('and')+' '+w[-1] if len(w)>1 else w[0]

      self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate("This ends the game."))

      winners = self.factory.getWinners(self.game_id)

      resolved_winners_without_me = [self.factory.findUsername(w) for w in winners.keys() if w != self.user_id]

      if self.user_id in winners:

        if len(winners) == 1: # you are the only winner
          self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('You win this game with {points} points. Congratulations!').format(points = winners[self.user_id]))
          self.factory.display.game_win_sound.stop()
          self.factory.display.game_win_sound.play()

        else: # tie
          self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate('You are one of the proud winners of this game and ended up gaining {points} points. Congratulations! But {players} gained the same amount of points.').format(points = winners[self.user_id], players = fmt_winners(resolved_winners_without_me)))
          self.factory.display.game_tie_sound.stop()
          self.factory.display.game_tie_sound.play()

      else: # you didn't win anything
        self.factory.display.callFunction('self.view.writeLog', self.factory.display.translator.translate("Sad, but true. You didn't win anything. {players} scored {points} points and made the game.").format(points = winners.values()[0], players = fmt_winners(resolved_winners_without_me)))
        self.factory.display.game_lose_sound.stop()
        self.factory.display.game_lose_sound.play()

      game = self.factory.findGame(self.game_id)

      score_table = Counter(game['points'])

      text = ''

      for score in score_table.most_common(10):

        text += self.factory.display.translator.translate('{player}: {points} points').format(player = self.factory.display.translator.translate('You') if score[0] == self.user_id else self.factory.findUsername(score[0]), points = score[1])+'\n'

      self.factory.display.callFunction('self.view.writeLog', text[:-1])

      self.factory.display.callFunction('self.view.setMode', GAME_MODE_PAUSED)
      self.factory.resetGamePoints(self.game_id)

  def sendChooseCards(self, cards):
    self.sendMessage(MSG_CHOOSE_CARDS, cards = [c.id for c in cards])

  def sendCzarDecision(self, cards):
    self.sendMessage(MSG_CZAR_DECISION, cards = [c.id for c in cards])

  def sendCreateGame(self, name, password, rounds):
    cmd = {
           'game_name': name
          }

    if password is not None:
      cmd['game_password'] = password

    if rounds is not None:
      cmd['rounds'] = rounds

    self.sendMessage(MSG_CREATE_GAME, **cmd)

  def sendJoinGame(self, id, password):

    cmd = {
           'game_id': id
          }

    if password is not None:
      cmd['game_password'] = password

    self.sendMessage(MSG_JOIN_GAME, **cmd)

  def sendSuspendGame(self):
    self.sendMessage(MSG_SUSPEND_GAME)

  def sendLeaveGame(self):
    self.sendMessage(MSG_LEAVE_GAME)

  def sendDeleteGame(self, id):
    self.sendMessage(MSG_DELETE_GAME, game_id = id)

  def connectionLost(self, reason):

    if not self.manual_close and self.factory.display.running and self.getMode() not in [MODE_CLIENT_AUTHENTIFICATION, MODE_USER_AUTHENTIFICATION, MODE_INITIAL_SYNC]:
      self.factory.display.setView('LoginView')
      self.factory.display.callFunction('self.view.errorMessage', self.factory.display.translator.translate('Lost connection to server')+': '+reason.getErrorMessage())

  def loseConnection(self):
    self.manual_close = True
    self.transport.loseConnection()
