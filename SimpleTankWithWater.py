import curses
from SimpleTank import SimpleTank

# TODO

class SimpleTankWithWater(SimpleTank):
  def __init__(self, x, y, grnd, grndColor, watColor, percentWater, c):
    SimpleTank.__init__(self, x, y, grnd, grndColor)
    self.waterColor = watColor
    self.waterX = x*percentWater/100
    self.colorless = c

  def drawGround(self, window):
    for i in range(0, self.termX):
      for j in range(0, self.termY-1):
        # Check if current index is a ` and skip it
        if window.instr(j, i, 1) == "`":
          if self.colorless:
            window.addstr(j, i, " ")
          else:
            window.addstr(j, i, " ", curses.color_pair(0))
        # If the current index is a character that isn't `, then it is important, skip it
        elif window.instr(j,i, 1) != " ":
          continue
        else:
          # If it's air, replace it with air
          if j < self.groundLevel:
            if self.colorless:
              window.addstr(j, i, " ")
            else:
              window.addstr(j,i, " ", curses.color_pair(0))
          # Else if it is water, color it water
          elif i <= self.waterX:
            if self.colorless:
              window.addstr(j, i, " ")
            else:
              window.addstr(j,i, " ", curses.color_pair(self.waterColor))
          # Else it is ground, color it ground
          else:
            if self.colorless:
              window.addstr(j, i, " ")
            else:
              window.addstr(j,i, " ", curses.color_pair(self.groundColor))

  def changeAnimalCoords(self, animX, animY, animLen, animHeight, animDir):
    if animDir == "right":
      # If animal is in water approaching edge of water
      if animX+animLen == self.waterX-1:
        # If there are only 2 spaces of animal or less under water, they can
        # get out of the water
        if animY + animHeight - 3 <= self.groundLevel:
          return 0, self.groundLevel-(animY + animHeight), "grnd"
        else:
          return -1, 0, "water"
      # If animal is approaching edge of map
      elif animX + animLen == self.termX-1:
        return -1, 0, "grnd"
      else:
        if animX + animLen < self.waterX-1:
          return 0,0,"water"
        else:
          return 0,0,"grnd"
    # If animal is moving left
    elif animDir == "left":
      # If animal is approaching edge of map:
      if animX == 1:
        #If they're approaching the edge they just need to stop
        return -1,0,"water"
      # If they are approaching the water and need to go down
      elif animX + animLen == self.waterX:
        return 0, 2, "water"
      else:
        # If in water
        if animX + animLen < self.waterX-1:
          return 0,0, "water"
        else:
          return 0,0, "grnd"
    # If animal is moving up (wether or not they can move up physically
    # is determined by the animal's class)
    elif animDir == "up":
      # If the animal is about to go above max terminal height
      #if animY == self.termY-1:
      if animY-1 == 1:
        return 0,-512, "air"
      # If animal would be walking on the water
      elif animY+animHeight-1 == self.groundLevel:
        return 0,-512, "water"
      # Else animal is just swimming or flying up into legal space
      elif animY-1 <= self.groundLevel:
        return 0,0,"water"
      elif animY-1 > self.groundLevel:
        return 0,0,"air"
    # If animal is moving down
    elif animDir == "down":
      # If the animal is about to go below minimum height:
      if animY + animHeight > self.termY - 2:
        return 0,-512, "water"
      # If the animal moving down in water or flying into water:
      elif animY + animHeight >= self.groundLevel:
        return 0,0, "water"
      # Else just moving down in air
      elif animY + animHeight < self.groundLevel:
        return 0,0, "air"

