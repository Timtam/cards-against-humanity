from .view import View
import text_input
import pygame

SPACE_BETWEEN_LABEL_AND_INPUT= 20
PADDING_RECT_TEXT = 5



class InitialView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    font = display.getFont()
    
    #calc middle of screen
    self.hmiddle = display.getSize()[0]/2
    self.vmiddle = display.getSize()[1]/2
    
    # short form of constants
    space = SPACE_BETWEEN_LABEL_AND_INPUT/2
    padding = PADDING_RECT_TEXT
    
    # short(! or we have to wrap it and that's not easy...) welcome text
    self.welcome_text = font.render("Welcome to Cards Against Humanity Online!", 1, (0, 0, 0))
    self.welcome_text_pos = (self.hmiddle - self.welcome_text.get_width()/2, 100)
    
    # create labels and inputs
    self.uname_label = font.render("Username:", 1, (0, 0, 0))
    self.pword_label = font.render("Password:", 1, (0, 0, 0))
    self.uname_input = text_input.TextInput(font)
    self.pword_input = text_input.TextInput(font)
    
    # calc their positions (same y for label and input as they should be side by side)
    self.uname_label_x = self.hmiddle - self.uname_label.get_width() - space
    self.uname_input_x = self.hmiddle + space + padding
    self.uname_y = self.vmiddle - 100
    self.pword_label_x = self.hmiddle - self.pword_label.get_width() - space
    self.pword_input_x = self.hmiddle + space + padding
    self.pword_y = self.vmiddle -  50

    # rectangles around the input texts (x, y, width, height)
    self.uname_input_rect = (self.hmiddle + space, self.uname_y - padding, 300, self.uname_label.get_height() + 2 * padding)
    self.pword_input_rect = (self.hmiddle + space, self.pword_y - padding, 300, self.pword_label.get_height() + 2 * padding)


  def handleEvent(self, event):
    self.uname_input.update(event)
    self.pword_input.update(event)
    
    
  def render(self):
    # get surfaces of input texts
    username_input = self.uname_input.get_surface()
    password_input = self.pword_input.get_surface()
    
    self.display.screen.blit(self.welcome_text, self.welcome_text_pos)
    
    # blit labels and input on screen
    self.display.screen.blit(self.uname_label, (self.uname_label_x, self.uname_y))
    self.display.screen.blit(username_input, (self.uname_input_x, self.uname_y))
    self.display.screen.blit(self.pword_label, (self.pword_label_x, self.pword_y))
    self.display.screen.blit(password_input, (self.pword_input_x, self.pword_y))

    # draw the input rectangles
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.uname_input_rect, 1)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.pword_input_rect, 1)
