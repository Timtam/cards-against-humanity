from .message_view import MessageView

# this view will handle all possible messages which could occur while connecting
# including the login and connection progress, but also all errors
class ConnectionView(MessageView):
  def connectingMessage(self, address):
    self.setText('connecting to %s...'%address)
    self.setButton('', None)
    self.display.connect_sound.stop()
    self.display.connect_sound.play()

  def clientRefusedMessage(self, reason):
    self.errorMessage('connection refused by the server:\n%s'%reason)

  def loginMessage(self):
    self.setText('logging in...')
    self.setButton('', None)

  def loggedInMessage(self, message):
    self.setText(message)
    self.setButton('OK', self.onOK)
    self.display.login_sound.stop()
    self.display.login_sound.play()

  def errorMessage(self, message):
    print message
    self.setText(message)
    self.setButton('OK', self.onOK)
    self.display.error_sound.stop()
    self.display.error_sound.play()

  def onOK(self):
    self.display.factory.closeClient()
    self.display.setView('LoginView')
