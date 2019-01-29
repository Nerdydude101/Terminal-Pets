import curses

class SimpleTank:
  def __init__(self, x, y, grnd, grndColor):
    self.termX = x
    self.termY = y
    self.groundLevel = grnd
    self.groundColor = grndColor

  def drawGround(self, window):
    for i in range(0, self.termX):
      for j in range(self.groundLevel, self.termY-1):
        window.addstr(j,i, " ", curses.color_pair(self.groundColor))


  '''
    Input: The animal's leading X and Y values, not their drawing values
           but the values of their frontmost X and Y based on direction
           The Animal's Length
           The Animal's Height
           The Animal's direction
    Output: X-change:
             -1 uf turranin can't be surpassed
            Y -change:
              -512 if invalid
            Terrain Type:
              indicates what the new terrain is
  '''
  def changeAnimalCoords(self, animX, animY, animLen, animHeight, animDir):
    if animDir == "right":
      if animX == self.termX-1:
        return -1.0, "grnd"
      else:
        return 0,0, "grnd"
    elif animDir == "left":
      if animX == 1:
        return -1,0, "grnd"
      else:
        return 0,0,"grnd"
    elif animDir == "up":
      if animY <= 1:
        return 0,-512,"air"
      else:
        if animY+animHeight == self.groundLevel-1:
          return 0,0,"grnd"
        else:
          return 0,0,"air"
    elif animDir == "down":
      if animY+animHeight == self.groundLevel-1:
        return 0,0,"grnd"
      elif animY_animHeight <= self.groundLevel:
        return 0,-512,"grnd"
      else:
        return 0,0,"air"
