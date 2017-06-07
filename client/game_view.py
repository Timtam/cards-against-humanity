from shared.card import CARD_BLACK, CARD_WHITE
from .view import View
from .tools import Button
from .scrolled_text_panel import ScrolledTextPanel
from card_surface import CardSurface

import pygame
import pygame.locals as pl

CARD_PADDING = 10
TEXT_PADDING = 10
CARD_SIZE = (150, 200)



class GameView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    self.display_size = self.display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.font = self.display.getFont()
    
    self.button_start_leave = Button(self.display, "Start Game", self.font, (self.display_size[0] * 0.85, self.display_size[1] * 0.5))
    self.button_start_leave.setCallback(self.onStartLeave)
    self.button_confirm = Button(self.display, "Confirm Choice", self.font, (self.display_size[0] * 0.85, self.display_size[1] * 0.6))
    
    self.surface_gamelog = pygame.Surface((200, self.display_size[1]))
    self.gamelog_border = pygame.Rect(0, 0, self.surface_gamelog.get_width(), self.surface_gamelog.get_height())
    self.gamelog_text = ScrolledTextPanel(self.display, TEXT_PADDING, TEXT_PADDING, self.surface_gamelog.get_width() - 2*TEXT_PADDING, self.surface_gamelog.get_height() - 2*TEXT_PADDING)
    self.writeLog('you joined the game')
    self.gamelog_text.setLabel('game log')

    self.cards = []

    self.tab_order = [self.button_start_leave, self.button_confirm, self.gamelog_text]
    self.createCardSurfaces()
    
    
  def createCardSurfaces(self):
    #self.surface_cards = pygame.Surface((self.display_size[0] * 0.6, self.display_size[1] * 0.5))
    #self.surface_cards = pygame.Surface((CARD_SIZE[0] * 5 + CARD_PADDING * 6, CARD_SIZE[1] * 2 + CARD_PADDING * 3))
    #self.card_border = pygame.Rect(0, 0, (self.surface_cards.get_width() - 6 * CARD_PADDING) / 5, (self.surface_cards.get_height() - 3 * CARD_PADDING) / 2)

    #self.card_surface = pygame.Surface(((
    #                               self.surface_cards.get_width() - 6 *
    #                               CARD_PADDING) / 5,
    #                               (
    #                               self.surface_cards.get_height() - 3 *
    #                               CARD_PADDING) / 2))
    
    #self.surface_black_card = pygame.Surface((self.card_surface.get_width(), self.card_surface.get_height()))
    self.black_card_x = self.hmiddle - CARD_SIZE[0]/2
    self.black_card_y = 50
    self.black_card = CardSurface(self.display, self.black_card_x, self.black_card_y, CARD_SIZE[0], CARD_SIZE[1], CARD_BLACK)
    #self.black_card_text = ScrolledTextPanel(self.display, TEXT_PADDING, TEXT_PADDING, self.card_surface.get_width() - 2*TEXT_PADDING, self.card_surface.get_height() - 2*TEXT_PADDING, (0, 0, 0))
    self.black_card.addText('no black card', (255, 255, 255))
    self.black_card.setLabel('black card')
    #self.black_card = None

    self.tab_order.append(self.black_card)

    for i in range(10):
      #card_position = ((i * (CARD_SIZE[0] + CARD_PADDING)) - (int(i / 5) * (self.surface_cards.get_width() - CARD_PADDING)) + CARD_PADDING,
      #                 int(i / 5) * (CARD_SIZE[1] + CARD_PADDING) + CARD_PADDING)
      #
      card_position = ((i * (CARD_SIZE[0] + CARD_PADDING)) - (int(i / 5) * (CARD_SIZE[0] * 5 + CARD_PADDING * 5)) + self.hmiddle - (CARD_SIZE[0] * 5 + CARD_PADDING * 4)/2,
                       int(i / 5) * (CARD_SIZE[1] + CARD_PADDING) + 300)
      self.cards.append({
        # we need to copy the surface, otherwise we will have the same
        # printed on every surface
        #'surface': self.card_surface.copy(),
        'card': CardSurface(self.display, card_position[0], card_position[1], CARD_SIZE[0], CARD_SIZE[1]),
        'position': card_position,
        #'text': None,
        #'card': None
      })
      #self.cards[i]['text']=ScrolledTextPanel(self.display, TEXT_PADDING, TEXT_PADDING, self.card_surface.get_width() - 2 * TEXT_PADDING, self.card_surface.get_height() - 2 * TEXT_PADDING)
      #self.cards[i]['text'].addText('no card')
      self.cards[i]['card'].addText('no card')
      #self.cards[i]['text'].setLabel('white card %d'%(i+1))
      self.cards[i]['card'].setLabel('white card %d' % (i + 1))
      #self.cards[i]['text'].setSpeakLines(False)
      self.cards[i]['card'].setSpeakLines(False)
      #self.tab_order.append(self.cards[i]['text'])
      self.tab_order.append(self.cards[i]['card'])
  
  
  def setCards(self, *cards):
    j = 0
    for i in range(10):
      if j >= len(cards):
        return
      if self.cards[i]['card'].getCard() is None:
        #self.cards[i]['card'] = cards[j]
        #self.cards[i]['card'].clearText()
        #self.cards[i]['card'].addText(cards[j].getCardText())
        self.cards[i]['card'].setCard(cards[j])
        j += 1

    if j < len(cards):
      self.log.warn('{count} cards remaining, but no place left', count = len(cards)-j)
  
  
  def setBlackCard(self, card):
    self.black_card.setCard(card)
  
  
  def writeLog(self, text):
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
  
  
  def render(self):
    #self.surface_cards.fill((255, 255, 255))
    #self.surface_black_card.fill((0, 0, 0))
    self.surface_gamelog.fill((255, 255, 255))
    
    pygame.draw.rect(self.surface_gamelog, (0, 0, 0), self.gamelog_border, 5)
    self.gamelog_text.render()
    self.display.screen.blit(self.surface_gamelog, (0, 0))
    self.display.screen.blit(self.gamelog_text, (TEXT_PADDING, TEXT_PADDING))
    
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
