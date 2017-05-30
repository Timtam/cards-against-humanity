from .view import View
from .tools import Button
from .scrolled_text_panel import ScrolledTextPanel

import pygame

CARD_PADDING = 10
TEXT_PADDING = 10



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
    self.surface_cards = pygame.Surface((self.display_size[0] * 0.6, self.display_size[1] * 0.5))
    self.card_border = pygame.Rect(0, 0, (self.surface_cards.get_width() - 6 * CARD_PADDING) / 5, (self.surface_cards.get_height() - 3 * CARD_PADDING) / 2)

    self.card_surface = pygame.Surface(((
                                   self.surface_cards.get_width() - 6 *
                                   CARD_PADDING) / 5,
                                   (
                                   self.surface_cards.get_height() - 3 *
                                   CARD_PADDING) / 2))
    
    self.surface_black_card = pygame.Surface((self.card_surface.get_width(), self.card_surface.get_height()))
    self.black_card_text = ScrolledTextPanel(self.display, TEXT_PADDING, TEXT_PADDING, self.card_surface.get_width() - 2*TEXT_PADDING, self.card_surface.get_height() - 2*TEXT_PADDING, (0, 0, 0))
    self.black_card_text.addText('no black card', (255, 255, 255))
    self.black_card_text.setLabel('black card')
    self.black_card = None
    
    for i in range(10):
      card_position = ((i * (self.card_surface.get_width() + CARD_PADDING)) - (
      int(i / 5) * (
      self.surface_cards.get_width() - CARD_PADDING)) + CARD_PADDING,
                       int(i / 5) * (
                       self.card_surface.get_height() + CARD_PADDING) + CARD_PADDING)
      self.cards.append({
        # we need to copy the surface, otherwise we will have the same
        # printed on every surface
        'surface': self.card_surface.copy(),
        'position': card_position,
        'text': None,
        'card': None
      })
      self.cards[i]['text']=ScrolledTextPanel(self.display, TEXT_PADDING, TEXT_PADDING, self.card_surface.get_width() - 2 * TEXT_PADDING, self.card_surface.get_height() - 2 * TEXT_PADDING)
      self.cards[i]['text'].addText('no card')
      self.cards[i]['text'].setLabel('white card %d'%(i+1))
      self.cards[i]['text'].setSpeakLines(False)
      self.tab_order.append(self.cards[i]['text'])

    self.tab_order.append(self.black_card_text)
  
  def setCards(self, *cards):
    j = 0
    for i in range(10):
      if j >= len(cards):
        return
      if not self.cards[i]['card']:
        self.cards[i]['card'] = cards[j]
        self.cards[i]['text'].clearText()
        self.cards[i]['text'].addText(cards[j].getCardText())
        j += 1

    if j < len(cards):
      self.log.warn('{count} cards remaining, but no place left', count = len(cards)-j)

  def setBlackCard(self, card):
    self.black_card_text.clearText()
    self.black_card_text.addText(card.getCardText(), (255, 255, 255))
    self.black_card = card

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
      self.cards[i]['text'].handleEvent(event)
    self.black_card_text.handleEvent(event)
    self.gamelog_text.handleEvent(event)
  
  
  def update(self):
    View.update(self)
  
  
  def render(self):
    self.surface_cards.fill((255, 255, 255))
    self.surface_black_card.fill((0, 0, 0))
    self.surface_gamelog.fill((255, 255, 255))

    pygame.draw.rect(self.surface_gamelog, (0, 0, 0), self.gamelog_border, 5)
    self.gamelog_text.render()
    self.display.screen.blit(self.surface_gamelog, (0, 0))
    self.display.screen.blit(self.gamelog_text, (TEXT_PADDING, TEXT_PADDING))
    
    self.black_card_text.render()
    self.display.screen.blit(self.surface_black_card, (self.hmiddle - self.surface_black_card.get_width()/2, 50))
    self.display.screen.blit(self.black_card_text, (self.hmiddle - self.card_surface.get_width()/2 + TEXT_PADDING, 50 + TEXT_PADDING))
    
    for i in range(10):
      self.cards[i]['surface'].fill((255, 255, 255))
      pygame.draw.rect(self.cards[i]['surface'], (0, 0, 0), self.card_border, 5)
      self.cards[i]['text'].render()
      self.surface_cards.blit(self.cards[i]['surface'], self.cards[i]['position'])
    
    self.display.screen.blit(self.surface_cards, (self.hmiddle - self.surface_cards.get_width()/2, self.display_size[1] - self.surface_cards.get_height() - 50))

    for i in range(10):
      self.display.screen.blit(self.cards[i]['text'], (
      self.hmiddle - self.surface_cards.get_width() / 2 +
      self.cards[i]['position'][0] + TEXT_PADDING,
      self.display_size[1] - self.surface_cards.get_height() - 50 +
      self.cards[i]['position'][1] + TEXT_PADDING))

    self.button_start_leave.render()
    self.button_confirm.render()
