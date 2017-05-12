from .message_view import MessageView

# this view will handle all possible messages which could occur while connecting
# including the login and connection progress, but also all errors
class ConnectionView(MessageView):
  def connectingMessage(self, address):
    self.setText('connecting to %s...'%address)
    self.setButton('', None)

  def clientRefusedMessage(self, reason):
    self.setText('connection refused by the server:\n%s'%reason)
    self.setButton('OK', self.onOK)

  def loginMessage(self):
    self.setText('logging in...')
    self.setButton('', None)

  def loggedInMessage(self, message):
    self.setText(message)
    self.setButton('OK', self.onOK)

  def errorMessage(self, message):
    self.setText(message)
    self.setButton('OK', self.onOK)

  def onOK(self):
    self.display.factory.closeClient()
    self.display.setView('LoginView')
