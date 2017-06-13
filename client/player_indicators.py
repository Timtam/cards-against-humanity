from player_square import PlayerSquare

SQUARE_SIZE = (50, 50)
SPACE = 5



class PlayerIndicators:
  def __init__(self, display, x, y, width=-1, height=-1):
    
    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.pos_x_new_square = self.x
    
    self.player_squares = []
  
  
  def addPlayer(self, id):
    self.player_squares.append(PlayerSquare(self.display, self.pos_x_new_square, self.y, SQUARE_SIZE[0], SQUARE_SIZE[1], id))
    self.pos_x_new_square += SQUARE_SIZE[0] + SPACE
  
  
  def getPlayer(self, id):
    for player in self.player_squares:
      if player.id == id:
        return player


  def delPlayer(self, id):
    for player in self.player_squares:
      if player.id == id:
        self.player_squares.remove(player)
    tmp_players = self.player_squares
    self.clearPlayers()
    for player in tmp_players:
      self.addPlayer(player.id)


  def clearPlayers(self):
    self.player_squares = []
    self.pos_x_new_square = self.x
  
  
  def setZar(self, id):
    czar = self.getPlayer(id)
    czar.setCzar()
  
  
  def setUnchosen(self):
    for player in self.player_squares:
      player.setUnchosen()
  
  
  def setChosen(self, id):
    player = self.getPlayer(id)
    player.setChosen()
  
  
  def handleEvent(self, event):
    for player in self.player_squares:
      player.handleEvent(event)
  
  
  def update(self):
    for player in self.player_squares:
      player.update()
  
  
  def render(self):
    pos_x = 0
    for player in self.player_squares:
      player.render()
      self.display.screen.blit(player, (self.x + pos_x, self.y))
      pos_x += player.get_width() + SPACE