from tools import *
from .view import View

SPACE_BETWEEN_LABEL_AND_INPUT = 20
TEXT_INPUT_WIDTH = 300



class InitialView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    font = display.getFont()
    size = display.getSize()
    
    # calc middle of screen
    hmiddle = size[0] / 2
    vmiddle = size[1] / 2
    
    # short form of constant
    space = SPACE_BETWEEN_LABEL_AND_INPUT / 2
    
    # short (! or we have to wrap it and that's not easy...) welcome text
    self.welcome_text = font.render("Welcome to Cards Against Humanity Online!",
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
    self.uname_y = vmiddle + 0
    self.pword_label_x = hmiddle - self.pword_label.get_width() - space - 100
    self.pword_y = vmiddle + 35
    self.input_x = hmiddle + space - 100
    
    # create text inputs with positions
    self.server_input = TextInput(display, font, (self.input_x, self.server_y),
                                  TEXT_INPUT_WIDTH, 'Server address')
    self.uname_input = TextInput(display, font, (self.input_x, self.uname_y),
                                 TEXT_INPUT_WIDTH, 'Username')
    self.pword_input = TextInput(display, font, (self.input_x, self.pword_y),
                                 TEXT_INPUT_WIDTH, 'Password')
    
    # buttons connect and close (dummy positions, for auto-determine width
    # and height)
    self.button_connect = Button(self.display, "Connect", font, (0, 0, 0),
                                 (hmiddle - 100, vmiddle + 100))
    # now calc position with own width
    self.button_connect.setPosition((hmiddle - self.button_connect.getWidth()
                                     - space, vmiddle + 150))
    self.button_close = Button(self.display, "Close", font, (0, 0, 0),
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
    
    # draw buttons
    self.button_connect.render()
    self.button_close.render()
  
  
  def update(self):
    View.update(self)
    self.server_input.update()
    self.uname_input.update()
    self.pword_input.update()
  
  
  def firstUpdate(self):
    self.speak("Welcome to Cards Against Humanity Online")
    self.display.start_sound.play()
    View.firstUpdate(self)
  
  
  def onClose(self):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
