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
    
    # create labels and inputs for server, username and password
    self.server_label = font.render("Server:", 1, (0, 0, 0))
    self.uname_label = font.render("Username:", 1, (0, 0, 0))
    self.pword_label = font.render("Password:", 1, (0, 0, 0))
    self.server_input = text_input.TextInput(font)
    self.uname_input = text_input.TextInput(font)
    self.pword_input = text_input.TextInput(font)
    
    # calc their positions (same y for label and input as they should be side by side)
    self.server_label_x = self.hmiddle - self.server_label.get_width() - space
    self.server_input_x = self.hmiddle + space + padding
    self.server_y = self.vmiddle - 50
    self.uname_label_x = self.hmiddle - self.uname_label.get_width() - space
    self.uname_input_x = self.hmiddle + space + padding
    self.uname_y = self.vmiddle + 50
    self.pword_label_x = self.hmiddle - self.pword_label.get_width() - space
    self.pword_input_x = self.hmiddle + space + padding
    self.pword_y = self.vmiddle + 100

    # rectangles around the input texts (x, y, width, height)
    self.server_input_rect = (self.hmiddle + space, self.server_y - padding, 300, self.server_label.get_height() + 2 * padding)
    self.uname_input_rect = (self.hmiddle + space, self.uname_y - padding, 300, self.uname_label.get_height() + 2 * padding)
    self.pword_input_rect = (self.hmiddle + space, self.pword_y - padding, 300, self.pword_label.get_height() + 2 * padding)


  def handleEvent(self, event):
    self.server_input.handleEvent(event)
    self.uname_input.handleEvent(event)
    self.pword_input.handleEvent(event)
    
  def render(self):
    # get surfaces of input texts
    server_input   = self.server_input.render()
    username_input = self.uname_input.render()
    password_input = self.pword_input.render()
    
    self.display.screen.blit(self.welcome_text, self.welcome_text_pos)
    
    # blit labels and input on screen
    self.display.screen.blit(self.server_label, (self.server_label_x, self.server_y))
    self.display.screen.blit(server_input, (self.server_input_x, self.server_y))
    self.display.screen.blit(self.uname_label, (self.uname_label_x, self.uname_y))
    self.display.screen.blit(username_input, (self.uname_input_x, self.uname_y))
    self.display.screen.blit(self.pword_label, (self.pword_label_x, self.pword_y))
    self.display.screen.blit(password_input, (self.pword_input_x, self.pword_y))

    # draw the input rectangles
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.server_input_rect, 1)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.uname_input_rect, 1)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.pword_input_rect, 1)

  def update(self):
    self.server_input.update()
    self.uname_input.update()
    self.pword_input.update()
