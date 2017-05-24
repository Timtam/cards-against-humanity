from .view import View
from .tools import Button
from .scrolled_text_panel import ScrolledTextPanel

import pygame

CARD_PADDING = 10
TEXT_PADDING = 10



class GameView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    self.display = display
    self.display_size = self.display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.font = self.display.getFont()
    
    self.button_start_leave = Button(self.display, "Start Game", self.font, (self.display_size[0] * 0.8, self.display_size[1] * 0.5))
    self.button_confirm = Button(self.display, "Confirm Choice", self.font, (self.display_size[0] * 0.8, self.display_size[1] * 0.6))
    
    self.surface_gamelog = pygame.Surface((300, self.display_size[1]))
    self.gamelog_border = pygame.Rect(0, 0, self.surface_gamelog.get_width(), self.surface_gamelog.get_height())
    self.gamelog_text = ScrolledTextPanel(self.display.screen, 2*TEXT_PADDING, 2*TEXT_PADDING, self.surface_gamelog.get_width() - 4*TEXT_PADDING, self.surface_gamelog.get_height() - 4*TEXT_PADDING)
    
    self.card_surfaces = []
    self.card_positions = []
    self.card_texts = []
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
    
    for i in range(0, 10, 1):
      self.card_surfaces.append(card_surface)
      card_position = ((i * (card_surface.get_width() + CARD_PADDING)) - (
      int(i / 5) * (
      self.surface_cards.get_width() - CARD_PADDING)) + CARD_PADDING,
                       int(i / 5) * (
                       card_surface.get_height() + CARD_PADDING) + CARD_PADDING)
      self.card_positions.append(card_position)


  def setCardTexts(self, cards):
    for i in range(0, 10, 1):
      if cards[i] is not None:
        card_text = ScrolledTextPanel(self.card_surfaces[i], TEXT_PADDING, TEXT_PADDING, self.surface_black_card.get_width() - 2 * TEXT_PADDING, self.surface_black_card.get_height() - 2 * TEXT_PADDING)
        card_text.addText(cards[i].text)
        self.card_texts.append(card_text)
  

  def handleEvent(self, event):
    self.button_start_leave.handleEvent(event)
    self.button_confirm.handleEvent(event)
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.surface_cards.fill((255, 255, 255))
    self.surface_black_card.fill((0, 0, 0))
    self.surface_gamelog.fill((255, 255, 255))
    
    pygame.draw.rect(self.surface_gamelog, (0, 0, 0), self.gamelog_border, 5)
    self.display.screen.blit(self.surface_gamelog, (0, 0))
    
    self.display.screen.blit(self.surface_black_card, (self.hmiddle - self.surface_black_card.get_width()/2, 50))
    
    for i in range(0, 10, 1):
      self.card_surfaces[i].fill((255, 255, 255))
      pygame.draw.rect(self.card_surfaces[i], (0, 0, 0), self.card_border, 5)
      #self.card_texts[i].render()
      self.surface_cards.blit(self.card_surfaces[i], self.card_positions[i])
    
    self.display.screen.blit(self.surface_cards, (self.hmiddle - self.surface_cards.get_width()/2, self.display_size[1] - self.surface_cards.get_height() - 50))

    self.button_start_leave.render()
    self.button_confirm.render()
