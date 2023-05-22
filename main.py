import pygame, sys, util, time, math
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
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 80), (standardMenuWidth, 65), TEXT_FONT, "Player 1: Barrel Man", "Player 1: Pog", "Player 1: dfjsbgfjs"),
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 160), (standardMenuWidth, 65), TEXT_FONT, "Player 2: Barrel Man", "Player 2: Pog", "Player 2: dfjsbgfjs"),
      self.startMenuOption
    ] # Create menu options
    self.currentIndex = 0
    

  def update(self):
    for i in range(len(self.menuOptions)): # Loop through all menu options
      self.menuOptions[i].isSelected = i == self.currentIndex # If the current index is on it, say that this is selected
      self.menuOptions[i].update() # Update
    self.detectKey() # Detect keys

    if self.startMenuOption.spaceTapped: # If the start button is pressed
      global currMenu
      currMenu = Game(self.menuOptions[0].currentIndex, self.menuOptions[1].currentIndex)

  def detectKey(self):
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

  def update(self):
    self.draw() # Continually draw the selector
    self.text.update() # Update all text
    if self.usesArrows == True and self.isSelected:
      self.leftArrow.update()
      self.rightArrow.update()
    if self.isSelected == True: # If this menu option is selected, detect if key is pressed
      self.detectKey()

  def detectKey(self):
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

  def updateText(self): # Update text and coords when it changes
    textSize = self.font.size(self.textList[self.currentIndex])
    self.text.x = self.coords[0] + (self.dimensions[0] // 2) - (textSize[0] // 2) # Center text on box
    self.text.y = self.coords[1] + (self.dimensions[1] // 2) - (textSize[1] // 2)

  def draw(self):
    if self.isSelected: # Draw rectangles, different shade of grey depending on if this menu otpion is selected or not
      pygame.draw.rect(WINDOW, (127, 127, 127), self.outlineRect)
    else:
      pygame.draw.rect(WINDOW, (63, 63, 63), self.outlineRect)
    
class TransparentRectangle:

  def __init__(self, coords, dimensions, alpha, color, text = None):
    self.x, self.y = coords
    self.width, self.height = dimensions
    self.surface = pygame.Surface(dimensions)
    self.surface.set_alpha(alpha)
    self.surface.fill(color)
    self.text = text

  def draw(self):
    WINDOW.blit(self.surface, (self.x, self.y))
    if self.text != None:
      self.text.update()


  def setText(self, text):
    if self.text != None:
      self.text.text = text
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

  def update(self):
    renderer = self.font.render(self.text, True, self.textColor) # Render text
    if self.bgColor != None: # If the background color is not None, add the background color
      renderer = self.font.render(self.text, True, self.textColor, self.bgColor) 
    if self.show: # If the text should be shown
      WINDOW.blit(renderer, (self.x, self.y)) # Draw text at coords


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
    ]
    self.players = []
    if player1option == 0:
      self.players.append(BarrelMan(self, (100, 100), 'left'))
    elif player1option == 1:
      self.players.append(Pog(self, (100, 100), 'left'))
    else:
      self.players.append(Player(self, (100, 100), 'left'))

    if player2option == 0:
      self.players.append(BarrelMan(self, (WINDOW_SIZE[0] - 100, 100), 'right'))
    elif player2option == 1:
      self.players.append(Pog(self, (WINDOW_SIZE[0] - 100, 100), 'right'))
    else:
      self.players.append(Player(self, (WINDOW_SIZE[0] - 100, 100), 'right'))

    self.obstacles = []
 
    self.percentageXSpacingDiff = (WINDOW_SIZE[0] - 200) / (len(self.players) - 1)
    self.percentageRectangles = []
    for i in range(len(self.players)):
      self.percentageRectangles.append(TransparentRectangle((50 + (self.percentageXSpacingDiff * i), WINDOW_SIZE[1] - 80), (100, 50), 127, PLAYER_COLORS[i], Text(TEXT_FONT, '0%')))

  def update(self):
    # Update platforms
    for platform in self.platforms:
      platform.update(self)

    # Update players
    for player in self.players:
      player.update(self)

    # Player attack box collisions
    for player in self.players:
      for hitPlayer in self.players:
        if player.attackBox != None and player != hitPlayer and player.attackBox.colliderect(hitPlayer.rect):
          hitPlayer.punched(player, 10)
    
    removableObstacles = []
    for obstacle in self.obstacles:
      obstacle.update(self)
      if obstacle.mustBeRemoved:
        removableObstacles.append(obstacle)
    for obstacle in removableObstacles:
      self.obstacles.remove(obstacle)
  
    self.drawPlayerPrecentages()

  def drawPlayerPrecentages(self):
    for i in range(len(self.players)):
      self.percentageRectangles[i].setText(f"{self.players[i].percentage}%")
      self.percentageRectangles[i].draw()

  # Player actual hitbox collisions
  def hitPlayer(self, checkingPlayer):
    for player in self.players:
      if player != checkingPlayer and checkingPlayer.rect.colliderect(player.rect):
        return player
    return None

    



# STANDARD GAMEOBJECT CLASS

class GameObject:

  def __init__(self, coords, dimensions, img = None):
    self.x, self.y = coords
    self.width, self.height = dimensions
    self.img = img
    self.xDir, self.yDir = (0, 0)
    self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    self.usesGravity = False
    self.inAir = True

  def update(self, game):
    self.rect.update(self.x, self.y, self.width, self.height)
    if self.usesGravity:
      self.gravity()
      if not isinstance(self, Platform):
        self.collideWithPlatform(game)
    self.move(deltaT)
    self.draw()

  def move(self, deltaT):
    self.x += self.xDir * 15 / deltaT
    self.y += self.yDir * 15 / deltaT

  def draw(self):
    WINDOW.blit(self.img, (self.x, self.y))
  
  def collideWithPlatform(self, game):
    self.inAir = True
    for platform in game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect)
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir > 0:
        self.hitPlatformFromBottom(platform)
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0:
        self.y -= self.yDir
        self.yDir = 0
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.x -= self.xDir

  def gravity(self):
    self.yDir += 0.2 # Add 2 to the vertical movement of the character going down

  def hitPlatformFromBottom(self, platform):
    self.y = platform.rect.top - self.height
    self.yDir = 0
    self.inAir = False


# PLATFORM CLASS

class Platform(GameObject):

  def __init__(self, coords, dimensions):
    super().__init__(coords, dimensions)
    self.rect = pygame.rect.Rect(self.x, self.y, dimensions[0], dimensions[1])

  def draw(self):
    pygame.draw.rect(WINDOW, (241, 241, 241), self.rect)
    
    

# PLAYER CLASS

class Player(GameObject):
  firstAbilityIsHeld = False
  secondAbilityIsHeld = False
  ultAbilityIsHeld = False
  downwardsAbilityIsHeld = False

  def __init__(self, game, coords, playerSide):
    self.game = game
    self.width, self.height = (32, 32) # Width and height coords
    super().__init__(coords, (self.width, self.height))
    self.rect = pygame.rect.Rect(coords[0], coords[1], self.width, self.height)
    self.playerSide = playerSide # 'left' or 'right'
    self.activeAbilities = {
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

    # Movement base stats
    self.jumpingPower = 25 # How high player can jump
    self.horizontalSpeed = 4 # Walking speed
    self.speedLocked = False
    self.direction = 1 # Sets which direction the character is facing (1 for right, -1 for left)

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
    self.attackBox = None # Finish tomorrow
    self.percentage = 0

    # Pointer image
    self.pointerImg = pygame.image.load('assets/images/character_visuals/character_pointer.png')

    # Shield information
    self.shieldImg = pygame.image.load('assets/images/character_visuals/shield.png')
    self.shieldActive = False
    self.shieldStartTimer = 0
    self.shieldButtonPressed = False


  def draw(self, image = None):
    if image == None:
      pygame.draw.rect(WINDOW, (127, 127, 127), self.rect) # Draw a rectangle, showing the hitbox of the player (DEBUG FEATURE)
    else:
      flipHorizontally = True if self.direction < 0 else False
      WINDOW.blit(pygame.transform.flip(image, flipHorizontally, False), (self.x, self.y))
      maxHeight = WINDOW_SIZE[1] - 5 - self.height
      if self.x < -30 or self.x > WINDOW_SIZE[0] + 30 - self.width:
        pointerRotation = 0
        if self.x < -30:
          pointerRotation = 180
          imageCoords = (5, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2))))
        else:
          imageCoords = (WINDOW_SIZE[0] - 5 - self.width, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2))))
        WINDOW.blit(pygame.transform.rotate(self.pointerImg, pointerRotation), imageCoords)
        WINDOW.blit(pygame.transform.flip(pygame.transform.scale(image, (14, 14)), flipHorizontally, False), (imageCoords[0] + 9, imageCoords[1] + 9))
      if self.shieldActive:
        WINDOW.blit(self.shieldImg, (self.x - 12, self.y - 12))
    


  def update(self, game): # Update every frame
    self.collideWithPlatforms(game) # Check collisions with platforms
    self.updateControls()
    super().update(game) # Call super function
    self.detectControls()
    self.updateAbilities()

  def updateControls(self): # Detect specific keys to be tapped or pressed, determined by which side of the keyboard the player is using
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
      self.ultControl = bTapped and self.xDir == 0
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
      self.ultControl = num1Tapped and self.xDir == 0

  def collideWithPlatforms(self, game):
    self.inAir = True
    for platform in game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect)
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir >= 0:
        self.y = platform.rect.top - self.height
        self.yDir = 0
        self.inAir = False
        self.remainingAirJumps = self.totalAirJumps
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0:
        self.y -= self.yDir
        self.yDir = 0
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.x -= self.xDir

  def detectControls(self):

    if self.firstAbilityIsHeld and self.activeAbilities['first']:
      if self.firstAbilityControlHeld:
        self.pressedFirstAbility()
      else:
        self.releaseFirstAbility()
    if self.secondAbilityIsHeld and self.activeAbilities['second']:
      print(self.secondAbilityControlHeld)
      if self.secondAbilityControlHeld:
        self.pressedSecondAbility()
      else:
        self.releaseSecondAbility()
    if self.downwardsAbilityIsHeld and self.activeAbilities['down']:
      if self.downControlHeld:
        self.pressedDownAbility()
      else:
        self.releaseDownAbility()

    if not self.speedLocked:
      if self.leftControl: # Move left if a is pressed
        self.direction = -1
        if not self.inAir:
          self.xDir = -self.horizontalSpeed
        elif self.xDir > -self.horizontalSpeed:
          self.xDir -= 0.5 / self.weight
      elif self.rightControl: # Move right if d is pressed
        self.direction = 1
        if not self.inAir:
          self.xDir = self.horizontalSpeed
        elif self.xDir < self.horizontalSpeed:
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
    if self.downControl and self.inAir: # Use downwards ability if s is pressed
      self.activateDownwardsAbility()
      if self.downwardsAbilityIsHeld:
        self.activeAbilities['down'] = True
    elif self.firstAbilityControl and self.activeAbilities['first'] == False: # Use first ability if first ability key is pressed
      self.activateFirstAbility()
      if self.firstAbilityIsHeld:
        self.activeAbilities['first'] = True
    elif self.secondAbilityControl and self.activeAbilities['second'] == False: # Use second ability if second ability key is pressed
      self.activateSecondAbility()
      if self.secondAbilityIsHeld:
        self.activeAbilities['second'] = True
    elif self.ultControl and self.activeAbilities['ult'] == False: # Use second ability if second ability key is pressed
      self.activateUltAbility()
      if self.ultAbilityIsHeld:
        self.activeAbilities['ult'] = True
    if self.punchControl:
      self.punch()
    else:
      self.attackBox = None
    
    if self.shieldControl and self.xDir == 0 and self.yDir == 0 and time.time() - self.shieldStartTimer < 2 and not self.shieldButtonPressed:

      self.shieldActive = True
    else:
      self.shieldStartTimer = time.time()
      self.shieldActive = False
      self.shieldButtonPressed = True
    if not self.shieldControl:
      self.shieldButtonPressed = False
    


  def punch(self):
    if self.direction == 1:
      self.attackBox = pygame.rect.Rect(self.x + (self.width / 2), self.y - 16, (self.width / 2) + 24, self.height + 32)
    else:
      self.attackBox = pygame.rect.Rect(self.x - 24, self.y - 16, (self.width / 2) + 24, self.height + 32)


  def updateAbilities(self):

    # FIRST ABILITY UPDATE
    if type(self.activeAbilities['first']) == list:
      if self.duringFirstAbility():
        self.activeAbilities['first'][0] -= deltaT
        if (self.activeAbilities['first'][0] <= 0) or (self.activeAbilities['first'][1] and self.firstAbilityControl):
          self.endFirstAbility()

    # SECOND ABILITY UPDATE
    if type(self.activeAbilities['second']) == list:
      if self.duringSecondAbility():
        self.activeAbilities['second'][0] -= deltaT
        if (self.activeAbilities['second'][0] <= 0) or (self.activeAbilities['second'][1] and self.secondAbilityControl):
          self.endSecondAbility()

    # DOWNWARDS ABILITY UPDATE
    if type(self.activeAbilities['down']) == list:
      if self.duringDownAbility():
        self.activeAbilities['down'][0] -= deltaT
        if (self.activeAbilities['down'][0] <= 0) or (self.activeAbilities['down'][1] and self.downControl):
          self.endDownAbility()

    # ULT ABILITY UPDATE
    if type(self.activeAbilities['ult']) == list:
      if self.duringUltAbility():
        self.activeAbilities['ult'][0] -= deltaT
        if (self.activeAbilities['ult'][0] <= 0) or (self.activeAbilities['ult'][1] and self.ultControl):
          self.endUltABility()
    

  # FIRST ABILITY:
  def activateFirstAbility(self, time = 0, endable = False): # TAP OR BEGIN PRESSING ABILITY
    self.firstAbilityControl = False
    if time > 0 and not self.firstAbilityIsHeld:
      self.activeAbilities['first'] = [time * 1000, endable]

  def pressedFirstAbility(self): # IF ABILITY IS HELD: RUN WHILE ABILITY BUTTON IS PRESSED
    pass;

  def releaseFirstAbility(self, time = 0, endable = False): # IF ABILITY IS HELD: RUN ONCE ABILITY BUTTON IS RELEASED
    if time > 0 and not self.firstAbilityIsHeld:
      self.activeAbilities['first'] = [time * 1000, endable]
    else:
      self.activeAbilities['first'] = False
  
  def duringFirstAbility(self): # IF ABILITY IS TIMED: RUN WHILE ABILITY IS ACTIVE
    return False
  
  def endFirstAbility(self): # IF ABILITY IS TIMED: RUN WHEN ABILITY ENDS
    self.activeAbilities['first'] = False

  # SECOND ABILITY
  def activateSecondAbility(self, time = 0, endable = False):
    self.secondAbilityControl = False

  def pressedSecondAbility(self):
    pass;

  def releaseSecondAbility(self, time = 0, endable = False):
    if time > 0 and not self.secondAbilityIsHeld:
      self.activeAbilities['second'] = [time * 1000, endable]
    else:
      self.activeAbilities['second'] = False
  
  def duringSecondAbility(self):
    return False
  
  def endSecondAbility(self):
    self.activeAbilities['second'] = False
  
  # DOWNWARDS ABILITY
  def activateDownwardsAbility(self, time = 0, endable = False):
    self.downControl = False
    
  def pressedDownAbility(self):
    pass;

  def releaseDownAbility(self, time = 0, endable = False):
    if time > 0 and not self.downwardsAbilityIsHeld:
      self.activeAbilities['down'] = [time * 1000, endable]
    else:
      self.activeAbilities['down'] = False
  
  def duringDownAbility(self):
    return False
  
  def endDownAbility(self):
    self.activeAbilities['down'] = False
  
  # ULT ABILITY
  def activateUltAbility(self, time = 0, endable = False):
    self.ultControl = False
    pass
  
  def pressedUltAbility(self):
    pass;

  def releaseUltAbility(self, time = 0, endable = False):
    if time > 0 and not self.ultAbilityIsHeld:
      self.activeAbilities['ult'] = [time * 1000, endable]
    else:
      self.activeAbilities['ult'] = False
  
  def duringUltAbility(self):
    return False
  
  def endUltABility(self):
    self.activeAbilities['ult'] = False

  def punched(self, attacker, damage, knockbackMultiplyer = 1):
    mult = 1
    angle = math.atan2(self.y - attacker.y, self.x - attacker.x)
    if not self.inAir:
      if angle < math.pi * (1 / 4):
        angle = math.pi * (1 / 4)
      elif angle > math.pi * (3 / 4):
        angle = math.pi * (3 / 4)
      mult = -1
    self.xDir = (math.cos(angle) * knockbackMultiplyer * 20 * ((self.percentage // 50) + 1)) / self.weight
    self.yDir = mult * (math.sin(angle) * knockbackMultiplyer * 20 * ((self.percentage // 50) + 1)) / self.weight
    self.percentage += damage
    self.percentage = round(self.percentage, 1)



# BARREL MAN CHARACTER

class BarrelMan(Player):
  firstAbilityIsHeld = True

  def __init__(self, game, coords, playerSide):
    super().__init__(game, coords, playerSide)
    self.image = pygame.transform.scale(pygame.image.load(
      'assets/images/characters/barrel_man/barrel_man.png'
    ), (self.width, self.height)) # Load normal image
    self.rollImage = pygame.transform.scale(pygame.image.load(
      'assets/images/characters/barrel_man/barrel_man_roll.png'
    ), (self.width, self.height)) # Load rolling image

    # First ability timer
    self.rollTimer = 0

    # Second ability cooldown
    self.daggerTimer = 0
  
  def draw(self):
    if self.activeAbilities['first'] != False: # Draw normal image if no abilities are used
      super().draw(self.rollImage)
    else: # Draw rolling image if an ability requiring Barrel Man to roll is used
      super().draw(self.image)

  def activateFirstAbility(self):
    if self.xDir != 0: # If there is movement on the x-plane
      super().activateFirstAbility() # Activate first ability
      self.xDir = (self.xDir // abs(self.xDir)) * 10 # Set speed
      self.speedLocked = True # Lock speed
      self.rollTimer = time.time()
  
  def pressedFirstAbility(self):
    hitPlayer = self.game.hitPlayer(self) # Find a hit player
    if hitPlayer != None: # If there is a hit player
      self.releaseFirstAbility() # End the ability
      hitPlayer.punched(self, 36, 1.8) # Launch player
    if time.time() - self.rollTimer > 1.5:
      self.releaseFirstAbility()

  def releaseFirstAbility(self):
    super().releaseFirstAbility()
    self.speedLocked = False

  def activateSecondAbility(self):
    if time.time() - self.daggerTimer > 3:
      super().activateSecondAbility()
      self.daggerTimer = time.time()
      for i in range(8):
        angle = i * (math.pi / 4)
        self.game.obstacles.append(Dagger(self.game, (self.x, self.y), angle, self))
  
  def activateDownwardsAbility(self):
    super().activateDownwardsAbility()
    self.game.obstacles.append(VeryLongSword(self.game, (self.x, self.y), self))
    self.yDir = 15

# POG CHARACTER

class Pog(Player):
  firstAbilityIsHeld = True

  def __init__(self, game, coords, playerSide):
    super().__init__(game, coords, playerSide)
    self.image = pygame.transform.scale(pygame.image.load('assets/images/characters/pog/pog.png'), (self.width, self.height))
    self.weight = 5
    self.jumpingPower = 25
    self.totalAirJumps = 4

    # FIRST ABILITY
    self.firstAbilityHeldTimer = 0
    self.maxPogHoldTimer = 3

  def draw(self):
    super().draw(self.image)

  def activateFirstAbility(self):
    super().activateFirstAbility()
    self.firstAbilityHeldTimer = time.time()

  def pressedFirstAbility(self):
    if time.time() - self.firstAbilityHeldTimer > self.maxPogHoldTimer:
      self.releaseFirstAbility()

  def releaseFirstAbility(self):
    super().releaseFirstAbility()
    self.game.obstacles.append(PogProjectile(self.game, self, time.time() - self.firstAbilityHeldTimer))

  def activateDownwardsAbility(self):
    super().activateDownwardsAbility()
    self.game.obstacles.append(PogBomb(self.game, self))





# OBSTACLE CLASS

class Obstacle(GameObject):

  def __init__(self, game, coords, img, immunePlayer = None, timer = None):
    self.width, self.height = img.get_width(), img.get_height()
    super().__init__(coords, (self.width, self.height), img)
    self.game = game
    self.immunePlayer = immunePlayer
    self.timer = timer
    self.detectHitPlayers = []
    self.currentlyHitPlayers = []
    for player in game.players:
      if player != self.immunePlayer:
        self.detectHitPlayers.append(player)
    self.mustBeRemoved = False
    

  def update(self, game):
    super().update(game)
    self.detectCollision()
    if self.timer != None:
      self.updateTimer()
  
  def updateTimer(self):
    self.timer -= deltaT / 1000
    if self.timer <= 0:
      self.belowZeroTimer()

  def belowZeroTimer(self):
    self.mustBeRemoved = True
  
  def detectCollision(self):
    for player in self.detectHitPlayers:
      if self.rect.colliderect(player.rect) and not player in self.currentlyHitPlayers:
        self.onCollision(player)
        self.currentlyHitPlayers.append(player)
      elif not self.rect.colliderect(player.rect) and player in self.currentlyHitPlayers:
        self.currentlyHitPlayers.remove(player)
  
  def onCollision(self, player):
    pass

class VeryLongSword(Obstacle):

  def __init__(self, game, coords, shotBy):
    super().__init__(game, coords, pygame.image.load("assets/images/characters/barrel_man/verylongsword.png"), shotBy, 15)
    self.attachedToPlayer = shotBy

  def update(self, game):
    super().update(game)
    if self.attachedToPlayer != None:
      self.x = self.attachedToPlayer.x + (self.attachedToPlayer.width / 2) - (self.width / 2)
      self.y = self.attachedToPlayer.y + self.attachedToPlayer.height
      if not self.attachedToPlayer.inAir:
        self.attachedToPlayer = None
        self.y -= 10

  def onCollision(self, player):
    player.punched(self.immunePlayer, 23, 1.3)

class Dagger(Obstacle):

  def __init__(self, game, coords, angle, shotBy):
    super().__init__(game, coords, pygame.image.load("assets/images/characters/barrel_man/dagger.png"), shotBy, 60)
    self.xDir = 14 * math.cos(angle)
    self.yDir = 14 * math.sin(angle)
    self.angle = 0
    self.usesGravity = True
    self.stuck = False

  def onCollision(self, player):
    player.punched(self.immunePlayer, 6, 0.1)

  def update(self, game):
    if not self.stuck:
      self.angle = math.atan2(self.xDir, self.yDir) * (180 / math.pi)
      for platform in game.platforms:
        if self.rect.colliderect(platform.rect):
          self.timer = 5
          self.usesGravity = False
          self.xDir = 0
          self.yDir = 0
          self.stuck = True
    super().update(game)

  def draw(self):
    WINDOW.blit(pygame.transform.rotate(self.img, self.angle), (self.x, self.y))

  def hitPlatformFromBottom(self, platform):
    self.y = platform.rect.top - self.height
    self.y -= self.yDir
    self.inAir = False

class PogProjectile(Obstacle):

  def __init__(self, game, shotBy, power):
    self.power = power
    self.size = 12 + (self.power * 20)

    super().__init__(game, (0, 0), pygame.transform.scale(pygame.image.load('assets/images/characters/pog/pog_projectile.png'), (self.size, self.size)), shotBy, 5)
    self.x, self.y = shotBy.x - (self.width / 2), shotBy.y - (self.height / 4)
    if shotBy.direction > 0:
      self.xDir = 9
    else:
      self.xDir = -9

  def onCollision(self, player):
    player.punched(self.immunePlayer, 12 * (self.power + 1), 0.9 + (self.power * 0.3))

class PogBomb(Obstacle):

  def __init__(self, game, shotBy):
    self.size = 36
    self.bombImage1 = pygame.transform.scale(pygame.image.load('assets/images/characters/pog/pog_bomb1.png'), (self.size, self.size))
    self.bombImage2 = pygame.transform.scale(pygame.image.load('assets/images/characters/pog/pog_bomb2.png'), (self.size, self.size))
    self.explosionImage = AnimatedSprite(pygame.image.load('assets/images/characters/pog/pog_explosion.png'), (0, 0), 0.02, 100)
    self.currImageFlipper = True
    self.currImageFlipTimer = time.time()
    self.isExploding = False
    super().__init__(game, (shotBy.x + (shotBy.width / 2) - (self.size / 2), shotBy.y + (shotBy.height / 2) - (self.size / 2)), self.bombImage1, shotBy, 3)
    self.usesGravity = True

  def update(self, game):
    super().update(game)
    if time.time() - self.currImageFlipTimer > 0.5:
      self.currImageFlipper = not self.currImageFlipper
      self.currImageFlipTimer = time.time()

  def draw(self):
    if not self.isExploding:
      if self.currImageFlipper:
        WINDOW.blit(self.bombImage1, (self.x, self.y))
      else:
        WINDOW.blit(self.bombImage2, (self.x, self.y))
    else:
      self.explosionImage.x = self.x + (self.width / 2) - (self.explosionImage.width / 2)
      self.explosionImage.y = self.y + (self.height / 2) - (self.explosionImage.height / 2)
      self.explosionImage.update()

  def belowZeroTimer(self):
    self.explosionImage.scale((350, 350))
    self.isExploding = True
    if self.explosionImage.frame == self.explosionImage.lastFrame:
      self.mustBeRemoved = True






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

  def update(self):
    self.timeAtFrame += deltaT / 1000
    if self.timeAtFrame > self.timePerFrame:
      self.frame += 1
      self.timeAtFrame = 0
      if self.frame > self.lastFrame:
        self.frame = 0
    self.draw()
  
  def draw(self):
    WINDOW.blit(self.imgFull, (self.x, self.y), (0, self.frame * self.frameHeight, self.width, self.height))

  def scale(self, scaling):
    self.width, self.height = scaling
    self.frameHeight = self.height
    self.imgFull = pygame.transform.scale(self.imgFull, (self.width, self.height * (self.lastFrame + 1)))

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
  deltaT = fpsClock.tick(60)
  
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