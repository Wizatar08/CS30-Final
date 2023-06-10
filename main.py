import pygame, sys, util, time, math, random
import pygame.locals as gameGlobals

pygame.init() # Initialize pygame

WINDOW_SIZE = (800, 600) # Set window sizes
pygame.display.set_caption("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

TEXT_FONT = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 32) # Create fonts
TEXT_FONT_SMALL = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 16)

PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (127, 127, 0)]

WINDOW = pygame.display.set_mode(WINDOW_SIZE)

fpsClock = pygame.time.Clock() # Create clock, tracks FPS and time between frames

# ================================================================
# ================================================================
#
#  MAIN MENU
#
# ================================================================
# ================================================================

class MainMenu:

  def __init__(self):
    standardMenuWidth = 512
    self.startMenuOption = MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 240), (standardMenuWidth, 65), TEXT_FONT, "START")
    self.menuOptions = [
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 80), (standardMenuWidth, 65), TEXT_FONT, "Player 1: Barrel Man", "Player 1: Pog", "Player 1: ERR://23¤Y%/"),
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 160), (standardMenuWidth, 65), TEXT_FONT, "Player 2: Barrel Man", "Player 2: Pog", "Player 2: ERR://23¤Y%/"),
      self.startMenuOption
    ] # Create menu options
    self.currentIndex = 0
    

  def update(self) -> None:
    for i in range(len(self.menuOptions)): # Loop through all menu options
      self.menuOptions[i].isSelected = i == self.currentIndex # If the current index is on it, say that this is selected
      self.menuOptions[i].update() # Update
    self.detectKey() # Detect keys

    if self.startMenuOption.spaceTapped: # If the start button is pressed
      global currMenu
      currMenu = Game(self.menuOptions[0].currentIndex, self.menuOptions[1].currentIndex)

  def detectKey(self) -> None:
    if downTapped: # Loop down menu option if down is pressed
      self.currentIndex += 1
      if self.currentIndex > len(self.menuOptions) - 1:
        self.currentIndex = len(self.menuOptions) - 1
    elif upTapped: # Loop up through menu options if up is pressed
      self.currentIndex -= 1
      if self.currentIndex < 0:
        self.currentIndex = 0


class MenuOption:

  def __init__(self, coords, dimensions, font, *text):
    self.coords = coords # Set top left coords
    self.dimensions = dimensions # Set width/height
    self.font = font # Set font
    self.textList = list(text) # Set list of text to loop through
    self.usesArrows = len(self.textList) != 1 # Set whether this option can be looped through
    self.isSelected = False # Create a variable that determines if this is selected or not, default is False
    self.spaceTapped = False # If arrows are not used, detect if space is tapped
    self.outlineRect = pygame.rect.Rect(self.coords[0], self.coords[1], self.dimensions[0], self.dimensions[1]) # Create rect for outline
    self.text = Text(font, self.textList[0]) # Create text object, used for storing the text of the current menu option
    self.currentIndex = 0 # Current index for text list
    self.maxIndex = len(self.textList) - 1 # Max index for text list
    self.updateText()
    self.leftArrow = Text(font, "<") # Create arrows that would be on the sides of the selector, then set their coordinates
    self.rightArrow = Text(font, ">")
    self.leftArrow.x = self.coords[0] + 20
    self.leftArrow.y = self.coords[1] + (self.dimensions[1] // 2) - (self.font.size(self.leftArrow.text)[1] // 2)
    self.rightArrow.x = self.coords[0] + self.dimensions[0] - self.font.size(self.rightArrow.text)[0] - 20
    self.rightArrow.y = self.coords[1] + (self.dimensions[1] // 2) - (self.font.size(self.rightArrow.text)[1] // 2)

  def update(self) -> None:
    self.draw() # Continually draw the selector
    self.text.update() # Update all text
    if self.usesArrows == True and self.isSelected:
      self.leftArrow.update()
      self.rightArrow.update()
    if self.isSelected == True: # If this menu option is selected, detect if key is pressed
      self.detectKey()

  def detectKey(self) -> None:
    if self.usesArrows == True: # If the menu option requires the use of arrow keys
      if rightTapped: # Loop forwards through menu options if right is tapped
        self.currentIndex += 1
        if self.currentIndex > self.maxIndex: # Loop back to front
          self.currentIndex = 0
        self.text.text = self.textList[self.currentIndex]
        self.updateText()
      elif leftTapped: # Loop backwards through menu options if left is pressed
        self.currentIndex -= 1
        if self.currentIndex < 0: # Loop to back
          self.currentIndex = self.maxIndex
        self.text.text = self.textList[self.currentIndex]
        self.updateText()
    else: # If this is a menu option where space tap is needed, set the space tap variable to be whether space is tapped
      self.spaceTapped = spaceTapped

  def updateText(self) -> None: # Update text and coords when it changes
    textSize = self.font.size(self.textList[self.currentIndex])
    self.text.x = self.coords[0] + (self.dimensions[0] // 2) - (textSize[0] // 2) # Center text on box
    self.text.y = self.coords[1] + (self.dimensions[1] // 2) - (textSize[1] // 2)

  def draw(self) -> None:
    if self.isSelected: # Draw rectangles, different shade of grey depending on if this menu otpion is selected or not
      pygame.draw.rect(WINDOW, (127, 127, 127), self.outlineRect)
    else:
      pygame.draw.rect(WINDOW, (63, 63, 63), self.outlineRect)
    
class TransparentRectangle:

  def __init__(self, coords, dimensions, alpha, color, text = None):
    # Set properties
    self.x, self.y = coords
    self.width, self.height = dimensions

    # Create new surface
    self.surface = pygame.Surface(dimensions)
    self.surface.set_alpha(alpha)
    self.surface.fill(color)

    # Set text
    self.text = text

    # Set text to center rectangle
    if self.text != None:
      self.setText(self.text.text)

  def draw(self) -> None:
    WINDOW.blit(self.surface, (self.x, self.y)) # Put surface on window
    if self.text != None: # If there is text, update the text
      self.text.update()


  def setText(self, text) -> None:
    if self.text != None: # If there is text
      self.text.text = text # Set text to be new text and update its coords
      self.text.x = self.x + (self.width / 2) - (self.text.font.size(self.text.text)[0] // 2)
      self.text.y = self.y + (self.height / 2) - (self.text.font.size(self.text.text)[1] // 2)


class Text:

  def __init__(self, font, text, coords = (0, 0), textColor = (255, 255, 255), bgColor = None):
    self.font = font # Set font
    self.text = text # Set text
    self.x, self.y = coords # Set coords
    self.textColor = textColor # Set color of text
    self.bgColor = bgColor # Set background color of text
    self.show = True # Set text to be shown

  def update(self) -> None:
    renderer = self.font.render(self.text, True, self.textColor) # Render text
    if self.bgColor != None: # If the background color is not None, add the background color
      renderer = self.font.render(self.text, True, self.textColor, self.bgColor) 
    if self.show: # If the text should be shown
      WINDOW.blit(renderer, (self.x, self.y)) # Draw text at coords


# ================================================================
# ================================================================
#
#  END SCREEN
#
# ================================================================
# ================================================================

class EndScreen:

  def __init__(self, playerInformation):
    self.playerInfo = playerInformation # Set player information
    self.boxes = [] # Create background boxes
    self.playerModels = [] # Get image of player
    self.leftCoord = [] # Box left coordinates
    self.statText = [] # Create text boxes 
    self.boxSize = (150, 450) # Set player box size
    self.playerModelSize = (128, 128)
    for i in range(len(self.playerInfo)):
      self.statText.append([])
      self.leftCoord.append((WINDOW_SIZE[0] / 2) - ((self.boxSize[0] / 2) * (len(self.playerInfo))) + (self.boxSize[0] * i))
      self.boxes.append(TransparentRectangle((self.leftCoord[i], (WINDOW_SIZE[1] / 2) - (self.boxSize[1] / 2)), self.boxSize, 210, PLAYER_COLORS[i]))
      self.playerModels.append(pygame.transform.scale(self.playerInfo[i].image, self.playerModelSize))

      # Create stat text
      self.statText[i].append(Text(TEXT_FONT_SMALL, f"KO's: {self.playerInfo[i].dealtKos}", (self.leftCoord[i] + 4, 250)))
      self.statText[i].append(Text(TEXT_FONT_SMALL, f"Death's: {self.playerInfo[i].kos}", (self.leftCoord[i] + 4, 275)))
      self.statText[i].append(Text(TEXT_FONT_SMALL, f"Dealt damage: {round(self.playerInfo[i].damageDealt, 1)}", (self.leftCoord[i] + 4, 300)))
      self.statText[i].append(Text(TEXT_FONT_SMALL, f"Damage received: {round(self.playerInfo[i].damageReceived, 1)}", (self.leftCoord[i] + 4, 325)))
      self.statText[i].append(Text(TEXT_FONT_SMALL, f"Healing received: {round(self.playerInfo[i].healingReceived, 1)}", (self.leftCoord[i] + 4, 350)))

    # Create title text
    self.titleText = Text(TEXT_FONT, 'GAME OVER', (0, 15))
    self.titleText.x = (WINDOW_SIZE[0] / 2) - (self.titleText.font.size(self.titleText.text)[0] / 2)

    # Create continue text
    self.continueText = Text(TEXT_FONT, 'PRESS SPACE TO CONTINUE', (0, WINDOW_SIZE[1] - 65))
    self.continueText.x = (WINDOW_SIZE[0] / 2) - (self.continueText.font.size(self.continueText.text)[0] / 2)

  def update(self):
    for i in range(len(self.boxes)):
      self.boxes[i].draw() # Draw each box
      WINDOW.blit(self.playerModels[i], (self.leftCoord[i] + ((self.boxSize[0] - self.playerModelSize[0]) / 2), 100)) # Draw the player models
      for j in range(len(self.statText[i])): # Draw the stat text
        self.statText[i][j].update()
    self.titleText.update() # Draw the header/footer text
    self.continueText.update()

    if spaceTapped:
      global currMenu
      currMenu = MainMenu()




# ================================================================
# ================================================================
#
#  GAME
#
# ================================================================
# ================================================================

class Game:

  def __init__(self, player1option, player2option):
    self.platforms = [
      Platform((100, 500), (200, 15)), Platform((500, 500), (200, 15)), Platform((250, 375), (300, 15)),
      Platform((50, 250), (250, 15)), Platform((500, 250), (250, 15)), Platform((150, 125), (500, 15)),
    ] # Create level platforms
    self.players = [] # Create list of players
    if player1option == 0: # Set player 1 character
      self.players.append(BarrelMan(self, (100, 100), 'left', 'P1', PLAYER_COLORS[0]))
    elif player1option == 1:
      self.players.append(Pog(self, (100, 100), 'left', 'P1', PLAYER_COLORS[0]))
    elif player1option == 2:
      self.players.append(ErrorPlayer(self, (100, 100), 'left', 'P1', PLAYER_COLORS[0]))
    else:
      self.players.append(Player(self, (100, 100), 'left', 'P1', PLAYER_COLORS[0]))

    if player2option == 0: # Set player 2 character
      self.players.append(BarrelMan(self, (WINDOW_SIZE[0] - 100, 100), 'right', 'P2', PLAYER_COLORS[1]))
    elif player2option == 1:
      self.players.append(Pog(self, (WINDOW_SIZE[0] - 100, 100), 'right', 'P2', PLAYER_COLORS[1]))
    elif player2option == 2:
      self.players.append(ErrorPlayer(self, (WINDOW_SIZE[0] - 100, 100), 'right', 'P2', PLAYER_COLORS[1]))
    else:
      self.players.append(Player(self, (WINDOW_SIZE[0] - 100, 100), 'right', 'P2', PLAYER_COLORS[1]))

    self.allPlayers = self.players.copy()
    self.obstacles = [] # Create list of obstacles
 
    self.percentageXSpacingDiff = (WINDOW_SIZE[0] - 200) / (len(self.players) - 1) # Set spacing between percentage box
    self.statDisplay = {} # Create rectangles, putting the percentages of each player over top of them
    for i in range(len(self.players)): # Add a transparent rectangle to the list for each player
      player = self.players[i]
      self.statDisplay[player] = [
        TransparentRectangle((50 + (self.percentageXSpacingDiff * i), WINDOW_SIZE[1] - 80), (100, 50), 127, PLAYER_COLORS[i], Text(TEXT_FONT, '0%')),
        Text(TEXT_FONT_SMALL, 'Stocks: 3', (50 + (self.percentageXSpacingDiff * i), WINDOW_SIZE[1] - 30), PLAYER_COLORS[i])
      ]

    self.currUltBall = None
    self.ultBallSpawnTimeDelay = 3
    self.ultBallSpawnTime = self.ultBallSpawnTimeDelay

  def update(self) -> None:
    # Update players
    for player in self.players:
      player.update(self)

    # Update platforms
    for platform in self.platforms:
      platform.update(self)

    # Player attack box collisions
    removablePlayers = []
    for player in self.players:
      for hitPlayer in self.players:
        if player.attackBox != None:
          if player != hitPlayer and player.attackBox.colliderect(hitPlayer.rect):
            hitPlayer.onNormalAttack(player, (player.x + (player.width / 2), player.y + (player.height / 2)), 10)
          else:
            for obstacle in self.obstacles:
              if player.attackBox.colliderect(obstacle.rect) and obstacle.punchable:
                obstacle.onNormalAttack(player, (player.x + (player.width / 2), player.y + (player.height / 2)), 10)
      if player.stocks <= 0:
        removablePlayers.append(player)
    for player in removablePlayers:
      self.players.remove(player)
    if len(self.players) == 1:
      global currMenu
      currMenu = EndScreen(self.allPlayers)
    
    removableObstacles = [] # List of obstacles to remove (obstacles cannot be removed from the list when in the middle of looping through that list)
    for obstacle in self.obstacles: # Update the obstacle
      obstacle.update(self) 
      if obstacle.mustBeRemoved: # If the obstacle should be removed, put it on the removable obstacles list
        removableObstacles.append(obstacle)
    for obstacle in removableObstacles: # Remove any obstacles that should be removed
      self.obstacles.remove(obstacle)
  
    self.drawPlayerStats() # Draw the player percentages and background rectangles

    # Update ult ball
    if self.ultBallSpawnTime > 0:
      self.ultBallSpawnTime -= deltaT
    elif self.currUltBall == None:
      self.currUltBall = UltBall(self)
      self.obstacles.append(self.currUltBall)

  def drawPlayerStats(self) -> None:
    for player in self.players: # Draw rectangle and text for each player
      self.statDisplay[player][0].draw()
      self.statDisplay[player][1].update()

  def setPlayerStocks(self, player, stocks) -> None:
    self.statDisplay[player][1].text = f'Stocks: {stocks}'

  # Player/object actual hitbox collisions
  def hitObject(self, checkingPlayer) -> bool:
    for player in self.players: # Loop through players
      if player != checkingPlayer and checkingPlayer.rect.colliderect(player.rect): # If attack box hits another player, return the hit player
        return player
    for obstacle in self.obstacles:
      if checkingPlayer.rect.colliderect(obstacle.rect) and obstacle.punchable:
        return obstacle
    return None # if no players are found, return nothing

    



# STANDARD GAMEOBJECT CLASS

class GameObject:

  def __init__(self, coords, dimensions, img = None):

    # Set position and dimensions
    self.x, self.y = coords
    self.width, self.height = dimensions

    # Set image
    self.img = img

    # Set directions
    self.xDir, self.yDir = (0, 0)

    # Set rectangle
    self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    # Set usage of gravity
    self.usesGravity = False

    # Set weight
    self.weight = 5

    # Set if object is in the air
    self.inAir = True

    # Set attack stats
    self.punchable = False

  def update(self, game) -> None:
    self.rect.update(self.x, self.y, self.width, self.height) # Update rectangle
    if self.usesGravity: # if object uses gravity, apply gravity and, if this isn't a platform, detect if it hits a platform
      self.gravity()
      if not isinstance(self, Platform):
        self.collideWithPlatforms(game)
    self.move() # move object
    self.draw() # draw object
    
    if self.isOutOfBounds():
      self.onOutOfBounds()

  def move(self) -> None:
    self.x += self.xDir * 0.015 / deltaT # Change x and y positions based on time between frames and directions
    self.y += self.yDir * 0.015 / deltaT

  def draw(self) -> None:
    WINDOW.blit(self.img, (self.x, self.y)) # Draw the image
  
  def collideWithPlatforms(self, game) -> None:
    self.inAir = True
    for platform in game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect) # Get all the collision info for platform collision
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir > 0: # If the object is falling and hits the top of a platform (bottom of object hits platform)
        self.hitPlatformFromBottom(platform) # Run code to hit platform
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0: # If the object is going upwards and htis the bottom of a platform
        self.y -= self.yDir # Stop upwards movement
        self.yDir = 0
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0): # If object hits side of platform
        self.x -= self.xDir # Stop the object

  def gravity(self) -> None:
    self.yDir += 0.2 # Add 2 to the vertical movement of the character going down

  def hitPlatformFromBottom(self, platform) -> None: # Code used to hit platform from the bottom
    self.y = platform.rect.top - self.height # Set y position so bottom of object is touching the platform
    self.xDir = 0
    if self.yDir > 20: # Bounce object 
      self.yDir *= -1
    else:
      self.yDir = 0 # Stop the object from moving
      self.inAir = False

  def onNormalAttack(self, source, sourceCoords, damage, knockbackMultiplyer = 1, ignoreGroundRestrictions = False) -> None:
    mult = 1
    angle = math.atan2(self.y + (self.height / 2) - sourceCoords[1], self.x + (self.width / 2) - sourceCoords[0]) # Get angle between player and soure of knockback
    if not self.inAir and not ignoreGroundRestrictions: # If the player is not in the air
      if angle < math.pi * (1 / 4): # If hitting angle is too low or too high, set it so the player can lift off the ground
        angle = math.pi * (1 / 4)
      elif angle > math.pi * (3 / 4):
        angle = math.pi * (3 / 4)
      mult = -1 # Set y direction multiplier
    self.xDir = (math.cos(angle) * knockbackMultiplyer * 10) / self.weight # Set new x and y directions
    self.yDir = mult * (math.sin(angle) * knockbackMultiplyer * 10) / self.weight

  def isOutOfBounds(self) -> bool:
    return self.x < -1500 or self.x > WINDOW_SIZE[0] + 1500 or self.y < -2000 or self.y > WINDOW_SIZE[1] + 1000
    
  def onOutOfBounds(self):
    pass


# PLATFORM CLASS

class Platform(GameObject):

  def __init__(self, coords, dimensions):
    super().__init__(coords, dimensions)
    self.rect = pygame.rect.Rect(self.x, self.y, dimensions[0], dimensions[1]) # Create rectangle for the platform

    # ERRORCUBE platform modifier abilities
    self.glitchedPlatformSource = None
    self.glitchedImg = ChangingSprite(pygame.image.load('assets/images/characters/error/glitched_text.png'), (self.x, self.y), (self.width, self.height), 0.15)
    self.glitchedTimer = (0, 0)

  def draw(self) -> None:
    if self.glitchedPlatformSource != None:
      self.glitchedImg.update()
    else:
      pygame.draw.rect(WINDOW, (167, 167, 167), self.rect) # Draw the platform

  def update(self, game) -> None:
    self.updateGlitchedPlatform(game)
    super().update(game)

  def updateGlitchedPlatform(self, game) -> None:
    if self.glitchedPlatformSource != None: # If the platform is glitched
      for player in game.players:
        if player.onTopOfPlatform == self: # Do a certain effect depending on which players are on top of the platform
          if self.glitchedPlatformSource == player: # Player is the glitched platform source: subtract from their percentage
            player.setPercentage(self.glitchedPlatformSource, player.percentage - (deltaT * 2.5))
          else: # Other players: add to their percentage
            player.setPercentage(self.glitchedPlatformSource, player.percentage + (deltaT * 6))
      if time.time() - self.glitchedTimer[0] > self.glitchedTimer[1]: # Unglitch the platform once time runs out
        self.glitchedPlatformSource = None

  def glitch(self, source, timeLength):
    self.glitchedPlatformSource = source # Set source
    self.glitchedTimer = (time.time(), timeLength) # Set timer
    
    

# PLAYER CLASS

class Player(GameObject):
  # Variables that tell whether the ability should be held or not
  firstAbilityIsHeld = False
  secondAbilityIsHeld = False
  downwardsAbilityIsHeld = False

  def __init__(self, game, imgDir, coords, playerSide, hoverText, hoverTextColor):
    self.game = game
    self.hoverText = Text(TEXT_FONT_SMALL, hoverText)
    self.hoverText.textColor = hoverTextColor
    self.width, self.height = (32, 32) # Width and height coords
    super().__init__(coords, (self.width, self.height))
    self.rect = pygame.rect.Rect(coords[0], coords[1], self.width, self.height)
    self.playerSide = playerSide # 'left' or 'right'
    self.activeAbilities = { # Create a dictionary of active abilities, showing if they are active and their times they are activef
      'first': False,
      'second': False,
      'down': False,
      'ult': False
    }
    self.usesGravity = True

    # Aerial abilities
    self.inAir = True
    self.totalAirJumps = 1 # Amount of times player can double jump
    self.remainingAirJumps = 0 # Times player has double jumped since the last time player touched a surface

    self.weight = 3

    # Movement base vars
    self.jumpingPower = 25 # How high player can jump
    self.horizontalSpeed = 4 # Walking speed
    self.speedLocked = False
    self.direction = 1 # Sets which direction the character is facing (1 for right, -1 for left)
    self.incapacitatedTimers = (0, 0)

    # Controls
    self.leftControl = False
    self.rightControl = False
    self.upControl = False
    self.downControl = False
    self.firstAbilityControl = False
    self.secondAbilityControl = False
    self.shieldControl = False
    self.punchControl = False

    # Attacking
    self.attackBox = None
    self.percentage = 0
    self.punchable = True

    # Pointer image
    self.pointerImg = pygame.image.load('assets/images/character_visuals/character_pointer.png')

    # Shield information
    self.shieldImg = pygame.image.load('assets/images/character_visuals/shield.png')
    self.shieldActive = False
    self.shieldStartTimer = 0
    self.shieldButtonPressed = False

    # Game stats
    self.stocks = 3
    self.spawnCoords = coords
    self.hasUlt = False
    self.kos = 0
    self.dealtKos = 0
    self.damageDealt = 0
    self.damageReceived = 0
    self.healingReceived = 0
    self.recentlyAttackedBy = None

    # Ult glow image
    self.ultGlowImage = pygame.transform.scale(pygame.image.load('assets/images/character_visuals/ult_glow.png'), (64, 64))

    # Platform info
    self.onTopOfPlatform = None

    # Image
    self.imageDir = imgDir
    self.image = pygame.transform.scale(pygame.image.load(self.imageDir), (self.width, self.height))



  def update(self, game) -> None: # Update every frame
    self.updateControls()
    super().update(game) # Call super function
    self.drawHoverText()
    self.detectControls()
    if isinstance(self.activeAbilities['ult'], float):
      self.duringUltAbility()
      if self.activeAbilities['ult'] <= 0:
        self.endUltAbility()

  def draw(self, image = None) -> None:
    if image == None:
      image = self.image
    # Draw the ult glow if they have ult
    if self.hasUlt:
      WINDOW.blit(self.ultGlowImage, (self.x + (self.width / 2) - (self.ultGlowImage.get_width() / 2), self.y + (self.height / 2) - (self.ultGlowImage.get_height() / 2)))

    flipHorizontally = True if self.direction < 0 else False # Mirror the image horizontally so it faces the same direction as its movement
    WINDOW.blit(pygame.transform.flip(image, flipHorizontally, False), (self.x, self.y)) # Put image on screen

    # If the charactes is outside the shown screen:
    if self.x < -30 or self.x > WINDOW_SIZE[0] + 30 - self.width:
      maxHeight = WINDOW_SIZE[1] - 5 - self.height # Get maximum height the pointer can go up to
      pointerRotation = 0 # Set pointer rotation (this is in degrees, not radians, because pygame takes in degrees)
      if self.x < -30: # Rotate the pointer if the player is too much to the left of the screen (so it points left)
        pointerRotation = 180
        imageCoords = (5, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2)))) # Place the image to the left of the screen and at a y-position correlating to the actual y-position unless the character is too high or low on the screen
      else:
        imageCoords = (WINDOW_SIZE[0] - 5 - self.width, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2)))) # Same thing but pointer is on the right
      WINDOW.blit(pygame.transform.rotate(self.pointerImg, pointerRotation), imageCoords) # Blit the image at the coords provided above
      WINDOW.blit(pygame.transform.flip(pygame.transform.scale(image, (14, 14)), flipHorizontally, False), (imageCoords[0] + 9, imageCoords[1] + 9)) # Place the character image in the middle
    if self.shieldActive: # Draw shield if shield is active
      WINDOW.blit(self.shieldImg, (self.x - 12, self.y - 12))

  def drawHoverText(self):
    # Draw hover text
    self.hoverText.x = self.x + (self.width / 2) - (TEXT_FONT.size(self.hoverText.text)[0] / 2)
    self.hoverText.y = self.y - 25
    self.hoverText.update()

  def updateControls(self) -> None: # Detect specific keys to be tapped or pressed, determined by which side of the keyboard the player is using
    if time.time() - self.incapacitatedTimers[0] > self.incapacitatedTimers[1]:
      if self.playerSide == 'left':
        self.leftControl = aPressed
        self.rightControl = dPressed
        self.upControl = wTapped
        self.downControl = sTapped
        self.downControlHeld = sPressed
        self.firstAbilityControl = nTapped
        self.firstAbilityControlHeld = nPressed
        self.secondAbilityControl = mTapped
        self.secondAbilityControlHeld = mTapped
        self.shieldControl = hPressed
        self.punchControl = bTapped
        self.ultControl = nTapped and self.xDir == 0
      elif self.playerSide == 'right':
        self.leftControl = leftPressed
        self.rightControl = rightPressed
        self.upControl = upTapped
        self.downControl = downTapped
        self.downControlHeld = downPressed
        self.firstAbilityControl = num2Tapped
        self.firstAbilityControlHeld = num2Pressed
        self.secondAbilityControl = num3Tapped
        self.secondAbilityControlHeld = num3Pressed
        self.shieldControl = num5Pressed
        self.punchControl = num1Tapped
        self.ultControl = num2Tapped and self.xDir == 0
    else:
      self.leftControl = False
      self.rightControl = False
      self.upControl = False
      self.downControl = False
      self.downControlHeld = False
      self.firstAbilityControl = False
      self.firstAbilityControlHeld = False
      self.secondAbilityControl = False
      self.secondAbilityControlHeld = False
      self.shieldControl = False
      self.punchControl = False
      self.ultControl = False

  def collideWithPlatforms(self, game) -> None:
    self.inAir = True # Automatically set the player to be in the air
    self.onTopOfPlatform = None
    for platform in game.platforms: # Loop through platforms
      collisionInfo = util.rectangleCollision(self.rect, platform.rect) # Get collision info for object
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir >= 0: # If bottom of player hits platform, run hitting ground function
        self.onLandOnPlatform(platform)
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0:
        self.y -= self.yDir
        self.yDir = 0
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.x -= self.xDir

  def onLandOnPlatform(self, platform):
    self.y = platform.rect.top - self.height
    self.yDir = 0
    self.inAir = False
    self.remainingAirJumps = self.totalAirJumps
    self.onTopOfPlatform = platform

  def detectControls(self) -> None:

    if self.firstAbilityIsHeld and self.activeAbilities['first']:
      if self.firstAbilityControlHeld: # Keep running this function if the ability is supposed to be held and the key is still held
        self.pressedFirstAbility()
      else: # Run this function if the ability is supposed to be held and the key is released
        self.releaseFirstAbility()
    if self.secondAbilityIsHeld and self.activeAbilities['second']:
      if self.secondAbilityControlHeld:
        self.pressedSecondAbility()
      else:
        self.releaseSecondAbility()
    if self.downwardsAbilityIsHeld and self.activeAbilities['down']:
      if self.downControlHeld:
        self.pressedDownAbility()
      else:
        self.releaseDownAbility()

    if not self.speedLocked: # If speed can change by user input (not speedlocked)
      if self.leftControl: # Move left if a is pressed
        self.direction = -1
        if not self.inAir: # Constant velocity if on ground
          self.xDir = -self.horizontalSpeed
        elif self.xDir > -self.horizontalSpeed: # Changing velocity if in air
          self.xDir -= 0.5 / self.weight
      elif self.rightControl: # Move right if d is pressed
        self.direction = 1
        if not self.inAir: # Constant velocity if on ground
          self.xDir = self.horizontalSpeed
        elif self.xDir < self.horizontalSpeed: # Changing velocity if in air
          self.xDir += 0.5 / self.weight
      elif not self.inAir: # Stop moving horizontally if none are pressed
        self.xDir = 0
      else:
        self.xDir += 0.1 if self.xDir < 0 else -0.1
    if self.upControl: # Jump if w is tapped
      if self.inAir and self.remainingAirJumps > 0: # If player is already in air and there are remaining double jumps left, jump again
        self.yDir = -self.jumpingPower / self.weight
        self.remainingAirJumps -= 1
      elif not self.inAir: # Jump if on surface
        self.yDir = -self.jumpingPower / self.weight
    if self.activeAbilities['ult'] == False:
      if self.downControl and self.inAir: # Use downwards ability if s is pressed
        if self.activateDownwardsAbility() and self.downwardsAbilityIsHeld:
          self.activeAbilities['down'] = True
      elif self.ultControl and self.hasUlt: # Use ult ability if second ability key is pressed
        self.activateUltAbility()
      elif self.firstAbilityControl and self.activeAbilities['first'] == False: # Use first ability if first ability key is pressed
        if self.activateFirstAbility() and self.firstAbilityIsHeld:
          self.activeAbilities['first'] = True
      elif self.secondAbilityControl and self.activeAbilities['second'] == False: # Use second ability if second ability key is pressed
        if self.activateSecondAbility() and self.secondAbilityIsHeld:
          self.activeAbilities['second'] = True
      if self.punchControl:
        self.punch()
      else:
        self.attackBox = None
    
    if self.shieldControl and self.xDir == 0 and self.yDir == 0 and time.time() - self.shieldStartTimer < 2 and not self.shieldButtonPressed: # If shield is pressed, player is not moving, and shield cooldown timer has passed
      self.shieldActive = True # Activate shield
    else:
      self.shieldStartTimer = time.time() # Set shield timer to be current time
      self.shieldActive = False # Turn off shield
      self.shieldButtonPressed = True
    if not self.shieldControl:
      self.shieldButtonPressed = False
    


  def punch(self) -> None:
    if self.direction == 1: # Place an attack box in front of the player
      self.attackBox = pygame.rect.Rect(self.x + (self.width / 2), self.y - 16, (self.width / 2) + 24, self.height + 32)
    else:
      self.attackBox = pygame.rect.Rect(self.x - 24, self.y - 16, (self.width / 2) + 24, self.height + 32)

  def incapacitate(self, timeLength):
    self.incapacitatedTimers = (time.time(), timeLength)

  def onOutOfBounds(self) -> None:
    self.x, self.y = self.spawnCoords # Reset their position
    self.xDir, self.yDir = (0, 0) # Set their movement to be frozen
    self.stocks -= 1 # Remove one from their stocks
    self.kos += 1
    if self.recentlyAttackedBy != None:
      self.recentlyAttackedBy.dealtKos += 1
    self.setPercentage(None, 0)
    self.game.setPlayerStocks(self, self.stocks) # Remove 1 from stocks
    #self.recentlyAttackedBy = None
    self.resetAbilities() # Reset abilties

  def changeSize(self, newDimensions) -> None:
    previousWidth, previousHeight = self.width, self.height # Save previous sizes
    self.width, self.height = newDimensions # Set new sizes
    self.x = self.x + (previousWidth / 2) - (self.width / 2) # Set new x and y positions
    self.y = self.y + (previousHeight / 2) - (self.height / 2)
    self.rect.width = self.width # Set rectangle sizes
    self.rect.height = self.height

  def setPercentage(self, source, percentage):
    oldPercentage = self.percentage
    self.percentage = percentage # Set their percentages to be equal to 0
    if self.percentage < 0:
      self.percentage = 0
    self.game.statDisplay[self][0].setText(f'{round(self.percentage, 1)}%')
    self.recentlyAttackedBy = source

    # update percentage stats
    if self.percentage > oldPercentage:
      percentDiff = self.percentage - oldPercentage
      self.damageReceived += percentDiff
      if source != None:
        source.damageDealt += percentDiff
    elif self.percentage < oldPercentage and source != None:
      self.healingReceived += oldPercentage - self.percentage
    

  # FIRST ABILITY:
  def activateFirstAbility(self, time = 0, endable = False) -> bool: # TAP OR BEGIN PRESSING ABILITY
    self.firstAbilityControl = False
    if time > 0 and not self.firstAbilityIsHeld:
      self.activeAbilities['first'] = [time, endable]
    return True

  def pressedFirstAbility(self) -> None: # IF ABILITY IS HELD: RUN WHILE ABILITY BUTTON IS PRESSED
    pass;

  def releaseFirstAbility(self, time = 0, endable = False) -> None: # IF ABILITY IS HELD: RUN ONCE ABILITY BUTTON IS RELEASED
    if time > 0 and not self.firstAbilityIsHeld:
      self.activeAbilities['first'] = [time, endable]
    else:
      self.activeAbilities['first'] = False

  # SECOND ABILITY
  def activateSecondAbility(self, time = 0, endable = False) -> bool:
    self.secondAbilityControl = False
    if time > 0 and not self.secondAbilityIsHeld:
      self.activeAbilities['second'] = [time, endable]
    return True

  def pressedSecondAbility(self) -> None:
    pass;

  def releaseSecondAbility(self, time = 0, endable = False) -> None:
    if time > 0 and not self.secondAbilityIsHeld:
      self.activeAbilities['second'] = [time, endable]
    else:
      self.activeAbilities['second'] = False
  
  # DOWNWARDS ABILITY
  def activateDownwardsAbility(self, time = 0, endable = False) -> bool:
    self.downControl = False
    if time > 0 and not self.downwardsAbilityIsHeld:
      self.activeAbilities['down'] = [time, endable]
    return True
    
  def pressedDownAbility(self) -> None:
    pass;

  def releaseDownAbility(self, time = 0, endable = False) -> None:
    if time > 0 and not self.downwardsAbilityIsHeld:
      self.activeAbilities['down'] = [time, endable]
    else:
      self.activeAbilities['down'] = False
  
  # ULT ABILITY
  def activateUltAbility(self, time = 0) -> None:
    self.ultControl = False
    self.activeAbilities['ult'] = float(time)
    self.hasUlt = False
  
  def duringUltAbility(self) -> None:
    self.activeAbilities['ult'] -= deltaT

  def endUltAbility(self) -> None:
    self.activeAbilities['ult'] = False

  # RESET ABILITIES (when a stock is lost)
  def resetAbilities(self) -> None:
    self.remainingAirJumps = self.totalAirJumps

  def onNormalAttack(self, source, sourceCoords, damage, knockbackMultiplyer = 1, ignoreGroundRestrictions = False) -> None:
    if not self.shieldActive: # If player shield is down
      super().onNormalAttack(source, sourceCoords, damage, knockbackMultiplyer * 2 * ((self.percentage // 50) + 1), ignoreGroundRestrictions)
      self.setPercentage(source, self.percentage + damage)



# BARREL MAN CHARACTER

class BarrelMan(Player):
  firstAbilityIsHeld = True

  def __init__(self, game, coords, playerSide, hoverText, hoverTextColor):
    super().__init__(game, 'assets/images/characters/barrel_man/barrel_man.png', coords, playerSide, hoverText, hoverTextColor)
    self.rollImage = pygame.transform.scale(pygame.image.load(
      'assets/images/characters/barrel_man/barrel_man_roll.png'
    ), (self.width, self.height)) # Load rolling image

    # First ability timer
    self.rollTimer = 0

    # Second ability cooldown
    self.daggerTimer = 0

    # Downwards ability
    self.sword = None

    # ult ability
    self.bounceMechanic = False
    self.constSpeed = 15
    self.ultSize = (64, 64)
    self.ultCircle = util.Circle((0, 0), self.ultSize[0] / 2)
    self.ultImage = pygame.transform.scale(pygame.image.load('assets/images/characters/barrel_man/barrel_man_roll.png'), self.ultSize)
    self.ultHitPlayers = []
  
  def update(self, game) -> None:
    if self.sword != None and not self.sword.attachedToPlayer:
      self.sword = None
    if self.activeAbilities['ult'] != False:
      self.ultCircle.x = self.x + (self.width / 2)
      self.ultCircle.y = self.y + (self.height / 2)
    super().update(game)

  def draw(self) -> None:
    if self.activeAbilities['first'] != False: # Draw normal image if no abilities are used
      super().draw(self.rollImage)
    elif self.activeAbilities['ult'] != False:
      super().draw(self.ultImage)
    else: # Draw rolling image if an ability requiring Barrel Man to roll is used
      super().draw()

  def activateFirstAbility(self) -> bool:
    if self.xDir != 0: # If there is movement on the x-plane
      self.xDir = (self.xDir // abs(self.xDir)) * 10 # Set speed
      self.speedLocked = True # Lock speed
      self.rollTimer = time.time()
      return super().activateFirstAbility() # Activate first ability
    return False
  
  def pressedFirstAbility(self) -> None:
    hitObj = self.game.hitObject(self) # Find a hit player
    if hitObj != None: # If there is a hit player
      self.releaseFirstAbility() # End the ability
      hitObj.onNormalAttack(self, (self.x + (self.width / 2), self.y + (self.height / 2)), 36, 1.8) # Launch player
    if time.time() - self.rollTimer > 1.5:
      self.releaseFirstAbility()

  def releaseFirstAbility(self) -> None:
    super().releaseFirstAbility()
    self.speedLocked = False # Allow player to move again

  def activateSecondAbility(self) -> bool:
    if time.time() - self.daggerTimer > 3: # If dagger cooldown is passed
      self.daggerTimer = time.time() # Set cooldown timer
      for i in range(8): # Create 8 daggers, each going a different direction
        angle = i * (math.pi / 4)
        self.game.obstacles.append(Dagger(self.game, (self.x, self.y), angle, self))
      return super().activateSecondAbility()
    return False
  
  def activateDownwardsAbility(self) -> None:
    super().activateDownwardsAbility()
    self.sword = VeryLongSword(self.game, (self.x, self.y), self)
    self.game.obstacles.append(self.sword) # Create a very long sword, which will stick to the player until it hits the ground
    self.yDir = 15 # Set y-dir of player to be 15
    self.remainingAirJumps = 0 # Make sure barrel man cannot double jump afterwards

  def activateUltAbility(self) -> None:
    super().activateUltAbility(5)
    prevHeight = self.height
    self.changeSize((72, 72))
    self.bounceMechanic = True
    self.usesGravity = False
    if self.direction == 1:
      self.xDir = self.constSpeed
    else:
      self.xDir = -self.constSpeed
    self.yDir = self.constSpeed
    self.y -= (self.height / 2) - (prevHeight / 2)

  def duringUltAbility(self) -> None:

    # COLLISION WITH BORDER OF SCREEN
    if self.x < 0: 
      self.xDir = abs(self.xDir)
      self.x = 0
    if self.x > WINDOW_SIZE[0] - self.width:
      self.xDir = -abs(self.xDir)
      self.x = WINDOW_SIZE[0] - self.width
    if self.y < 0:
      self.yDir = abs(self.yDir)
      self.y = 0
    if self.y > WINDOW_SIZE[1] - self.height:
      self.yDir = -abs(self.yDir)
      self.y = WINDOW_SIZE[1] - self.height

    # COLLISIONS WITH PLATFORMS: BOUNCE OFF THEM
    for platform in self.game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect)
      if (collisionInfo[util.COLLIDE_TOP] and self.yDir < 0) or (collisionInfo[util.COLLIDE_BOTTOM] and self.yDir > 0):
        self.yDir *= -1
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.xDir *= -1

    # HIT PLAYERS
    for player in self.game.players:
      collided = util.rectangleCircleCollision(player.rect, self.ultCircle) # See if the circle and player has collided
      if player != self:
        if collided and not player in self.ultHitPlayers: # If they have, and they were not already collided, do an attack against the player
          player.onNormalAttack(self, (self.x, self.y), 30, 3.1)
          self.ultHitPlayers.append(player)
        elif not collided and player in self.ultHitPlayers: # If the player is no longer collided with the circle, remove it from the collided list
          self.ultHitPlayers.remove(player)

    super().duringUltAbility()

  def endUltAbility(self) -> None:
    super().endUltAbility()
    self.bounceMechanic = False
    self.changeSize((32, 32))
    self.usesGravity = True

  def move(self) -> None:
    if self.activeAbilities['ult'] != False:
      self.x += self.constSpeed * self.direction * 0.015 / deltaT # Change x and y positions based on time between frames and directions
      self.y += self.yDir * 0.015 / deltaT
    else:
      super().move()


  def resetAbilities(self) -> None:
    self.speedLocked = False # Turn off speedlock
    self.daggerTimer = 0 # Reset dagger timer
    if self.sword != None: # Remove Very Long Sword if it is still attached to Barrel Man
      self.game.obstacles.remove(self.sword)
      self.sword = None
    super().resetAbilities()



# POG CHARACTER

class Pog(Player):
  firstAbilityIsHeld = True

  def __init__(self, game, coords, playerSide, hoverText, hoverTextColor):
    super().__init__(game, 'assets/images/characters/pog/pog.png', coords, playerSide, hoverText, hoverTextColor)
    self.weight = 5 # Set base stats
    self.jumpingPower = 25
    self.totalAirJumps = 4
    self.regularSize = (self.width, self.height)

    # FIRST ABILITY
    self.firstAbilityCooldownTimer = 0
    self.firstAbilityHeldTimer = 0
    self.maxPogHoldTimer = 3

    # SECOND ABILITY
    self.isBig = False
    self.hitObjects = [] # Set players that this ability has hit

    # DOWN ABILITY
    self.releasedBomb = False

    # ULT ABILITY
    self.ultSize = [300, 425, 550]
    self.ultCircle = util.Circle((0, 0), self.ultSize[0] / 2)
    self.lockedX, self.lockedY = 0, 0
    self.timeAtSizeChange = 0
    self.currSizeIndex = 0

  def update(self, game) -> None:
    super().update(game)
    if self.isBig: # If player is big
      for gameObject in game.players + game.obstacles: # Loop through players
        if self != gameObject: # If the player is not themselves
          collide = self.rect.colliderect(gameObject.rect)
          if collide and not gameObject in self.hitObjects and gameObject.punchable: # If player hits Pog
            gameObject.onNormalAttack(self, (self.x, self.y), 19, 1.25) # Punch the player
            self.hitObjects.append(gameObject) # Set player to be hit by Pog
          elif not collide and gameObject in self.hitObjects:
            self.hitObjects.remove(gameObject)
    if not self.inAir:
      self.releasedBomb = False

  def activateFirstAbility(self) -> bool:
    if not self.isBig: # If the player is not big
      self.firstAbilityHeldTimer = time.time() # Set a timer for how long this is held down
      return super().activateFirstAbility()
    return False

  def pressedFirstAbility(self) -> None:
    if time.time() - self.firstAbilityHeldTimer > self.maxPogHoldTimer: # If the held down time reaches the maximum held down time
      self.releaseFirstAbility()

  def releaseFirstAbility(self) -> None:
    super().releaseFirstAbility()
    if time.time() - self.firstAbilityCooldownTimer >= 0.5: # If firsy ability is teleased and the time since the last projectile was shot is greater than 0.5s
      self.game.obstacles.append(PogProjectile(self.game, self, time.time() - self.firstAbilityHeldTimer)) # shoot projectile
      self.firstAbilityCooldownTimer = time.time() # Reset ability timer

  def activateDownwardsAbility(self) -> bool:
    if not self.isBig and not self.releasedBomb: # If the player is not big
      self.game.obstacles.append(PogBomb(self.game, self)) # Add a PogBomb to the game
      self.yDir -= 5
      self.releasedBomb = True
      return super().activateDownwardsAbility()
    return False

  def activateSecondAbility(self) -> bool:
    # Switch Pog from being small/big and set its mobility variables to match the soze
    if not self.isBig: 
      self.changeSize((80, 80))
      self.remainingAirJumps = 0
      self.totalAirJumps = 0
      self.jumpingPower = 75
      self.weight = 12
    else:
      self.changeSize((24, 24))
      self.totalAirJumps = 5
      self.remainingAirJumps = 5
      self.jumpingPower = 24
      self.weight = 5
      self.hitObjects.clear() # Make sure no objects are in this list when shrinking
    self.isBig = not self.isBig
    return super().activateSecondAbility()
  
  def activateUltAbility(self) -> None:
    super().activateUltAbility(3) # Activate ult for 3 seconds
    self.ultCircle.x = self.x + (self.width / 2) # Set coordinates for collision circle
    self.ultCircle.y = self.y + (self.height / 2)
    self.changeSize((self.ultSize[0], self.ultSize[0])) # Change size of image
    self.lockedX, self.lockedY = self.x, self.y # Set x and y variables to be locked in during this time
    self.speedLocked = True # Make sure xDir cannot be influenced during ult
    self.xDir = 0 # Set xDir and yDir to be 0
    self.yDir = 0
    self.usesGravity = False # Turn off gravity for Pog
    self.timeAtSizeChange = time.time() # Set time, so Pog knows when to change size

  def duringUltAbility(self) -> None:
    super().duringUltAbility()
    self.x, self.y = self.lockedX, self.lockedY # Set coords
    for gameObject in self.game.players + self.game.obstacles: # Loop through players and obstacles
      collide = util.rectangleCircleCollision(gameObject.rect, self.ultCircle) # Get collision info for circle and object
      if gameObject != self and collide and not gameObject in self.hitObjects and gameObject.punchable: # If it can, hit the object
        gameObject.onNormalAttack(self, (self.ultCircle.x, self.ultCircle.y), 41, 4.5)
        self.hitObjects.append(gameObject) # Add to list so it cannot be punched twice while already in collision influence
      elif not collide and gameObject in self.hitObjects: # Remove any objects that left the circle
        self.hitObjects.remove(gameObject)
    
    if time.time() - self.timeAtSizeChange >= 1 and self.currSizeIndex < len(self.ultSize): # Every 1 second:
      self.timeAtSizeChange = time.time() # Reset ult size change timer
      self.currSizeIndex += 1 # Look at next size in the list and change sizes
      self.changeSize((self.ultSize[self.currSizeIndex], self.ultSize[self.currSizeIndex]))
      self.lockedX = self.x # Set the new lockedX/Y to be the new coords
      self.lockedY = self.y
      self.ultCircle.radius = self.ultSize[self.currSizeIndex] / 2 # Set radius of circle to fit the new size

  def endUltAbility(self) -> None:
    super().endUltAbility()
    self.changeSize(self.regularSize) # Go back to regular size
    self.speedLocked = False # Go back to normal player settings
    self.usesGravity = True
    self.hitObjects.clear() # Clear this list
    self.currSizeIndex = 0

  def collideWithPlatforms(self, game) -> None:
    if self.activeAbilities['ult'] == False:
      super().collideWithPlatforms(game)
  
  def resetAbilities(self) -> None:
    self.isBig = False # Become small again, give the small properties back
    self.changeSize((24, 24))
    self.totalAirJumps = 5
    self.jumpingPower = 24
    self.weight = 5
    self.firstAbilityHeldTimer = 0 # Make sure Pop Projectile ability is reset (it doesn't fire after resetting)
    self.firstAbilityCooldownTimer = time.time() # Set the cooldown timer
    super().resetAbilities()

  def changeSize(self, newDimensions) -> None:
    super().changeSize(newDimensions) # Change size when Pog switches sizes
    self.image = pygame.transform.scale(pygame.image.load('assets/images/characters/pog/pog.png'), newDimensions) # Image bugs out after changing sizes a lot, so this should stop it

# ERROR PLAYER CLASS

class ErrorPlayer(Player):

  def __init__(self, game, coords, playerSide, hoverText, hoverTextColor):
    super().__init__(game, 'assets/images/characters/error/errorcube.png', coords, playerSide, hoverText, hoverTextColor)
    self.glitchedImage = ChangingSprite(pygame.image.load('assets/images/characters/error/green_code.png'), (0, 0), (24, 24), 0.2)
    self.currGlitchedPlatform = None
    self.glitchedMode = False

    # DOWN ABILITY
    self.downGlitch = False

    # FIRST ABILITY
    self.sideGlitch = False
    self.remainingDist = 0
    self.activeBomb = None
    self.bombCooldown = 0
    self.firstAbilityMovement = True

  def update(self, game) -> None:
    super().update(game)
    if (self.downGlitch and (not self.inAir or self.yDir <= 0)) or (self.sideGlitch and self.remainingDist <= 0): # If player's abilities do not require player to be in glitched mode, turn it off and reset any limitations
      self.glitchedMode = False
      self.speedLocked = False
      if self.downGlitch:
        self.downGlitch = False
      elif self.sideGlitch:
        self.sideGlitch = False
    if not self.inAir:
      self.firstAbilityMovement = True

    if self.currGlitchedPlatform != None and not self.currGlitchedPlatform.glitchedPlatformSource: # If a platform player is glitching passes its allowed glitch time, make sure the player knows as well
      self.currGlitchedPlatform = None

  def move(self) -> None:
    if not self.sideGlitch: # move as normal
      super().move()
    else:
      dist = 0.5 / deltaT # If side glitching, move the player towards the side
      self.x += dist * self.direction
      self.remainingDist -= dist

  def onLandOnPlatform(self, platform) -> None:
    if self.glitchedMode and self.currGlitchedPlatform == None: # If the player is using their down ability and don't already have a glitched latform
      self.currGlitchedPlatform = platform # Glitch platform and record it
      platform.glitch(self, 5)
      for player in self.game.players: # Launch all enemy players
        if player.onTopOfPlatform == platform:
          player.onNormalAttack(self, (player.x + (player.width / 2), player.y + (self.width * (3 / 2))), 12, 1.7, True)
    super().onLandOnPlatform(platform)

  def draw(self) -> None:
    if self.glitchedMode: # If in glitch mode, draw the glitch img
      self.glitchedImage.x = self.x
      self.glitchedImage.y = self.y
      self.glitchedImage.update()
    else:
      super().draw()

  def activateDownwardsAbility(self) -> bool:
    if not self.sideGlitch: # Use down ability if side ability is off
      self.glitchedMode = True # Launch player directly downwards
      self.yDir = 15
      self.speedLocked = True
      self.xDir = 0
      self.downGlitch = True
    return super().activateDownwardsAbility()
  
  def activateFirstAbility(self) -> bool:
    if not self.downGlitch: # Use side ability if down ability is off and no glitch bomb is in place
      if self.activeBomb == None and self.firstAbilityMovement: # Launch player sideways a certain distance
        self.remainingDist = 200
        self.sideGlitch = True
        self.glitchedMode = True
        self.speedLocked = True
        self.xDir = 0
        self.yDir = 0
        self.firstAbilityMovement = False
        if time.time() - self.bombCooldown >= 5: # If the last time this ability is used is greater than 5 seconds, create a glitch bomb
          newBomb = GlitchBomb(self.game, (self.x + (self.width / 2), self.y + (self.height / 2)), self)
          self.activeBomb = newBomb
          self.game.obstacles.append(newBomb)
          self.bombCooldown = time.time()
      elif self.activeBomb != None:
        self.activeBomb.detonate() # Detonate the bomb
        self.activeBomb = None
    return super().activateFirstAbility()
  
  def collideWithPlatforms(self, game) -> None: # If the side glitch effect isn't active, collide with platforms as normal
    if not self.sideGlitch:
      super().collideWithPlatforms(game)
  
  def resetAbilities(self) -> None:
    self.glitchedMode = False
    super().resetAbilities()
    self.bombCooldown = time.time()



# OBSTACLE CLASS

class Obstacle(GameObject):

  def __init__(self, game, coords, img, immunePlayer = None, timer = None):
    self.width, self.height = img.get_width(), img.get_height()
    super().__init__(coords, (self.width, self.height), img)
    
    # Set variables
    self.game = game
    self.immunePlayer = immunePlayer
    self.timer = timer
    self.detectHitObjects = []
    self.currentlyHitObjects = []
    for gameObject in game.players + game.obstacles: # Loop through player list, add all players except immune player to detectable players
      if gameObject != self.immunePlayer and gameObject.punchable:
        self.detectHitObjects.append(gameObject)
    self.mustBeRemoved = False # Variable used to tell the game when the obstacle should be removed from the game
    

  def update(self, game) -> None:
    super().update(game)
    self.detectCollision() # Detect collisions with players
    if self.timer != None: # Update obstacle timers
      self.updateTimer()
  
  def updateTimer(self) -> None:
    self.timer -= deltaT # Update timer
    if self.timer <= 0: # Run function if timer is less than or equal to 0 (most of the time, this will remove the obstacle)
      self.belowZeroTimer()

  def belowZeroTimer(self) -> None:
    self.mustBeRemoved = True # Remove obstacle
  
  def detectCollision(self) -> None:
    for player in self.detectHitObjects: # Loop through applicable players
      if self.rect.colliderect(player.rect) and not player in self.currentlyHitObjects:
        self.onCollision(player) # Hit player, make sure they are not hit twice before their rectangles are not colliding
        self.currentlyHitObjects.append(player)
      elif not self.rect.colliderect(player.rect) and player in self.currentlyHitObjects:
        self.currentlyHitObjects.remove(player)
  
  def onCollision(self, gameObject): # Code that runs when a player hits the obstacle
    pass

  def onNormalAttack(self, source, sourceCoords, damage, knockbackMultiplyer=1, ignoreGroundRestrictions=False) -> None:
    super().onNormalAttack(source, sourceCoords, damage, knockbackMultiplyer * 2, ignoreGroundRestrictions)

class UltBall(Obstacle):

  def __init__(self, game):
    super().__init__(game, (0, 0), pygame.image.load('assets/images/objects/ult_ball.png'))
    self.usesGravity = True
    self.health = 100
    self.punchable = True
    self.redoSpawn()

  def redoSpawn(self):
    self.x = random.randint(100, WINDOW_SIZE[0] - 100)
    self.y = -100
    self.xDir = 0
    self.yDir = 0

  def onOutOfBounds(self):
    self.redoSpawn()

  def onNormalAttack(self, source, sourceCoords, damage, knockbackMultiplyer=1, ignoreGroundRestrictions=False) -> None:
    super().onNormalAttack(source, sourceCoords, damage, knockbackMultiplyer, ignoreGroundRestrictions)
    self.health -= damage
    if self.health <= 0:
      source.hasUlt = True
      self.mustBeRemoved = True
      self.game.currUltBall = None
      self.game.ultBallSpawnTime = self.game.ultBallSpawnTimeDelay

class VeryLongSword(Obstacle):

  def __init__(self, game, coords, shotBy):
    super().__init__(game, coords, pygame.image.load("assets/images/objects/verylongsword.png"), shotBy, 6)
    self.attachedToPlayer = shotBy # Track who created the Very Long Sword
    self.shotBy = shotBy

  def update(self, game):
    super().update(game)
    if self.attachedToPlayer != None: # If sword is attached to Barrel Man
      self.x = self.attachedToPlayer.x + (self.attachedToPlayer.width / 2) - (self.width / 2) # Set coords to be just under Barrel Man
      self.y = self.attachedToPlayer.y + self.attachedToPlayer.height
      if not self.attachedToPlayer.inAir: # If Barrel Man hits ground, stick sword into the ground and remove it so it no longer follows the player
        self.attachedToPlayer = None
        self.y -= 10

  def onCollision(self, gameObject) -> None:
    gameObject.onNormalAttack(self.shotBy, (self.x, self.y), 11, 0.6) # Hit any colliding players

class Dagger(Obstacle):

  def __init__(self, game, coords, angle, shotBy):
    super().__init__(game, coords, pygame.image.load("assets/images/objects/dagger.png"), shotBy, 60)
    self.xDir = 14 * math.cos(angle) # Launch dagger in a particular direction
    self.yDir = 14 * math.sin(angle)
    self.angle = 0
    self.usesGravity = True
    self.stuck = False # Track whether the dagger should continue moving
    self.stuckTime = 7 # Time the dagger should stay once it hits a platform
    self.shotBy = shotBy

  def onCollision(self, gameObject) -> None:
    gameObject.onNormalAttack(self.shotBy, (self.x, self.y), 8, 0.35) # Hit any colliding players

  def update(self, game) -> None:
    if not self.stuck:
      self.angle = math.atan2(self.xDir, self.yDir) * (180 / math.pi) # Set angle
      for platform in game.platforms:
        if self.rect.colliderect(platform.rect): # If dagger hits a platform
          self.timer = self.stuckTime # Set timer so the dagger can disappear on its own
          self.usesGravity = False # Make sure dagger does not move due to gravity any longer
          self.xDir = 0 # Stop all movement
          self.yDir = 0
          self.stuck = True
    super().update(game)

  def draw(self) -> None:
    WINDOW.blit(pygame.transform.rotate(self.img, self.angle), (self.x, self.y))

  def hitPlatformFromBottom(self, platform) -> None:
    self.y = platform.rect.top - self.height
    self.y -= self.yDir
    self.inAir = False

class PogProjectile(Obstacle):

  def __init__(self, game, shotBy, power):
    self.power = power
    self.size = 12 + (self.power * 50) # Set size of projectile
    self.shotBy = shotBy

    super().__init__(game, (0, 0), pygame.transform.scale(pygame.image.load('assets/images/objects/pog_projectile.png'), (self.size, self.size)), shotBy, 5)
    self.x, self.y = shotBy.x - (self.width / 2), shotBy.y - (self.height / 4) # Set coords of the projectile spawning
    if shotBy.direction > 0: # Set direction of projectile moving, base the speed on power
      self.xDir = 5 + (power * 3)
    else:
      self.xDir = -5 - (power * 3)

  def onCollision(self, gameObject) -> None:
    gameObject.onNormalAttack(self.shotBy, (self.x + (self.width / 2), self.y + (self.height / 2)), 12 * (self.power), 0.9 + (self.power * 0.3)) # Launch hit players and add to their percentagers, based on the power of the projectile

class PogBomb(Obstacle):

  def __init__(self, game, shotBy):
    self.size = 36
    self.bombImage1 = pygame.transform.scale(pygame.image.load('assets/images/objects/pog_bomb1.png'), (self.size, self.size)) # Load different images
    self.bombImage2 = pygame.transform.scale(pygame.image.load('assets/images/objects/pog_bomb2.png'), (self.size, self.size))
    self.currImageFlipper = True # Track which of the two primed bomb texture should be displayed
    self.currImageFlipTimer = time.time()
    self.shotBy = shotBy

    self.explosion = util.CircularExplosion(150, AnimatedSprite(pygame.image.load('assets/images/explosions/pog_explosion.png'), (0, 0), 0.02, 100))

    super().__init__(game, (shotBy.x + (shotBy.width / 2) - (self.size / 2), shotBy.y + (shotBy.height / 2) - (self.size / 2)), self.bombImage1, None, 1.5)
    self.usesGravity = True
    self.punchable = True

  def update(self, game) -> None:
    super().update(game)
    if time.time() - self.currImageFlipTimer > 0.5: # Flip the image used in the bomb's primed stage
      self.currImageFlipper = not self.currImageFlipper
      self.currImageFlipTimer = time.time()

  def draw(self) -> None:
    if not self.explosion.isExploding:
      if self.currImageFlipper: # Display a different image based on how long it has been since it was last switched
        WINDOW.blit(self.bombImage1, (self.x, self.y))
      else:
        WINDOW.blit(self.bombImage2, (self.x, self.y))
    else: # Set the explosion coordinates to be at the top left of the texture, and update the animation
      self.explosion.draw()

  def belowZeroTimer(self) -> None:
    if not self.explosion.isExploding: # On the first frame where the bomb explodes, create the circle
      self.explosion.startExplosion((self.x + (self.width / 2), self.y + (self.height / 2)))
    self.isExploding = True
    self.punchable = False
    self.explosion.update()
    if self.explosion.atEnd: # Remove the obstacle if the animation is on its last frame
      self.mustBeRemoved = True

  def detectCollision(self) -> None:
    if self.explosion.isExploding:
      for player in self.detectHitObjects:
        if self.explosion.hitGameObject(player):
          self.onCollision(player)
      for obstacle in self.game.obstacles:
        if obstacle.punchable and self.explosion.hitGameObject(obstacle):
          self.onCollision(obstacle)

  def onCollision(self, gameObject) -> None:
    gameObject.onNormalAttack(self.shotBy, (self.x + (self.width / 2), self.y + (self.height / 2)), 43, 2.3) # Knockback/damage given

class GlitchBomb(Obstacle):

  def __init__(self, game, coords, shotBy):
    super().__init__(game, coords, pygame.transform.scale(pygame.image.load('assets/images/objects/missing_textures_pb.png'), (20, 20)), shotBy)
    self.usesGravity = True
    self.explosion = util.CircularExplosion(150, AnimatedSprite(pygame.image.load('assets/images/explosions/glitch_explosion.png'), (self.x, self.y), 0.05, 500))
    self.punchable = True

  def draw(self) -> None:
    if self.explosion.isExploding:
      self.explosion.draw()
    else:
      super().draw()

  def update(self, game) -> None:
    self.explosion.update()
    if self.explosion.atEnd: # At end of explosion animation, remove the object
      self.mustBeRemoved = True
    return super().update(game)
  
  def detonate(self):
    self.isExploding = True # Explode
    self.explosion.startExplosion((self.x + (self.width / 2), self.y + (self.height / 2)))
    self.punchable = False # make sure the explosion can't be punched
  
  def detectCollision(self) -> None:
    if self.explosion.isExploding: # Make sure the explosion circle exists
      for gameObject in self.detectHitObjects: # Hit a player if they hit the explosion
        if isinstance(gameObject, Player) and self.explosion.hitGameObject(gameObject):
          gameObject.incapacitate(1.5)

  


# ANIMATED SPRITE

class AnimatedSprite:

  def __init__(self, sprite, coords, timePerFrame, frameHeight):
    self.imgFull = sprite.convert_alpha() # Get sprite
    self.timePerFrame = timePerFrame # Set preferred time per frame and how high the image actually should be
    self.frameHeight = frameHeight

    self.x, self.y = coords
    self.width, self.height = self.imgFull.get_width(), self.frameHeight

    self.timeAtFrame = 0 # Get amount of time image is at a frame

    self.lastFrame = (self.imgFull.get_height() // self.frameHeight) - 1
    self.frame = 0

  def update(self) -> None:
    self.timeAtFrame += deltaT # Track time on frame
    if self.timeAtFrame > self.timePerFrame: # If time exceeds time needed at frame, move to the next frame
      self.frame += 1
      self.timeAtFrame = 0
      if self.frame > self.lastFrame: # Move back to the initial frame if there are no more frames
        self.frame = 0
    self.draw()
  
  def draw(self) -> None:
    WINDOW.blit(self.imgFull, (self.x, self.y), (0, self.frame * self.frameHeight, self.width, self.height))

  def scale(self, scaling) -> None:
    self.width, self.height = scaling # Scale the image
    self.frameHeight = self.height
    self.imgFull = pygame.transform.scale(self.imgFull, (self.width, self.height * (self.lastFrame + 1)))

# RANDOM CHANGING CLIPPED SPRITE

class ChangingSprite:

  def __init__(self, fullImage, coords, dimensions, timePerPartialImage):
    self.fullImage = fullImage
    self.x, self.y = coords # Position of image
    self.width, self.height = dimensions # Dimensions of cropped image
    self.timeDiff = timePerPartialImage # Time before there should be a new crop
    self.currTime = 0 # Time at crop
    self.imagePosX = 0 # Corner coords within the full image
    self.imagePosY = 0

  def update(self) -> None:
    self.currTime += deltaT # ADd to time at crop
    if time.time() - self.currTime >= self.timeDiff: # Set a new crop if time is exceeded
      self.changeSpritePosition()
    WINDOW.blit(self.fullImage, (self.x, self.y), (self.imagePosX, self.imagePosY, self.width, self.height)) # Blit that part of the image onto the screen

  def changeSpritePosition(self):
    self.imagePosX = random.randint(0, self.fullImage.get_width() - self.width) # Set new cropped corner coords
    self.imagePosY = random.randint(0, self.fullImage.get_height() - self.height)

  def scale(self, scaling) -> None: # Scale the image
    self.fullImage = pygame.transform.scale(self.fullImage, ((self.fullImage.get_width() / self.width) * scaling[0], (self.fullImage.get_height() / self.height) * scaling[1]))
    self.width, self.height = scaling
  

# ================================================================
# ================================================================
#
#  MAIN LOOP
#
# ================================================================
# ================================================================

currMenu = MainMenu()
deltaT = 0

while True:
  pygame.display.update() # Update display
  WINDOW.fill((0, 0, 0))
  deltaT = fpsClock.tick(60) / 1000
  
  keys = pygame.key.get_pressed() # Get all keys pressed
  wPressed = keys[gameGlobals.K_w] # Get certain pressed keys
  sPressed = keys[gameGlobals.K_s]
  aPressed = keys[gameGlobals.K_a]
  dPressed = keys[gameGlobals.K_d]
  bPressed = keys[gameGlobals.K_b]
  nPressed = keys[gameGlobals.K_n]
  mPressed = keys[gameGlobals.K_m]
  hPressed = keys[gameGlobals.K_h]
  upPressed = keys[gameGlobals.K_UP]
  downPressed = keys[gameGlobals.K_DOWN]
  leftPressed = keys[gameGlobals.K_LEFT]
  rightPressed = keys[gameGlobals.K_RIGHT]
  num1Pressed = keys[gameGlobals.K_KP1]
  num2Pressed = keys[gameGlobals.K_KP2]
  num3Pressed = keys[gameGlobals.K_KP3]
  num5Pressed = keys[gameGlobals.K_KP5]
  wTapped, sTapped, upTapped, downTapped, leftTapped, rightTapped, spaceTapped, keyTapped = False, False, False, False, False, False, False, False # Set tapped keys to be false

  # Player 1 tapped keys
  bTapped, nTapped, mTapped = False, False, False

  # Player 2 tapped keys
  num1Tapped, num2Tapped, num3Tapped = False, False, False
  
  
  for event in pygame.event.get():
    if event.type == gameGlobals.QUIT: # If the user wants to quit game, shut down python and system operations
      pygame.quit()
      sys.exit()
    elif event.type == gameGlobals.KEYDOWN: # If the key is down
      keyTapped = True # Show that a key is tapped
      if event.key == pygame.K_w: # If a certain key is tapped, set that variable to show that the key is tapped
        wTapped = True
      elif event.key == pygame.K_s:
        sTapped = True
      elif event.key == pygame.K_UP:
        upTapped = True
      elif event.key == pygame.K_DOWN:
        downTapped = True
      elif event.key == pygame.K_LEFT:
        leftTapped = True
      elif event.key == pygame.K_RIGHT:
        rightTapped = True
      elif event.key == pygame.K_SPACE:
        spaceTapped = True
        
      if event.key == pygame.K_b:
        bTapped = True
      elif event.key == pygame.K_n:
        nTapped = True
      elif event.key == pygame.K_m:
        mTapped = True
        
      if event.key == pygame.K_KP1:
        num1Tapped = True
      elif event.key == pygame.K_KP2:
        num2Tapped = True
      elif event.key == pygame.K_KP3:
        num3Tapped = True
      


  currMenu.update()
