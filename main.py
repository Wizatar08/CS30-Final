import pygame, sys, util, time, math
import pygame.locals as gameGlobals

pygame.init(); # Initialize pygame

WINDOW_SIZE = (800, 600); # Set window sizes
pygame.display.set_caption("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

TEXT_FONT = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 32); # Create fonts
TEXT_FONT_SMALL = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 16);

PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (127, 127, 0)];

WINDOW = pygame.display.set_mode(WINDOW_SIZE);

fpsClock = pygame.time.Clock(); # Create clock, tracks FPS and time between frames

# ================================================================
# ================================================================
#
#  MAIN MENU
#
# ================================================================
# ================================================================

class MainMenu:

  def __init__(self):
    standardMenuWidth = 512;
    self.startMenuOption = MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 240), (standardMenuWidth, 65), TEXT_FONT, "START");
    self.menuOptions = [
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 80), (standardMenuWidth, 65), TEXT_FONT, "Player 1: Barrel Man", "Player 1: fhdj", "Player 1: dfjsbgfjs"),
      MenuOption(((WINDOW_SIZE[0] // 2) - (standardMenuWidth // 2), 160), (standardMenuWidth, 65), TEXT_FONT, "Player 2: Barrel Man", "Player 2: fhdj", "Player 2: dfjsbgfjs"),
      self.startMenuOption
    ] # Create menu options
    self.currentIndex = 0;
    

  def update(self, deltaT):
    for i in range(len(self.menuOptions)): # Loop through all menu options
      self.menuOptions[i].isSelected = i == self.currentIndex; # If the current index is on it, say that this is selected
      self.menuOptions[i].update(); # Update
    self.detectKey(); # Detect keys

    if self.startMenuOption.spaceTapped: # If the start button is pressed
      global currMenu;
      currMenu = Game(self.menuOptions[0].currentIndex, self.menuOptions[1].currentIndex);

  def detectKey(self):
    if downTapped: # Loop down menu option if down is pressed
      self.currentIndex += 1;
      if self.currentIndex > len(self.menuOptions) - 1:
        self.currentIndex = len(self.menuOptions) - 1;
    elif upTapped: # Loop up through menu options if up is pressed
      self.currentIndex -= 1;
      if self.currentIndex < 0:
        self.currentIndex = 0;


class MenuOption:

  def __init__(self, coords, dimensions, font, *text):
    self.coords = coords; # Set top left coords
    self.dimensions = dimensions; # Set width/height
    self.font = font; # Set font
    self.textList = list(text); # Set list of text to loop through
    self.usesArrows = len(self.textList) != 1; # Set whether this option can be looped through
    self.isSelected = False; # Create a variable that determines if this is selected or not, default is False
    self.spaceTapped = False; # If arrows are not used, detect if space is tapped
    self.outlineRect = pygame.rect.Rect(self.coords[0], self.coords[1], self.dimensions[0], self.dimensions[1]); # Create rect for outline
    self.text = Text(font, self.textList[0]); # Create text object, used for storing the text of the current menu option
    self.currentIndex = 0; # Current index for text list
    self.maxIndex = len(self.textList) - 1; # Mxx index for text list
    self.updateText();
    self.leftArrow = Text(font, "<"); # Create arrows that would be on the sides of the selector, then set their coordinates
    self.rightArrow = Text(font, ">");
    self.leftArrow.x = self.coords[0] + 20;
    self.leftArrow.y = self.coords[1] + (self.dimensions[1] // 2) - (self.font.size(self.leftArrow.text)[1] // 2);
    self.rightArrow.x = self.coords[0] + self.dimensions[0] - self.font.size(self.rightArrow.text)[0] - 20;
    self.rightArrow.y = self.coords[1] + (self.dimensions[1] // 2) - (self.font.size(self.rightArrow.text)[1] // 2);

  def update(self):
    self.draw(); # Continually draw the selector
    self.text.update(); # Update all text
    if self.usesArrows == True and self.isSelected:
      self.leftArrow.update();
      self.rightArrow.update();
    if self.isSelected == True: # If this menu option is selected, detect if key is pressed
      self.detectKey();

  def detectKey(self):
    if self.usesArrows == True: # If the menu option requires the use of arrow keys
      if rightTapped: # Loop forwards through menu options if right is tapped
        self.currentIndex += 1;
        if self.currentIndex > self.maxIndex: # Loop back to front
          self.currentIndex = 0;
        self.text.text = self.textList[self.currentIndex];
        self.updateText();
      elif leftTapped: # Loop backwards through menu options if left is pressed
        self.currentIndex -= 1;
        if self.currentIndex < 0: # Loop to back
          self.currentIndex = self.maxIndex;
        self.text.text = self.textList[self.currentIndex];
        self.updateText()
    else: # If this is a menu option where space tap is needed, set the space tap variable to be whether space is tapped
      self.spaceTapped = spaceTapped;

  def updateText(self): # Update text and coords when it changes
    textSize = self.font.size(self.textList[self.currentIndex]);
    self.text.x = self.coords[0] + (self.dimensions[0] // 2) - (textSize[0] // 2); # Center text on box
    self.text.y = self.coords[1] + (self.dimensions[1] // 2) - (textSize[1] // 2);

  def draw(self):
    if self.isSelected: # Draw rectangles, different shade of grey depending on if this menu otpion is selected or not
      pygame.draw.rect(WINDOW, (127, 127, 127), self.outlineRect);
    else:
      pygame.draw.rect(WINDOW, (63, 63, 63), self.outlineRect);
    
class TransparentRectangle:

  def __init__(self, coords, dimensions, alpha, color, text = None):
    self.x, self.y = coords;
    self.width, self.height = dimensions;
    self.surface = pygame.Surface(dimensions)
    self.surface.set_alpha(alpha);
    self.surface.fill(color);
    self.text = text;

  def draw(self):
    WINDOW.blit(self.surface, (self.x, self.y));
    if self.text != None:
      self.text.update();


  def setText(self, text):
    if self.text != None:
      self.text.text = text;
      self.text.x = self.x + (self.width / 2) - (self.text.font.size(self.text.text)[0] // 2);
      self.text.y = self.y + (self.height / 2) - (self.text.font.size(self.text.text)[1] // 2);


class Text:

  def __init__(self, font, text, coords = (0, 0), textColor = (255, 255, 255), bgColor = None):
    self.font = font; # Set font
    self.text = text; # Set text
    self.x, self.y = coords; # Set coords
    self.textColor = textColor; # Set color of text
    self.bgColor = bgColor; # Set background color of text
    self.show = True; # Set text to be shown

  def update(self):
    renderer = self.font.render(self.text, True, self.textColor); # Render text
    if self.bgColor != None: # If the background color is not None, add the background color
      renderer = self.font.render(self.text, True, self.textColor, self.bgColor); 
    if self.show: # If the text should be shown
      WINDOW.blit(renderer, (self.x, self.y)); # Draw text at coords


# ================================================================
# ================================================================
#
#  GAME
#
# ================================================================
# ================================================================

class Game:

  def __init__(self, player1option, player2option):
    self.platforms = [Platform((50, 450), (600, 60)), Platform((0, 200), (300, 130)), Platform((700, 300), (100, 100))];
    self.players = [];
    if player1option == 0:
      self.players.append(BarrelMan(self, (100, 100), 'left'));
    else:
      self.players.append(Player(self, (100, 100), 'left'));

    if player2option == 0:
      self.players.append(BarrelMan(self, (WINDOW_SIZE[0] - 100, 100), 'right'));
    else:
      self.players.append(Player(self, (WINDOW_SIZE[0] - 100, 100), 'right'));

 
    self.percentageXSpacingDiff = (WINDOW_SIZE[0] - 200) / (len(self.players) - 1);
    self.percentageRectangles = [];
    for i in range(len(self.players)):
      self.percentageRectangles.append(TransparentRectangle((50 + (self.percentageXSpacingDiff * i), WINDOW_SIZE[1] - 80), (100, 50), 127, PLAYER_COLORS[i], Text(TEXT_FONT, '0%')));

  def update(self, deltaT):
    # Update platforms
    for platform in self.platforms:
      platform.update(self, deltaT);

    # Update players
    for player in self.players:
      player.update(self, deltaT);

    # Player attack box collisions
    for player in self.players:
      for hitPlayer in self.players:
        if player.attackBox != None and player != hitPlayer and player.attackBox.colliderect(hitPlayer.rect):
          hitPlayer.punched(player, 10);
  
    self.drawPlayerPrecentages();

  def drawPlayerPrecentages(self):
    for i in range(len(self.players)):
      self.percentageRectangles[i].setText(f"{self.players[i].percentage}%");
      self.percentageRectangles[i].draw();

  # Player actual hitbox collisions
  def hitPlayer(self, checkingPlayer):
    for player in self.players:
      if player != checkingPlayer and checkingPlayer.rect.colliderect(player.rect):
        return player;
    return None;

    



# STANDARD GAMEOBJECT CLASS

class GameObject:

  def __init__(self, coords, dimensions, img = None):
    self.x, self.y = coords;
    self.width, self.height = dimensions;
    self.img = img;
    self.xDir, self.yDir = (0, 0);
    self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    self.usesGravity = False;
    self.inAir = True;

  def update(self, game, deltaT):
    if self.usesGravity:
      self.gravity();
      if not isinstance(self, Platform):
        self.collideWithPlatform(game);
    self.move(deltaT);
    self.draw();

  def move(self, deltaT):
    self.x += self.xDir * 15 / deltaT;
    self.y += self.yDir * 15 / deltaT;

  def draw(self):
    WINDOW.blit(self.img, (self.x, self.y));
  
  def collideWithPlatform(self, game):
    self.inAir = True;
    for platform in game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect)
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir > 0:
        self.y = platform.rect.top - self.height;
        self.yDir = 0;
        self.inAir = False;
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0:
        self.y -= self.yDir;
        self.yDir = 0;
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.x -= self.xDir;

  def gravity(self):
    self.yDir += 0.2; # Add 2 to the vertical movement of the character going down


# PLATFORM CLASS

class Platform(GameObject):

  def __init__(self, coords, dimensions):
    super().__init__(coords, dimensions);
    self.rect = pygame.rect.Rect(self.x, self.y, dimensions[0], dimensions[1]);

  def draw(self):
    pygame.draw.rect(WINDOW, (241, 241, 241), self.rect);
    
    

# PLAYER CLASS

class Player(GameObject):

  def __init__(self, game, coords, playerSide):
    self.game = game;
    self.width, self.height = (32, 32) # Width and height coords
    super().__init__(coords, (self.width, self.height));
    self.rect = pygame.rect.Rect(coords[0], coords[1], self.width, self.height);
    self.playerSide = playerSide; # 'left' or 'right'
    self.activeAbilities = {
      'first': False,
      'second': False,
      'down': False,
      'ult': False
    }
    self.usesGravity = True;

    # Aerial abilities
    self.inAir = True
    self.totalAirJumps = 1; # Amount of times player can double jump
    self.remainingAirJumps = 0; # Times player has double jumped since the last time player touched a surface

    self.weight = 3;

    # Movement base stats
    self.jumpingPower = 10; # How high player can jump
    self.horizontalSpeed = 4; # Walking speed
    self.speedLocked = False;
    self.direction = 1; # Sets which direction the character is facing (1 for right, -1 for left)

    # Controls
    self.leftControl = False;
    self.rightControl = False;
    self.upControl = False;
    self.downControl = False;
    self.firstAbilityControl = False;
    self.secondAbilityControl = False;
    self.shieldControl = False;
    self.punchControl = False;

    # Attacking
    self.attackBox = None; # Finish tomorrow
    self.percentage = 0;

    # Pointer image
    self.pointerImg = pygame.image.load('assets/images/character_visuals/character_pointer.png');

    # Shield information
    self.shieldImg = pygame.image.load('assets/images/character_visuals/shield.png');
    self.shieldActive = False
    self.shieldStartTimer = 0;
    self.shieldButtonPressed = False;


  def draw(self, image = None):
    if image == None:
      pygame.draw.rect(WINDOW, (127, 127, 127), self.rect); # Draw a rectangle, showing the hitbox of the player (DEBUG FEATURE)
    else:
      flipHorizontally = True if self.direction < 0 else False
      WINDOW.blit(pygame.transform.flip(image, flipHorizontally, False), (self.x, self.y));
      maxHeight = WINDOW_SIZE[1] - 5 - self.height
      if self.x < -30 or self.x > WINDOW_SIZE[0] + 30 - self.width:
        pointerRotation = 0;
        if self.x < -30:
          pointerRotation = 180;
          imageCoords = (5, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2))))
        else:
          imageCoords = (WINDOW_SIZE[0] - 5 - self.width, min(maxHeight, max(5, self.y - ((self.pointerImg.get_height() - self.height) / 2))))
        WINDOW.blit(pygame.transform.rotate(self.pointerImg, pointerRotation), imageCoords);
        WINDOW.blit(pygame.transform.flip(pygame.transform.scale(image, (14, 14)), flipHorizontally, False), (imageCoords[0] + 9, imageCoords[1] + 9));
      if self.shieldActive:
        WINDOW.blit(self.shieldImg, (self.x - 12, self.y - 12));
    


  def update(self, game, deltaT): # Update every frame
    #self.collideWithPlatforms(game); # Check collisions with platforms
    self.updateControls();
    super().update(game, deltaT); # Call super function
    self.detectControls();
    self.updateAbilities(deltaT);

  def updateControls(self): # Detect specific keys to be tapped or pressed, determined by which side of the keyboard the player is using
    if self.playerSide == 'left':
      self.leftControl = aPressed;
      self.rightControl = dPressed;
      self.upControl = wTapped;
      self.downControl = sTapped;
      self.firstAbilityControl = nTapped;
      self.secondAbilityControl = mTapped;
      self.shieldControl = hPressed;
      self.punchControl = bTapped;
      self.ultControl = bTapped and self.xDir == 0;
    elif self.playerSide == 'right':
      self.leftControl = leftPressed;
      self.rightControl = rightPressed;
      self.upControl = upTapped;
      self.downControl = downTapped;
      self.firstAbilityControl = num2Tapped;
      self.secondAbilityControl = num3Tapped;
      self.shieldControl = num5Pressed;
      self.punchControl = num1Tapped;
      self.ultControl = num1Tapped and self.xDir == 0;

  def collideWithPlatforms(self, game):
    self.inAir = True;
    for platform in game.platforms:
      collisionInfo = util.rectangleCollision(self.rect, platform.rect)
      if collisionInfo[util.COLLIDE_BOTTOM] and self.yDir > 0:
        self.y = platform.rect.top - self.height;
        self.yDir = 0;
        self.inAir = False
        self.remainingAirJumps = self.totalAirJumps;
      if collisionInfo[util.COLLIDE_TOP] and self.yDir < 0:
        self.y -= self.yDir;
        self.yDir = 0;
      if (collisionInfo[util.COLLIDE_LEFT] and self.xDir < 0) or (collisionInfo[util.COLLIDE_RIGHT] and self.xDir > 0):
        self.x -= self.xDir;

  def detectControls(self):
    self.rect.update(self.x, self.y, self.width, self.height)
    if not self.speedLocked:
      if self.leftControl: # Move left if a is pressed
        self.direction = -1;
        if not self.inAir:
          self.xDir = -self.horizontalSpeed;
        elif self.xDir > -self.horizontalSpeed:
          self.xDir -= 0.5 / self.weight;
      elif self.rightControl: # Move right if d is pressed
        self.direction = 1;
        if not self.inAir:
          self.xDir = self.horizontalSpeed;
        elif self.xDir < self.horizontalSpeed:
          self.xDir += 0.5 / self.weight;
      elif not self.inAir: # Stop moving horizontally if none are pressed
        self.xDir = 0;
      else:
        self.xDir += 0.1 if self.xDir < 0 else -0.1;
    if self.upControl: # Jump if w is tapped
      if self.inAir and self.remainingAirJumps > 0: # If player is already in air and there are remaining double jumps left, jump again
        self.yDir = -self.jumpingPower;
        self.remainingAirJumps -= 1;
      elif not self.inAir: # Jump if on surface
        self.yDir = -self.jumpingPower;
    if self.downControl and self.inAir: # Use downwards ability if s is pressed
      self.activateDownwardsAbility();
    elif self.firstAbilityControl and self.activeAbilities['first'] == False: # Use first ability if first ability key is pressed
      self.activateFirstAbility();
    elif self.secondAbilityControl and self.activeAbilities['second'] == False: # Use second ability if second ability key is pressed
      self.activateSecondAbility();
    elif self.ultControl and self.activeAbilities['ult'] == False: # Use second ability if second ability key is pressed
      self.activateUltAbility();
    if self.punchControl:
      self.punch();
    else:
      self.attackBox = None;

    if self.shieldControl and self.xDir == 0 and self.yDir == 0 and time.time() - self.shieldStartTimer < 2 and not self.shieldButtonPressed:
      self.shieldActive = True;
    else:
      self.shieldStartTimer = time.time();
      self.shieldActive = False;
      self.shieldButtonPressed = True;
    if not self.shieldControl:
      self.shieldButtonPressed = False;
    


  def punch(self):
    if self.direction == 1:
      self.attackBox = pygame.rect.Rect(self.x + (self.width / 2), self.y - 16, (self.width / 2) + 24, self.height + 32);
    else:
      self.attackBox = pygame.rect.Rect(self.x - 24, self.y - 16, (self.width / 2) + 24, self.height + 32);


  def updateAbilities(self, deltaT):

    # FIRST ABILITY UPDATE
    if type(self.activeAbilities['first']) == list:
      if self.duringFirstAbility():
        self.activeAbilities['first'][0] -= deltaT;
        if (self.activeAbilities['first'][0] <= 0) or (self.activeAbilities['first'][1] and self.firstAbilityControl):
          self.endFirstAbility();

    # SECOND ABILITY UPDATE
    if type(self.activeAbilities['second']) == list:
      if self.duringSecondAbility():
        self.activeAbilities['second'][0] -= deltaT;
        if (self.activeAbilities['second'][0] <= 0) or (self.activeAbilities['second'][1] and self.secondAbilityControl):
          self.endSecondAbility();

    # DOWNWARDS ABILITY UPDATE
    if type(self.activeAbilities['down']) == list:
      if self.duringDownAbility():
        self.activeAbilities['down'][0] -= deltaT;
        if (self.activeAbilities['down'][0] <= 0) or (self.activeAbilities['down'][1] and self.downControl):
          self.endDownAbility();

    # ULT ABILITY UPDATE
    if type(self.activeAbilities['ult']) == list:
      if self.duringUltAbility():
        self.activeAbilities['ult'][0] -= deltaT;
        if (self.activeAbilities['ult'][0] <= 0) or (self.activeAbilities['ult'][1] and self.ultControl):
          self.endUltABility();
    

  # FIRST ABILITY:
  def activateFirstAbility(self, time = 0, endable = False):
    self.firstAbilityControl = False;
    if time > 0:
      self.activeAbilities['first'] = [time * 1000, endable];
  
  def duringFirstAbility(self):
    return False;
  
  def endFirstAbility(self):
    self.activeAbilities['first'] = False;

  # SECOND ABILITY
  def activateSecondAbility(self):
    self.secondAbilityControl = False;
  
  def duringSecondAbility(self):
    return False;
  
  def endSecondAbility(self):
    self.activeAbilities['second'] = False;
  
  # DOWNWARDS ABILITY
  def activateDownwardsAbility(self):
    self.downControl = False;
    self.yDir = 5;
  
  def duringDownAbility(self):
    return False;
  
  def endDownAbility(self):
    self.activeAbilities['down'] = False;
  
  # ULT ABILITY
  def activateUltAbility(self):
    self.ultControl = False;
    pass;
  
  def duringUltAbility(self):
    return False;
  
  def endUltABility(self):
    self.activeAbilities['ult'] = False;

  def punched(self, attacker, damage, knockbackMultiplyer = 1):
    mult = 1;
    angle = math.atan2(self.y - attacker.y, self.x - attacker.x);
    if not self.inAir:
      if angle < math.pi * (1 / 4):
        angle = math.pi * (1 / 4);
      elif angle > math.pi * (3 / 4):
        angle = math.pi * (3 / 4);
      mult = -1;
    self.xDir = (math.cos(angle) * knockbackMultiplyer * 20 * ((self.percentage // 50) + 1)) / self.weight;
    self.yDir = mult * (math.sin(angle) * knockbackMultiplyer * 20 * ((self.percentage // 50) + 1)) / self.weight;
    self.percentage += damage;



# BARREL MAN CHARACTER

class BarrelMan(Player):

  def __init__(self, game, coords, playerSide):
    super().__init__(game, coords, playerSide);
    self.image = pygame.transform.scale(pygame.image.load(
      'assets/images/characters/barrel_man/barrel_man.png'
    ), (self.width, self.height)); # Load normal image
    self.rollImage = pygame.transform.scale(pygame.image.load(
      'assets/images/characters/barrel_man/barrel_man_roll.png'
    ), (self.width, self.height)); # Load rolling image

    # First ability variables
    self.rollTimer = time.time();
  
  def draw(self):
    if self.activeAbilities['first'] != False: # Draw normal image if no abilities are used
      super().draw(self.rollImage);
    else: # Draw rolling image if an ability requiring Barrel Man to roll is used
      super().draw(self.image);

  def activateFirstAbility(self):
    if self.xDir != 0: # If there is movement on the x-plane
      super().activateFirstAbility(1.5, True); # Activate first ability
      self.xDir = (self.xDir // abs(self.xDir)) * 10; # Set speed
      self.speedLocked = True; # Lock speed
  
  def duringFirstAbility(self):
    hitPlayer = self.game.hitPlayer(self) # Find a hit player
    if hitPlayer != None: # If there is a hit player
      self.endFirstAbility(); # End the ability
      hitPlayer.punched(self, 36, 1.8); # Launch player
      return False; # Do not run the timer code
    return True;

  def endFirstAbility(self):
    super().endFirstAbility();
    self.speedLocked = False;

  def activateSecondAbility(self):
    super().activateSecondAbility();








# OBSTACLE CLASS

class Obstacle(GameObject):

  def __init__(self, game, coords, img, immunePlayer = None, timer = None):
    self.width, self.height = img.get_width(), img.get_height();
    super().__init__(coords, (self.width, self.height), img);
    self.game = game;
    self.immunePlayer = immunePlayer;
    self.timer = timer;
    self.detectHitPlayers = [];
    for player in game.players:
      if player != self.immunePlayer:
        self.detectHitPlayers.append(player);
    self.mustBeRemoved = False;
  

  def update(self, game, deltaT):
    super().update(game, deltaT);
    self.detectCollision();
  
  def detectCollision(self):
    for player in self.detectHitPlayers:
      if self.rect.colliderect(player.rect):
        self.onCollision(player);
  
  def onCollision(self, player):
    pass;

class VeryLongSword(Obstacle):

  def __init__(self, game, coords, shotBy):
    super().__init__(game, coords, pygame.image.load("assets/images/characters/barrel_man/verylongsword.png"), shotBy, 15);

# ================================================================
# ================================================================
#
#  MAIN LOOP
#
# ================================================================
# ================================================================

currMenu = MainMenu();

while True:
  pygame.display.update(); # Update display
  WINDOW.fill((0, 0, 0));
  deltaT = fpsClock.tick(60);
  
  keys = pygame.key.get_pressed(); # Get all keys pressed
  wPressed = keys[gameGlobals.K_w]; # Get certain pressed keys
  sPressed = keys[gameGlobals.K_s];
  aPressed = keys[gameGlobals.K_a];
  dPressed = keys[gameGlobals.K_d];
  mPressed = keys[gameGlobals.K_m];
  hPressed = keys[gameGlobals.K_h];
  upPressed = keys[gameGlobals.K_UP];
  downPressed = keys[gameGlobals.K_DOWN];
  leftPressed = keys[gameGlobals.K_LEFT];
  rightPressed = keys[gameGlobals.K_RIGHT];
  num3Pressed = keys[gameGlobals.K_KP3];
  num5Pressed = keys[gameGlobals.K_KP5];
  wTapped, sTapped, upTapped, downTapped, leftTapped, rightTapped, spaceTapped, keyTapped = False, False, False, False, False, False, False, False; # Set tapped keys to be false

  # Player 1 tapped keys
  bTapped, nTapped, mTapped = False, False, False;

  # Player 2 tapped keys
  num1Tapped, num2Tapped, num3Tapped = False, False, False;
  
  for event in pygame.event.get():
    if event.type == gameGlobals.QUIT: # If the user wants to quit game, shut down python and system operations
      pygame.quit();
      sys.exit();
    elif event.type == gameGlobals.KEYDOWN: # If the key is down
      keyTapped = True; # Show that a key is tapped
      if event.key == pygame.K_w: # If a certain key is tapped, set that variable to show that the key is tapped
        wTapped = True;
      elif event.key == pygame.K_s:
        sTapped = True;
      elif event.key == pygame.K_UP:
        upTapped = True;
      elif event.key == pygame.K_DOWN:
        downTapped = True;
      elif event.key == pygame.K_LEFT:
        leftTapped = True;
      elif event.key == pygame.K_RIGHT:
        rightTapped = True;
      elif event.key == pygame.K_SPACE:
        spaceTapped = True;
        
      if event.key == pygame.K_b:
        bTapped = True;
      elif event.key == pygame.K_n:
        nTapped = True;
      elif event.key == pygame.K_m:
        mTapped = True;
        
      if event.key == pygame.K_KP1:
        num1Tapped = True;
      elif event.key == pygame.K_KP2:
        num2Tapped = True;
      elif event.key == pygame.K_KP3:
        num3Tapped = True;
      


  currMenu.update(deltaT);
      

      # LAST UPDATED: MAY 18 10:27AM