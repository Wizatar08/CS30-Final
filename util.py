import math

# Variables used to see which side something collides on
COLLIDE = 0;
COLLIDE_TOP = 1;
COLLIDE_BOTTOM = 2;
COLLIDE_RIGHT = 3;
COLLIDE_LEFT = 4;

def rectangleCollision(rect1, rect2):
  if rect1.right >= rect2.left and rect1.left <= rect2.right and rect1.bottom >= rect2.top and rect1.top <= rect2.bottom:
    deltaBottom = abs(rect1.top - rect2.bottom)
    deltaTop = abs(rect1.bottom - rect2.top)
    deltaRight = abs(rect1.right - rect2.left)
    deltaLeft = abs(rect1.left - rect2.right)
    lowestDelta = min(deltaTop, deltaBottom, deltaLeft, deltaRight);
    if lowestDelta == deltaBottom:
      return True, True, False, False, False
    elif lowestDelta == deltaTop:
      return True, False, True, False, False
    elif lowestDelta == deltaRight:
      return True, False, False, True, False
    elif lowestDelta == deltaLeft:
      return True, False, False, False, True
  return False, False, False, False, False


def rectangleCircleCollision(rect, circle):
    rectCenterX = rect.x + (rect.width / 2) # Get the center of the rectangle
    rectCenterY = rect.y + (rect.height / 2)

    centerDistanceX = abs(circle.x - rectCenterX) # Get the distances, in x and y pieces, of the distance between the center of the rectangle and the circle
    centerDistanceY = abs(circle.y - rectCenterY)

    if centerDistanceX > rect.width / 2 + circle.radius or centerDistanceY > rect.height / 2 + circle.radius: # If the horizontal or vertical distances are greater than the horizontal or vertical radii (circles) plus half-dimensions (rect)
        return False # Return false
    if centerDistanceX <= rect.width / 2 or centerDistanceY <= rect.height / 2: # If their radii/half distances are touching, return True
        return True
    rectCornerX = centerDistanceX - rect.width / 2 # Get corner coords or rectangle
    rectCornerY = centerDistanceY - rect.height / 2
    cornerDistance = math.sqrt(rectCornerX ** 2 + rectCornerY ** 2) # Get distance between circle and nearest rect corner coords
    return cornerDistance <= circle.radius # If distance is within corner coord distance, return true, otherwise return false

class Circle:
   
   def __init__(self, coords, radius):
      self.x, self.y = coords
      self.radius = radius

class CircularExplosion:
   
   def __init__(self, radius, animatedImg):
      self.x, self.y = 0, 0 # Create center coords variables (this will be changed later)
      self.radius = radius # Radius
      self.image = animatedImg # Explosion animation image
      self.isExploding = False # If the explosion is exploding
      self.explosionCircle = None # If there is an explosion circle
      self.atEnd = False # If the explosion is done
      self.currentlyHitObjects = [] # Explosion's currently hit objects

   def startExplosion(self, centerCoords):
      self.x = centerCoords[0] # Set coords
      self.y = centerCoords[1]
      self.image.x = self.x - self.radius # Set image coords
      self.image.y = self.y - self.radius
      self.image.scale((self.radius * 2, self.radius * 2)) # Scale animation
      self.isExploding = True # Say that this is explosing
      self.explosionCircle = Circle((self.x, self.y), self.radius) # Create circle

   def update(self):
      if self.image.frame == self.image.lastFrame: # If the explosion image frame is at the last one, say that the explosion has ended
        self.atEnd = True
   
   def draw(self):
      if self.isExploding: # update the image if the explosion is happening
        self.image.update()

   def hitGameObject(self, gameObject):
      if self.explosionCircle != None: # If the collision circle exists
        if rectangleCircleCollision(gameObject.rect, self.explosionCircle) and not gameObject in self.currentlyHitObjects: # If an object is in the explosion circle, append to the recently touched list and return true
          self.currentlyHitObjects.append(gameObject)
          return True
        elif not rectangleCircleCollision(gameObject.rect, self.explosionCircle) and gameObject in self.currentlyHitObjects: # If an object is no longer in the explosion radius, remove it from the list
          self.currentlyHitObjects.remove(gameObject)
      return False # Return False
   
   