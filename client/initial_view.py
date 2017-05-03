import pygame

import text_input
from .view import View

SPACE_BETWEEN_LABEL_AND_INPUT = 20
PADDING_RECT_TEXT = 5
TEXT_INPUT_LEN = 300

COLOR_BUTTON = (128, 128, 128)
COLOR_BUTTON_HOVER = (100, 100, 100)



class InitialView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    font = display.getFont()
    size = display.getSize()
    
    # calc middle of screen
    hmiddle = size[0] / 2
    vmiddle = size[1] / 2
    
    # short form of constants
    space = SPACE_BETWEEN_LABEL_AND_INPUT / 2
    self.padding = PADDING_RECT_TEXT
    
    self.color_but_connect = self.color_but_close = COLOR_BUTTON
    
    # short(! or we have to wrap it and that's not easy...) welcome text
    self.welcome_text = font.render("Welcome to Cards Against Humanity Online!",
                                    1, (0, 0, 0))
    self.welcome_text_pos = (hmiddle - self.welcome_text.get_width() / 2, 100)
    
    # create labels and inputs for server, username and password
    self.server_label = font.render("Server:", 1, (0, 0, 0))
    self.uname_label = font.render("Username:", 1, (0, 0, 0))
    self.pword_label = font.render("Password:", 1, (0, 0, 0))
    self.server_input = text_input.TextInput(font)
    self.uname_input = text_input.TextInput(font)
    self.pword_input = text_input.TextInput(font)
    
    # calc their positions (same y for label and input as they should be side
    #  by side, same x for all inputs as the should be exactly among each other)
    self.server_label_x = hmiddle - self.server_label.get_width() - space
    self.server_y = vmiddle - size[1] * 0.1
    self.uname_label_x = hmiddle - self.uname_label.get_width() - space
    self.uname_y = vmiddle + size[1] * 0.0
    self.pword_label_x = hmiddle - self.pword_label.get_width() - space
    self.pword_y = vmiddle + size[1] * 0.06
    self.input_x = hmiddle + space + self.padding
    
    # button texts
    self.button_connect_text = font.render("Connect", 1, (0, 0, 0))
    self.button_close_text = font.render("Close", 1, (0, 0, 0))
    
    # button positions
    self.button_connect_x = hmiddle - self.button_connect_text.get_width() - \
                            space
    self.button_close_x = hmiddle + space
    self.button_y = size[1] * 0.8
    
    # button rectangle positions
    self.but_connect_rect_x = self.button_connect_x - self.padding
    self.but_connect_rect_w = self.button_connect_text.get_width() + 2 * \
                                                                     self.padding
    self.but_connect_rect_h = self.button_connect_text.get_height() + 1.5 * \
                                                                      self.padding
    
    self.but_close_rect_x = self.button_close_x - self.padding
    self.but_close_rect_w = self.button_close_text.get_width() + 2 * \
                                                                 self.padding
    self.but_close_rect_h = self.button_close_text.get_height() + 1.5 * \
                                                                  self.padding
    self.but_rect_y = self.button_y - self.padding
    
    self.but_connect_rect_x_end = self.but_connect_rect_x + \
                                  self.but_connect_rect_w
    self.but_connect_rect_y_end = self.but_rect_y + self.but_connect_rect_h
    self.but_close_rect_x_end = self.but_close_rect_x + self.but_close_rect_w
    self.but_close_rect_y_end = self.but_rect_y + self.but_close_rect_h
    
    # rectangles around the input texts (x, y, width, height)
    self.server_input_rect = (
      self.input_x - self.padding, self.server_y - self.padding, TEXT_INPUT_LEN,
      self.server_label.get_height() + 2 * self.padding)
    self.uname_input_rect = (
      self.input_x - self.padding, self.uname_y - self.padding, TEXT_INPUT_LEN,
      self.uname_label.get_height() + 2 * self.padding)
    self.pword_input_rect = (
      self.input_x - self.padding, self.pword_y - self.padding, TEXT_INPUT_LEN,
      self.pword_label.get_height() + 2 * self.padding)
    
    # button rectangles
    self.button_connect_rect = (
      self.but_connect_rect_x, self.but_rect_y, self.but_connect_rect_w,
      self.but_connect_rect_h)
    self.button_close_rect = (
      self.but_close_rect_x, self.but_rect_y, self.but_close_rect_w,
      self.but_close_rect_h)
  
  
  def handleEvent(self, event):
    self.server_input.handleEvent(event)
    self.uname_input.handleEvent(event)
    self.pword_input.handleEvent(event)
    
    if event.type == pygame.MOUSEMOTION:
      mouse = pygame.mouse.get_pos()
      # hover over buttons
      if self.but_connect_rect_x < mouse[
        0] < self.but_connect_rect_x_end and self.but_rect_y < mouse[
        1] < self.but_connect_rect_y_end:
        self.color_but_connect = COLOR_BUTTON_HOVER
      else:
        self.color_but_connect = COLOR_BUTTON
      if self.but_close_rect_x < mouse[
        0] < self.but_close_rect_x_end and self.but_rect_y < mouse[
        1] < self.but_close_rect_y_end:
        self.color_but_close = COLOR_BUTTON_HOVER
      else:
        self.color_but_close = COLOR_BUTTON
  
  
  def render(self):
    # get surfaces of input texts
    server_input = self.server_input.render()
    username_input = self.uname_input.render()
    password_input = self.pword_input.render()
    
    self.display.screen.blit(self.welcome_text, self.welcome_text_pos)
    
    # blit labels and input on screen
    self.display.screen.blit(self.server_label,
                             (self.server_label_x, self.server_y))
    self.display.screen.blit(server_input, (self.input_x, self.server_y))
    self.display.screen.blit(self.uname_label,
                             (self.uname_label_x, self.uname_y))
    self.display.screen.blit(username_input, (self.input_x, self.uname_y))
    self.display.screen.blit(self.pword_label,
                             (self.pword_label_x, self.pword_y))
    self.display.screen.blit(password_input, (self.input_x, self.pword_y))
    
    # draw the input rectangles
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.server_input_rect, 1)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.uname_input_rect, 1)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.pword_input_rect, 1)
    
    # draw button rectangles
    pygame.draw.rect(self.display.screen, self.color_but_connect,
                     self.button_connect_rect, 0)
    pygame.draw.rect(self.display.screen, self.color_but_close,
                     self.button_close_rect, 0)
    
    # button texts
    self.display.screen.blit(self.button_connect_text,
                             (self.button_connect_x, self.button_y))
    self.display.screen.blit(self.button_close_text,
                             (self.button_close_x, self.button_y))
  
  
  def update(self):
    self.server_input.update()
    self.uname_input.update()
    self.pword_input.update()
