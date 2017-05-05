import text_input
from tools import *
from .view import View

SPACE_BETWEEN_LABEL_AND_INPUT = 20
PADDING_RECT_TEXT = 5
TEXT_INPUT_LEN = 300



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
    
    # short (! or we have to wrap it and that's not easy...) welcome text
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
    self.server_label_x = hmiddle - self.server_label.get_width() - space - 100
    self.server_y = vmiddle - 70
    self.uname_label_x = hmiddle - self.uname_label.get_width() - space - 100
    self.uname_y = vmiddle + 0
    self.pword_label_x = hmiddle - self.pword_label.get_width() - space - 100
    self.pword_y = vmiddle + 35
    self.input_x = hmiddle + space + self.padding - 100
    
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
    
    # buttons connect and close
    self.button_connect = Button(self.display.screen, "Connect", font,
                                 (0, 0, 0), hmiddle - 100,
                                 vmiddle + 100)  # dummy positions,
    # for auto-deetermine width and height
    self.button_connect.setPosition(
      hmiddle - self.button_connect.getWidth() - space,
      vmiddle + 150)  # calc position with own width
    self.button_close = Button(self.display.screen, "Close", font, (0, 0, 0),
                               hmiddle, vmiddle + 150)
  
  
  def handleEvent(self, event):
    self.server_input.handleEvent(event)
    self.uname_input.handleEvent(event)
    self.pword_input.handleEvent(event)
    
    self.button_connect.handleEvent(event)
    self.button_close.handleEvent(event)
  
  
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
    
    # draw buttons
    self.button_connect.render()
    self.button_close.render()
  
  
  def update(self):
    self.server_input.update()
    self.uname_input.update()
    self.pword_input.update()
