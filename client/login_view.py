import os.path

from shared.path import getScriptDirectory
from tools import *
from .view import View

SPACE_BETWEEN_LABEL_AND_INPUT = 20
TEXT_INPUT_WIDTH = 300



class LoginView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    font = display.getFont()
    font_welcome = pygame.font.Font(
      os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 30)
    font_note = pygame.font.Font(
      os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 14)
    size = display.getSize()
    
    # calc middle of screen
    hmiddle = size[0] / 2
    vmiddle = size[1] / 2
    
    # short form of constant
    space = SPACE_BETWEEN_LABEL_AND_INPUT / 2
    
    # short welcome text
    self.welcome_text = font_welcome.render(
      "Welcome to Cards Against Humanity Online!",
      1, (0, 0, 0))
    self.welcome_text_pos = (hmiddle - self.welcome_text.get_width() / 2, 100)
    
    # create labels and inputs for server, username and password
    self.server_label = font.render("Server:", 1, (0, 0, 0))
    self.uname_label = font.render("Username:", 1, (0, 0, 0))
    self.pword_label = font.render("Password:", 1, (0, 0, 0))
    
    # calc positions of labels and inputs (same y for label and input as they
    #  should be side by side, same x for all inputs as the should be exactly
    #  among each other)
    self.server_label_x = hmiddle - self.server_label.get_width() - space - 100
    self.server_y = vmiddle - 70
    self.uname_label_x = hmiddle - self.uname_label.get_width() - space - 100
    self.uname_y = self.server_y + 70
    self.pword_label_x = hmiddle - self.pword_label.get_width() - space - 100
    self.pword_y = self.uname_y + 35
    self.input_x = hmiddle + space - 100
    
    # create text inputs with positions
    self.server_input = TextInput(display, font, (self.input_x, self.server_y),
                                  TEXT_INPUT_WIDTH, 'Server address')
    self.server_input.input.input_string = self.display.server_name
    self.uname_input = TextInput(display, font, (self.input_x, self.uname_y),
                                 TEXT_INPUT_WIDTH, 'Username')
    self.uname_input.input.input_string = self.display.login_name
    self.pword_input = TextInput(display, font, (self.input_x, self.pword_y),
                                 TEXT_INPUT_WIDTH, 'Password', True)
    self.pword_input.input.input_string = self.display.login_password
    
    # note for first login/create account
    self.login_note = font_note.render(
      "NOTE: If username won't be found a new account will be created with "
      "the entered password!",
      1, (224, 0, 0))
    
    self.login_note_x = hmiddle - self.login_note.get_width() / 2
    self.login_note_y = self.pword_y + 50
    
    # buttons connect and close (dummy positions, for auto-determine width
    # and height)
    self.button_connect = Button(self.display, "Connect", font,
                                 (hmiddle - 100, vmiddle + 100))
    # now calc position with own width
    self.button_connect.setPosition((hmiddle - self.button_connect.getWidth()
                                     - space, vmiddle + 150))
    self.button_connect.setCallback(self.onConnect)
    self.button_connect.setEnable(False)
    self.button_close = Button(self.display, "Close", font,
                               (hmiddle, vmiddle + 150))
    
    self.button_close.setCallback(self.onClose)
    
    self.tab_order = [self.server_input, self.uname_input, self.pword_input,
                      self.button_connect, self.button_close]
  
  
  def handleEvent(self, event):
    View.handleEvent(self, event)
    self.server_input.handleEvent(event)
    self.uname_input.handleEvent(event)
    self.pword_input.handleEvent(event)
    
    self.button_connect.handleEvent(event)
    self.button_close.handleEvent(event)
  
  
  def render(self):
    # blit texts and labels on screen
    self.display.screen.blit(self.welcome_text, self.welcome_text_pos)
    self.display.screen.blit(self.server_label,
                             (self.server_label_x, self.server_y))
    self.display.screen.blit(self.uname_label,
                             (self.uname_label_x, self.uname_y))
    self.display.screen.blit(self.pword_label,
                             (self.pword_label_x, self.pword_y))
    
    # render text inputs
    self.server_input.render()
    self.uname_input.render()
    self.pword_input.render()
    
    # first login note
    self.display.screen.blit(self.login_note,
                             (self.login_note_x, self.login_note_y))
    
    # draw buttons
    self.button_connect.render()
    self.button_close.render()
  
  
  def update(self):
    View.update(self)
    self.server_input.update()
    self.uname_input.update()
    self.pword_input.update()
    if self.server_input.input.get_text() == '' or \
                    self.uname_input.input.get_text() == '' or \
                    self.pword_input.input.get_text() == '' or \
                    len(self.uname_input.input.get_text())<6 or \
                    len(self.uname_input.input.get_text())>30:
      self.button_connect.setEnable(False)
    else:
      self.button_connect.setEnable(True)
  
  
  def firstUpdate(self):
    self.speak("Welcome to Cards Against Humanity Online")
    View.firstUpdate(self)
  
  
  def onClose(self):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
  
  
  def onConnect(self):
    self.display.setView('ConnectionView')
    self.display.callFunction('self.view.connectingMessage', self.server_input.input.get_text())
    self.display.callFunction('self.connect', self.server_input.input.get_text(),
                         self.uname_input.input.get_text(),
                         self.pword_input.input.get_text())
