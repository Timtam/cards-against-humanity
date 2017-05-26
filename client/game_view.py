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
    
    self.button_start_leave = Button(self.display, "Start Game", self.font, (self.display_size[0] * 0.8, self.display_size[1] * 0.5))
    self.button_start_leave.setCallback(self.onStartLeave)
    self.button_confirm = Button(self.display, "Confirm Choice", self.font, (self.display_size[0] * 0.8, self.display_size[1] * 0.6))
    
    self.surface_gamelog = pygame.Surface((300, self.display_size[1]))
    self.gamelog_border = pygame.Rect(0, 0, self.surface_gamelog.get_width(), self.surface_gamelog.get_height())
    self.gamelog_text = ScrolledTextPanel(self.display.screen, 2*TEXT_PADDING, 2*TEXT_PADDING, self.surface_gamelog.get_width() - 4*TEXT_PADDING, self.surface_gamelog.get_height() - 4*TEXT_PADDING)
    self.writeLog('you joined the game')
    self.gamelog_text.setLabel('game log')

    self.cards = []

    self.tab_order = [self.button_start_leave, self.button_confirm, self.gamelog_text]
    self.createCardSurfaces()
    
    
  def createCardSurfaces(self):
    self.surface_cards = pygame.Surface((self.display_size[0] * 0.5, self.display_size[1] * 0.5))
    self.card_border = pygame.Rect(0, 0, (self.surface_cards.get_width() - 6 * CARD_PADDING) / 5, (self.surface_cards.get_height() - 3 * CARD_PADDING) / 2)

    card_surface = pygame.Surface(((
                                   self.surface_cards.get_width() - 6 *
                                   CARD_PADDING) / 5,
                                   (
                                   self.surface_cards.get_height() - 3 *
                                   CARD_PADDING) / 2))
    
    self.surface_black_card = pygame.Surface((card_surface.get_width(), card_surface.get_height()))
    self.black_card_text = ScrolledTextPanel(self.surface_black_card, TEXT_PADDING, TEXT_PADDING, self.surface_black_card.get_width() - 2*TEXT_PADDING, self.surface_black_card.get_height() - 2*TEXT_PADDING)
    self.black_card_text.addText('no black card')
    self.black_card_text.setLabel('black card')
    self.black_card = None
    
    for i in range(10):
      card_position = ((i * (card_surface.get_width() + CARD_PADDING)) - (
      int(i / 5) * (
      self.surface_cards.get_width() - CARD_PADDING)) + CARD_PADDING,
                       int(i / 5) * (
                       card_surface.get_height() + CARD_PADDING) + CARD_PADDING)
      self.cards.append({
        # we need to copy the surface, otherwise we will have the same
        # printed on every surface
        'surface': card_surface.copy(),
        'position': card_position,
        'text': None,
        'card': None
      })
      self.cards[i]['text']=ScrolledTextPanel(self.cards[i]['surface'], TEXT_PADDING, TEXT_PADDING, self.surface_black_card.get_width() - 2 * TEXT_PADDING, self.surface_black_card.get_height() - 2 * TEXT_PADDING)
      self.cards[i]['text'].addText('no card')
      self.cards[i]['text'].setLabel('white card %d'%(i+1))
      self.cards[i]['text'].setSpeakLines(False)
      self.tab_order.append(self.cards[i]['text'])

    self.tab_order.append(self.black_card_text)
  
  def setCards(self, *cards):
    for i in range(10):
      if len(cards)==0:
        return
      if not self.cards[i]['card']:
        self.cards[i]['card'] = cards[0]
        self.cards[i]['text'].clearText()
        self.cards[i]['text'].addText(cards[0].getCardText())
        del cards[0]

    if len(cards)>0:
      self.log.warn('{count} cards remaining, but no place left', count = len(cards))

  def setBlackCard(self, card):
    self.black_card_text.clear()
    self.black_card_text.addText(card.getCardText())
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
      self.cards[i]['text'].handleEvent(event, self.display)
    self.black_card_text.handleEvent(event, self.display)
    self.gamelog_text.handleEvent(event, self.display)
  
  
  def update(self):
    View.update(self)
  
  
  def render(self):
    self.surface_cards.fill((255, 255, 255))
    self.surface_black_card.fill((0, 0, 0))
    self.surface_gamelog.fill((255, 255, 255))
    
    pygame.draw.rect(self.surface_gamelog, (0, 0, 0), self.gamelog_border, 5)
    self.display.screen.blit(self.surface_gamelog, (0, 0))
    
    self.display.screen.blit(self.surface_black_card, (self.hmiddle - self.surface_black_card.get_width()/2, 50))
    
    for i in range(10):
      self.cards[i]['surface'].fill((255, 255, 255))
      pygame.draw.rect(self.cards[i]['surface'], (0, 0, 0), self.card_border, 5)
      self.cards[i]['text'].render()
      self.surface_cards.blit(self.cards[i]['surface'], self.cards[i]['position'])
    
    self.display.screen.blit(self.surface_cards, (self.hmiddle - self.surface_cards.get_width()/2, self.display_size[1] - self.surface_cards.get_height() - 50))

    self.button_start_leave.render()
    self.button_confirm.render()
