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
    rectCenterX = rect.x + (rect.width / 2)
    rectCenterY = rect.y + (rect.height / 2)

    centerDistanceX = abs(circle.x - rectCenterX)
    centerDistanceY = abs(circle.y - rectCenterY)

    if centerDistanceX > rect.width / 2 + circle.radius or centerDistanceY > rect.height /2 + circle.radius:
        return False
    if centerDistanceX <= rect.width / 2 or centerDistanceY <= rect.height / 2:
        return True
    rectCornerX = centerDistanceX - rect.width / 2
    rectCornerY = centerDistanceY - rect.height / 2
    cornerDistance = math.sqrt(rectCornerX ** 2 + rectCornerY ** 2)
    return cornerDistance <= circle.radius

class Circle:
   
   def __init__(self, coords, radius):
      self.x, self.y = coords
      self.radius = radius