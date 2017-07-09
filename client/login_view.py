from .tools import *
from .message_view import MessageView
from .scrolled_panel import ScrolledPanel
from .language_entry import LanguageEntry

SPACE_BETWEEN_LABEL_AND_INPUT = 20
TEXT_INPUT_WIDTH = 300
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)



class LoginView(MessageView):
  def __init__(self, display):
    MessageView.__init__(self, display)
    
    font = display.getFont()
    font_welcome = display.getFont(30)
    font_note = display.getFont(14)
    self.display_size = display.getSize()
    
    # calc middle of screen
    hmiddle = self.display_size[0] / 2
    vmiddle = self.display_size[1] / 2
    
    # short form of constant
    space = SPACE_BETWEEN_LABEL_AND_INPUT / 2
    
    # short welcome text
    self.welcome_text = font_welcome.render(
      display.translator.translate("Welcome to Cards Against Humanity Online!"),
      1, (0, 0, 0))
    self.welcome_text_pos = (hmiddle - self.welcome_text.get_width() / 2, 100)
    
    # create labels and inputs for server, username and password
    self.server_label = font.render(display.translator.translate("Server")+":", 1, (0, 0, 0))
    self.port_label = font.render(display.translator.translate("Port") + ":", 1, (0, 0, 0))
    self.uname_label = font.render(display.translator.translate("Username")+":", 1, (0, 0, 0))
    self.pword_label = font.render(display.translator.translate("Password")+":", 1, (0, 0, 0))
    
    # calc positions of labels and inputs (same y for label and input as they
    #  should be side by side, same x for all inputs as the should be exactly
    #  among each other)
    self.server_label_x = hmiddle - self.server_label.get_width() - space - 100
    self.server_y = vmiddle - 70
    self.port_label_x = hmiddle - self.port_label.get_width() - space - 100
    self.port_y = self.server_y + 35
    self.uname_label_x = hmiddle - self.uname_label.get_width() - space - 100
    self.uname_y = self.port_y + 70
    self.pword_label_x = hmiddle - self.pword_label.get_width() - space - 100
    self.pword_y = self.uname_y + 35
    self.input_x = hmiddle + space - 100
    
    # create text inputs with positions
    self.server_input = TextInput(display, font, (self.input_x, self.server_y),
                                  TEXT_INPUT_WIDTH, display.translator.translate('Server'))
    self.server_input.input.input_string = self.display.server_name
    self.port_input = TextInput(display, font, (self.input_x, self.port_y),
                                  TEXT_INPUT_WIDTH,
                                  display.translator.translate('Port'), only_digits = True)
    self.port_input.input.input_string = str(self.display.server_port)
    self.uname_input = TextInput(display, font, (self.input_x, self.uname_y),
                                 TEXT_INPUT_WIDTH, display.translator.translate('Username'))
    self.uname_input.input.input_string = self.display.login_name
    self.pword_input = TextInput(display, font, (self.input_x, self.pword_y),
                                 TEXT_INPUT_WIDTH, display.translator.translate('Password'), True)
    self.pword_input.input.input_string = self.display.login_password
    
    # note for first login/create account
    self.login_note = font_note.render(
      display.translator.translate("NOTE: If username won't be found a new account will be created with "
      "the entered password!"),
      1, (224, 0, 0))
    
    self.login_note_x = hmiddle - self.login_note.get_width() / 2
    self.login_note_y = self.pword_y + 50
    
    # buttons connect and close (dummy positions, for auto-determine width
    # and height)
    self.button_connect = Button(self.display, display.translator.translate("Connect"), font,
                                 (hmiddle - 100, self.login_note_y + 70))
    # now calc position with own width
    self.button_connect.setPosition((hmiddle - self.button_connect.getWidth()
                                     - space, self.login_note_y + 70))
    self.button_connect.setCallback(self.onConnect)
    self.button_connect.setEnable(False)
    self.button_close = Button(self.display, display.translator.translate("Close"), font,
                               (hmiddle, self.login_note_y + 70))
    
    self.button_close.setCallback(self.onClose)
    
    self.button_select_language = Button(self.display, self.display.translator.translate("Select Language"), font, (0, 0))
    self.button_select_language.setPosition((self.display_size[0] - self.button_select_language.getWidth() - 20, self.display_size[1] - self.button_select_language.getHeight() - 20))
    self.button_select_language.setCallback(self.onSelectLanguage)
    self.button_select_language.setEnable(False)
    
    self.surface_languages = pygame.Surface((self.button_select_language.getWidth(), self.button_select_language.getHeight() * 2 + 60))
    self.languages_border = pygame.Rect(0, 0, self.surface_languages.get_width(), self.surface_languages.get_height())
    self.languages = ScrolledPanel(self.display, self.display_size[0] - self.button_select_language.getWidth(), self.display_size[1] - self.button_select_language.getHeight() - self.surface_languages.get_height() - 20, self.surface_languages.get_width() - 40, self.surface_languages.get_height() - 40)
    self.languages.setLabel(self.display.translator.translate("Language selection"))
    self.border_color = COLOR_BLACK
    
    self.next_surface_pos_y = self.languages.getPos()[1]

    self.addLanguageEntries()

    self.tab_order = [self.server_input, self.port_input, self.uname_input, self.pword_input,
                      self.button_connect, self.button_close, self.languages, self.button_select_language]
    self.language_selected = False
  
  
  def handleEventDefault(self, event):
    self.language_selected = False
    MessageView.handleEventDefault(self, event)
    self.server_input.handleEvent(event)
    self.port_input.handleEvent(event)
    self.uname_input.handleEvent(event)
    self.pword_input.handleEvent(event)
    
    self.button_connect.handleEvent(event)
    self.button_close.handleEvent(event)
    
    self.languages.handleEvent(event)
    self.button_select_language.handleEvent(event)
  
  
  def renderDefault(self):
    # blit texts and labels on screen
    self.display.screen.blit(self.welcome_text, self.welcome_text_pos)
    self.display.screen.blit(self.server_label,
                             (self.server_label_x, self.server_y))
    self.display.screen.blit(self.port_label, (self.port_label_x, self.port_y))
    self.display.screen.blit(self.uname_label,
                             (self.uname_label_x, self.uname_y))
    self.display.screen.blit(self.pword_label,
                             (self.pword_label_x, self.pword_y))
    
    # render text inputs
    self.server_input.render()
    self.port_input.render()
    self.uname_input.render()
    self.pword_input.render()
    
    # first login note
    self.display.screen.blit(self.login_note,
                             (self.login_note_x, self.login_note_y))
    
    # draw buttons
    self.button_connect.render()
    self.button_close.render()
    
    self.surface_languages.fill((255, 255, 255))
    pygame.draw.rect(self.surface_languages, self.border_color, self.languages_border, 1)
    self.display.screen.blit(self.surface_languages, (self.display_size[0] - self.button_select_language.getWidth() - 20, self.display_size[1] - self.button_select_language.getHeight() - self.surface_languages.get_height() - 40))
    self.languages.render()
    self.display.screen.blit(self.languages, self.languages.getPos())
    self.button_select_language.render()
    
  
  def updateDefault(self):
    MessageView.updateDefault(self)
    self.server_input.update()
    self.port_input.update()
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
      
    self.button_connect.update()
    self.button_close.update()
    self.button_select_language.update()
    if self.languages.getFocus():
      self.border_color = COLOR_RED
    else:
      self.border_color = COLOR_BLACK
      
  
  def firstUpdate(self):
    self.speak(self.display.translator.translate("Welcome to Cards Against Humanity Online!"))
    MessageView.firstUpdate(self)
  
  
  def onClose(self):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
  
  
  def onConnect(self):
    self.default_mode = False
    self.connectingMessage(self.server_input.input.get_text())
    self.display.callFunction('self.connect', self.server_input.input.get_text(),
                         int(self.port_input.input.get_text()),
                         self.uname_input.input.get_text(),
                         self.pword_input.input.get_text())


  def connectingMessage(self, address):
    self.setText(self.display.translator.translate('Connecting to {address}...').format(address = address))
    self.setButton('', None)
    self.display.connect_sound.stop()
    self.display.connect_sound.play()


  def clientRefusedMessage(self, reason):
    self.errorMessage(self.display.translator.translate('Connection refused by the server')+':\n%s'%reason)


  def loginMessage(self):
    self.setText(self.display.translator.translate('Logging in...'))
    self.setButton('', None)


  def syncMessage(self):
    self.setText(self.display.translator.translate('Syncing data...'))
    self.setButton('', None)


  def errorMessage(self, message):
    self.default_mode = False
    MessageView.errorMessage(self, message, self.onOK)


  def onOK(self):
    self.display.callFunction('self.factory.closeClient')
    self.default_mode = True
  
  
  def addLanguageEntries(self):
    for language in self.display.translator.getAvailableLanguages():
      language_entry = LanguageEntry(self.display, self.languages.getPos()[0], self.next_surface_pos_y, self.button_select_language.getWidth() - 60, self.button_select_language.getHeight(), language)
      language_entry.setSelectCallback(self.onLanguageSelect)
      language_entry.setDeselectCallback(self.onLanguageDeselect)
      self.languages.addSurface(language_entry)
      if language == self.display.translator.getLanguage():
        language_entry.setClicked()
        self.languages.cursor = len(self.languages.surfaces)-1
      self.next_surface_pos_y += language_entry.get_height() + self.languages.getVSpace()
  
  
  def onLanguageSelect(self, language):
    if language.text != self.display.translator.getLanguage():
      self.button_select_language.setEnable(True)
      self.language_selected = True
    self.display.surface_switch_sound.stop()
    self.display.surface_switch_sound.play()
    
  
  def onLanguageDeselect(self, language):
    if not self.language_selected:
      self.button_select_language.setEnable(False)


  def onSelectLanguage(self):

    language = self.languages.getClickedSurface()

    self.display.translator.setLanguage(language.text)
    self.display.config.set('language', language.text)
    self.display.setView('LoginView')
