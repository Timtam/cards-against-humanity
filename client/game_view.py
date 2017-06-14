from shared.card import CARD_BLACK, CARD_WHITE
from shared.exceptions import CardLinkError
from .constants import *
from .view import View
from .tools import Button
from .scrolled_text_panel import ScrolledTextPanel
from .card_surface import CardSurface
from .player_indicators import PlayerIndicators

import copy
import pygame
import pygame.locals as pl

CARD_PADDING = 10
TEXT_PADDING = 10
CARD_SIZE = (160, 200)



class GameView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    self.display_size = self.display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.font = self.display.getFont()
    self.mode = GAME_MODE_PAUSED
    
    self.button_start_leave = Button(self.display, "Start Game", self.font, (self.display_size[0] * 0.85, self.display_size[1] * 0.1))
    self.button_start_leave.setCallback(self.onStartLeave)
    self.button_confirm = Button(self.display, "Confirm Choice", self.font, (self.display_size[0] * 0.85, self.display_size[1] * 0.2))
    self.button_confirm.setCallback(self.onConfirmChoice)
    
    self.player_indicators = PlayerIndicators(self.display, 5, 5)
    
    self.surface_gamelog = pygame.Surface((300, self.display_size[1] - 65))
    self.gamelog_border = pygame.Rect(0, 0, self.surface_gamelog.get_width(), self.surface_gamelog.get_height())
    self.gamelog_text = ScrolledTextPanel(self.display, TEXT_PADDING, 65 + TEXT_PADDING, self.surface_gamelog.get_width() - 2*TEXT_PADDING, self.surface_gamelog.get_height() - 2*TEXT_PADDING, True)
    self.gamelog_text.setFont(self.display.getFont(16))
    self.writeLog('you joined the game')
    self.gamelog_text.setLabel('game log')

    self.cards = []

    self.tab_order = [self.button_start_leave, self.button_confirm, self.gamelog_text]
    self.createCardSurfaces()
    self.setMode(GAME_MODE_PAUSED)
    self.tab_order.append(self.player_indicators)
    
    
  def createCardSurfaces(self):

    surface_cards_x = (self.display_size[0] - self.surface_gamelog.get_width()) / 2 + self.surface_gamelog.get_width()

    self.black_card_x = surface_cards_x - CARD_SIZE[0] / 2
    self.black_card_y = 45
    self.black_card = CardSurface(self.display, self.black_card_x, self.black_card_y, CARD_SIZE[0], CARD_SIZE[1], CARD_BLACK)
    self.black_card.setFont(self.display.getFont(18))
    self.black_card.setLabel('your selection')
    self.black_card.setEnable(False)

    self.tab_order.append(self.black_card)

    for i in range(10):
      card_position = ((i * (CARD_SIZE[0] + CARD_PADDING)) - (int(i / 5) * (CARD_SIZE[0] * 5 + CARD_PADDING * 5)) + surface_cards_x - (CARD_SIZE[0] * 5 + CARD_PADDING * 4)/2,
                       int(i / 5) * (CARD_SIZE[1] + CARD_PADDING) + 290)
      self.cards.append({
        'card': CardSurface(self.display, card_position[0], card_position[1], CARD_SIZE[0], CARD_SIZE[1]),
        'position': card_position,
      })
      self.cards[i]['card'].setFont(self.display.getFont(18))
      self.cards[i]['card'].setLabel('selectable card %d' % (i + 1))
      self.cards[i]['card'].setSpeakLines(False)
      self.cards[i]['card'].setCallback(self.generateCardLambda(i))
      self.tab_order.append(self.cards[i]['card'])
  
  
  def setCards(self, *cards):
    for i in range(len(cards)):
      self.cards[i]['card'].setCard(cards[i])
      self.cards[i]['card'].setEnable(True)

      if self.cards[i]['card'].chosen:
        self.cards[i]['card'].toggleChosen()

  def setBlackCard(self, card):
    self.black_card.setCard(card)

  def setChoices(self, choices):
    for i in range(10):
      self.clearCard(i)

    for i in range(len(choices)):
      card = copy.deepcopy(self.black_card.getCard())
      card.unlinkAll()
      for j in range(len(choices[i])):
        card.link(choices[i][j])
      self.cards[i]['card'].setEnable(self.mode == GAME_MODE_CZAR_DECIDING)
      self.cards[i]['card'].setCard(card)


  def writeLog(self, text):
    if self.gamelog_text.getText() != "":
      self.gamelog_text.addText("\n")
    self.gamelog_text.addText(text)
    self.speak(text, False)
  
  
  def writeLogError(self, text):
    self.writeLog('An error occured: '+text)
    self.display.game_error_sound.stop()
    self.display.game_error_sound.play()
  
  
  def onStartLeave(self):
    self.display.factory.client.sendStartGame()
  
  
  def handleEvent(self, event):
    View.handleEvent(self, event)
    self.button_start_leave.handleEvent(event)
    self.button_confirm.handleEvent(event)

    self.player_indicators.handleEvent(event)

    for i in range(10):
      self.cards[i]['card'].handleEvent(event)
      if event.type == pygame.KEYDOWN:
        if event.key == eval('pl.K_%d'%((i+1)%10)):
          try:
            self.tab_order[self.tab_position].setFocus(False)
          except AttributeError:
            pass
          self.cards[i]['card'].setFocus(True)
          self.tab_position = self.tab_order.index(self.cards[i]['card'])
          self.speak(self.cards[i]['card'].getLabel(), True)
    self.black_card.handleEvent(event)
    self.gamelog_text.handleEvent(event)

    if event.type == pygame.KEYDOWN:
      if event.key == pl.K_b:
        try:
          self.tab_order[self.tab_position].setFocus(False)
        except AttributeError:
          pass
        self.tab_position = self.tab_order.index(self.black_card)
        self.black_card.setFocus(True)
        self.speak(self.black_card.getLabel(), True)
  
  
  def update(self):
    View.update(self)
    self.player_indicators.update()
  
  
  def render(self):
    #self.surface_cards.fill((255, 255, 255))
    #self.surface_black_card.fill((0, 0, 0))
    self.surface_gamelog.fill((255, 255, 255))
    
    pygame.draw.rect(self.surface_gamelog, (0, 0, 0), self.gamelog_border, 5)
    self.gamelog_text.render()
    self.display.screen.blit(self.surface_gamelog, (0, 65))
    self.display.screen.blit(self.gamelog_text, (TEXT_PADDING, 65 + TEXT_PADDING))
    
    #self.black_card_text.render()
    #self.display.screen.blit(self.surface_black_card, (self.hmiddle - self.surface_black_card.get_width()/2, 50))
    #self.display.screen.blit(self.black_card_text, (self.hmiddle - self.card_surface.get_width()/2 + TEXT_PADDING, 50 + TEXT_PADDING))
    
    self.black_card.render()
    self.display.screen.blit(self.black_card, (self.black_card_x, self.black_card_y))
    
    
    #for i in range(10):
    #  self.cards[i]['surface'].fill((255, 255, 255))
    #  pygame.draw.rect(self.cards[i]['surface'], (0, 0, 0), self.card_border, 5)
    #  self.cards[i]['text'].render()
    #  self.surface_cards.blit(self.cards[i]['surface'], self.cards[i]['position'])
    
    for i in range(10):
      self.cards[i]['card'].render()
      self.display.screen.blit(self.cards[i]['card'], self.cards[i]['position'])
    
    #self.display.screen.blit(self.surface_cards, (self.hmiddle - self.surface_cards.get_width()/2, self.display_size[1] - self.surface_cards.get_height() - 50))

    #for i in range(10):
    #  self.display.screen.blit(self.cards[i]['text'], (
    #  self.hmiddle - self.surface_cards.get_width() / 2 +
    #  self.cards[i]['position'][0] + TEXT_PADDING,
    #  self.display_size[1] - self.surface_cards.get_height() - 50 +
    #  self.cards[i]['position'][1] + TEXT_PADDING))

    self.button_start_leave.render()
    self.button_confirm.render()

    self.player_indicators.render()
    
  
  def setMode(self, mode):
    self.mode = mode

    if mode != GAME_MODE_CZAR_DECIDING:
      self.player_indicators.setUnchosen()

    if mode == GAME_MODE_CZAR_WAITING or mode == GAME_MODE_PAUSED:
      self.button_confirm.setEnable(False)
      for i in range(10):
        if mode == GAME_MODE_PAUSED:
          self.clearCard(i)
        else:
          self.cards[i]['card'].setEnable(False)

      if mode == GAME_MODE_PAUSED:
        self.black_card.setEnable(False)
        self.black_card.setCard(None)
    else:
      self.button_confirm.setEnable(True)


  def generateCardLambda(self, index):
    return lambda: self.cardCallback(index)


  def cardCallback(self, i):

    if self.mode == GAME_MODE_CZAR_DECIDING:

      # if we're choosing a card which is already chosen, we will deselect it
      # if we choose a card which isn't chosen yet, we will deselect all other cards
      # and choose this one

      if self.cards[i]['card'].chosen:
        self.cards[i]['card'].toggleChosen()
      else:

        chosen_cards = [c['card'] for c in self.cards if c['card'].chosen]

        if len(chosen_cards)>0:
          for c in chosen_cards:
            c.toggleChosen()

        self.cards[i]['card'].toggleChosen()

    else:
      # we need to find the selected card, choose / unchoose it, and link/unlink it
      if self.cards[i]['card'].chosen:
        self.black_card.getCard().unlink(self.cards[i]['card'].getCard())
      else:
        try:
          self.black_card.getCard().link(self.cards[i]['card'].getCard())
        except CardLinkError:
          self.writeLog("you've already chosen enough cards. If you want to switch cards, you'll have to deselect another card first.")
          return
      self.black_card.setCard(self.black_card.getCard())
      self.cards[i]['card'].toggleChosen()

  def onConfirmChoice(self):

    cards = [c for c in self.cards if c['card'].chosen]

    if self.mode == GAME_MODE_CZAR_DECIDING:

      if len(cards) != 1:
        self.writeLog("You didn't select your favorite yet.")
        return

      self.display.factory.client.sendCzarDecision(cards[0]['card'].getCard().links)

    else:

      if len(cards) != self.black_card.getCard().placeholders:
        self.writeLog("You didn't select enough white cards yet.")
        return

      self.display.factory.client.sendChooseCards(self.black_card.getCard().links)

      for card in cards:
        self.clearCard(self.cards.index(card))

    for c in self.cards:
      c['card'].setEnable(False)
    self.button_confirm.setEnable(False)


  def clearCard(self, i):
    self.cards[i]['card'].setCard(None)
    self.cards[i]['card'].setLabel("selectable card %d"%(i+1))
    if self.cards[i]['card'].chosen:
      self.cards[i]['card'].toggleChosen()
