from .message_view import MessageView

# this view will handle all possible messages which could occur while connecting
# including the login and connection progress, but also all errors
class ConnectionView(MessageView):
  def connectingMessage(self, address):
    self.setText(self.display.translator.translate('Connecting to {address}').format(address = address))
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
    self.setText(message)
    self.setButton(self.display.translator.translate('OK'), self.onOK)
    self.display.error_sound.stop()
    self.display.error_sound.play()

  def onOK(self):
    self.display.callFunction('self.factory.closeClient')
    self.display.setView('LoginView')
