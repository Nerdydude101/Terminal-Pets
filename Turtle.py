import random, time, curses

#TODO
# Swimming
#
#
# test output: 
#       self.x.write(dir+"\n")



class Turtle:
  # Constant Variables
  DEFAULT_TURTLE = ["  ______    ____ ",\
                    " /\____/\  |``o`|",\
                    "|_/````\_|/`___\|",\
                    "|_\____/_|/",\
                    "|_|_| |_|_|      "]
  LEFT_TURTLE =    [" ____    ______  ",\
                    "|`o``|  /\____/\ ",\
                    "|/___`\|_/````\_|",\
                    "      \|_\____/_|",\
                    "      |_|_| |_|_|"]


  def __init__(self, startX, startY, n, c):

    # Self Variable Declaration
    self.x = open("outputTest.txt", "w")
    self.idleState = 0
    self.sleepState = 0
    self.eatState = 0
    self.actionQueue = []
    self.curTerrain = "grnd"
    self.orientation = "right"
    self.lastMove = 0
    self.turtName = n
    self.turtArr = self.DEFAULT_TURTLE
    self.turtX = startX
    self.turtY = startY
    self.colorless = c

  # This function sets the turtle to its default turtle based
  # on direction
  def default(self):
    if self.orientation == "right":
      self.turtArr = self.DEFAULT_TURTLE
    else:
      self.turtArr = self.LEFT_TURTLE

  # This function removes the turtle from the curses window, does not refresh
  def removeTurtle(self, window):
    for y in range(0, len(self.turtArr)):
      for x in range(0, len(self.turtArr[y])):
        window.addch(self.turtY + y, self.turtX + x, " ")

  # Draws turtle to curses window, does not refresh
  def drawTurtle(self, window):
    for y in range(0, len(self.turtArr)):
      for x in range(0, len(self.turtArr[y])):
        if self.colorless:
          window.addch(self.turtY + y, self.turtX + x, self.turtArr[y][x])
        else:
          window.addch(self.turtY + y, self.turtX + x, self.turtArr[y][x], curses.color_pair(18))

  # Sets movement variables to 0 and resets turtle between actions
  def transition(self, window):
    self.lastMove = 0
    self.idleState = 0
    self.sleepState = 0
    self.removeTurtle(window)
    self.default()
    self.drawTurtle(window)

  # Change the current direction of turtle
  def changeDir(self, dir):
    if dir == "left" or dir == "right":
      self.setDir(dir)

  # Perform the Idle action
  def idleTurtle(self, window):
    self.removeTurtle(window)
    self.idleAnimation()
    self.drawTurtle(window)

  # Perform the Sleep action
  def sleepTurtle(self, window):
    self.removeTurtle(window)
    self.sleepAnimation()
    self.drawTurtle(window)

  # Perform a move action
  def moveTurtle(self, dir, mvX, mvY, window):
    # Remove before changes to XY values happen so that I don't have to do
    # weird removels like I had to in the previous version
    self.removeTurtle(window)
    self.turtX += mvX; self.turtY += mvY
    if self.getDir() != dir:
      self.changeDir(dir)
    if dir == "left":
      self.turtX += -1
    elif dir == "right":
      self.turtX += 1
    elif dir == "up":
      self.turtY += -1
    else:
      self.turtY += 1

    # Generate motion-animated turtle
    if self.curTerrain == "grnd":
      self.moveAnimation()
    else:
      self.swimAnimation()
    # Draw new animated turtle
    self.drawTurtle(window)

  # Change the Turtle array for animation of move action
  def moveAnimation(self):
    if self.orientation == "right":
      # Alternate through 4 steps
      if self.lastMove == 0:
        self.lastMove = 1
        self.turtArr[4] = "|_| |_|_|_|      "
      elif self.lastMove == 1:
        self.lastMove = 2
        self.turtArr[4] = "|_|_| |_|_|      "
      elif self.lastMove == 2:
        self.lastMove = 3
        self.turtArr[4] =  "|_|_|_| |_|      "
      elif self.lastMove == 3:
        self.lastMove = 0
        self.turtArr[4] =  "|_|_| |_|_|      "
    elif self.orientation == "left":
      # Alternate through 4 steps
      if self.lastMove == 0:
        self.lastMove = 1
        self.turtArr[4] = "      |_|_|_| |_|"
      elif self.lastMove == 1:
        self.lastMove = 2
        self.turtArr[4] = "      |_|_| |_|_|"
      elif self.lastMove == 2:
        self.lastMove = 3
        self.turtArr[4] = "      |_| |_|_|_|"
      elif self.lastMove == 3:
        self.lastMove = 0
        self.turtArr[4] = "      |_|_| |_|_|"
    return self.turtArr

  # Animate the turtle array for swimming
  def swimAnimation(self):
    if self.orientation == "right":
      # Alternate through 3 animation steps
      if self.lastMove == 0:
        self.turtArr[4] = "|_|_| |_|_|      "
        self.lastMove = 1
      elif self.lastMove == 1:
        self.turtArr[4] = "|_|_|_|_|        "
        self.lastMove = 2
      else:
        self.turtArr[4] = "  |_|_|_|_|      "
        self.lastMove = 1
    else:
      # Alternate through 3 animation steps
      if self.lastMove == 0:
        self.turtArr[4] = "      |_|_| |_|_|"
        self.lastMove = 1
      elif self.lastMove == 1:
        self.turtArr[4] = "        |_|_|_|_|"
        self.lastMove = 2
      else:
        self.turtArr[4] = "      |_|_|_|_|  "
        self.lastMove = 1
    return self.turtArr

  # Animate the turtle array for Idle action
  def idleAnimation(self):
    if self.orientation == "right":
      # Should alternate between this predefined low-head and default.
      #  TODO
      #  for some reason instead of default it changes it to a standing turtle
      #  with legs moved from move actions.
      if self.curTerrain == "grnd":
        if self.idleState == 0:
          self.turtArr = ["  ______         ",\
                          " /\____/\   ____ ",\
                          "|_/````\_|_|``o`|",\
                          "|_\____/_|_____\|",\
                          "|_|_| |_|_|      "]
          self.idleState = 1
        else:
          self.turtArr = self.DEFAULT_TURTLE
          self.idleState = 0
      elif self.curTerrain == "water":
        if self.idleState == 0:
          self.turtArr = ["  ______    ____ ",\
                          " /\____/\  |``o`|",\
                          "|_/````\_|/`___o|",\
                          "|_\____/_|/    o ",\
                          "|_|_| |_|_|      "]
          self.idleState = 1
        elif self.idleState == 1:
          self.turtArr = ["  ______    ____ ",\
                          " /\____/\  |``o`|",\
                          "|_/````\_|/`___\|",\
                          "|_\____/_|/      ",\
                          "|_|_| |_|_|      "]
          self.idleState = 2
        elif self.idleState == 2:
          self.turtArr = ["  ______    ____ ",\
                          " /\____/\ o|``o`| ",\
                          "|_/````\_|/`___\|",\
                          "|_\____/_|/      ",\
                          "|_|_| |_|_|      "]
          self.idleState = 3
        elif self.idleState == 3:
          self.turtArr = ["  ______ o  ____ ",\
                          " /\____/\  |``o`|",\
                          "|_/````\_|/`___\|",\
                          "|_\____/_|/      ",\
                          "|_|_| |_|_|      "]
          self.idleState = 4
        elif self.idleState == 4:
          self.turtArr = ["  ______    ____ ",\
                          " /\____/\  |``o`|",\
                          "|_/````\_|/`___\|",\
                          "|_\____/_|/      ",\
                          "|_|_| |_|_|      "]
          self.idleState = 0
    else:
      if self.curTerrain == "grnd":
        if self.idleState == 0:
          self.turtArr = ["         ______  ",\
                          " ____   /\____/\ ",\
                          "|`o``|_|_/````\_|",\
                          "|/_____|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 1
        else:
          self.turtArr = self.LEFT_TURTLE
          self.idleState = 0
      elif self.curTerrain == "water":
        if self.idleState == 0:
          self.turtArr = [" ____    ______  ",\
                          "|`o``|  /\____/\ ",\
                          "|o___`\|_/````\_|",\
                          " o    \|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 1
        elif self.idleState == 1:
          self.turtArr = [" ____    ______  ",\
                          "|`o``|  /\____/\ ",\
                          "|/___`\|_/````\_|",\
                          "      \|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 2
        elif self.idleState == 2:
          self.turtArr = [" ____    ______  ",\
                          "|`o``|o /\____/\ ",\
                          "|/___`\|_/````\_|",\
                          "      \|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 3
        elif self.idleState == 3:
          self.turtArr = [" ____  o ______  ",\
                          "|`o``|  /\____/\ ",\
                          "|/___`\|_/````\_|",\
                          "      \|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 4
        elif self.idleState == 4:
          self.turtArr = [" ____    ______  ",\
                          "|`o``|  /\____/\ ",\
                          "|/___`\|_/````\_|",\
                          "      \|_\____/_|",\
                          "      |_|_| |_|_|"]
          self.idleState = 0

  # Animate tutrle array for Sleep action
  def sleepAnimation(self):
    if self.sleepState == 0:
      self.turtArr = ["                 ",\
                      "      ______     ",\
                      "     /\____/\Z   ",\
                      "    |_/````\_|   ",\
                      "    |_\____/_|   "]
      self.sleepState = 1
    elif self.sleepState == 1:
      self.turtArr = ["                 ",\
                      "      ______  Z  ",\
                      "     /\____/\    ",\
                      "    |_/````\_|   ",\
                      "    |_\____/_|   "]
      self.sleepState = 2
    elif self.sleepState == 2:
      self.turtArr = ["               Z ",\
                      "      ______     ",\
                      "     /\____/\    ",\
                      "    |_/````\_|   ",\
                      "    |_\____/_|   "]
      self.sleepState = 0

  # animate turtle array for Feed action
  def feedAnimation(self):
    if self.orientation == "right":
      if self.eatState == 0:
        self.turtArr = self.DEFAULT_TURTLE
        self.eatState = 1
      elif self.eatState == 1:
        self.turtArr = ["  ______         ",\
                        " /\____/\   ____ ",\
                        "|_/````\_|_|``-`|",\
                        "|_\____/_|_____O|",\
                        "|_|_| |_|_|      "]
        self.eatState = 2
      elif self.eatState == 2:
        self.turtArr = ["  ______         ",\
                        " /\____/\   ____ ",\
                        "|_/````\_|_|``o`|",\
                        "|_\____/_|_____\|",\
                        "|_|_| |_|_|      "]
        self.eatState = 1
    elif self.orientation == "left":
      if self.eatState == 0:
        self.turtArr = [" ____    ______  ",\
                        "|`o``|  /\____/\ ",\
                        "|/___`\|_/````\_|",\
                        "      \|_\____/_|",\
                        "      |_|_| |_|_|"]
        self.eatState = 1
      elif self.eatState == 1:
        self.turtArr = ["         ______  ",\
                        " ____   /\____/\ ",\
                        "|`-``|_|_/````\_|",\
                        "|O_____|_\____/_|",\
                        "      |_|_| |_|_|"]
        self.eatState = 2
      elif self.eatState == 2:
        self.turtArr = ["         ______  ",\
                        " ____   /\____/\ ",\
                        "|`o``|_|_/````\_|",\
                        "|/_____|_\____/_|",\
                        "      |_|_| |_|_|"]
        self.eatState = 1

  # Draw food for the feed action
  def drawFood(self, window):
    if self.orientation == "right":
      if self.colorless:
        window.addstr(self.turtY+3, self.turtX+len(self.turtArr[3]), "/##\\")
        window.addstr(self.turtY+4, self.turtX+len(self.turtArr[3]), "\##/")
      else:
        window.addstr(self.turtY+3, self.turtX+len(self.turtArr[3]), "/##\\", curses.color_pair(42))
        window.addstr(self.turtY+4, self.turtX+len(self.turtArr[3]), "\##/", curses.color_pair(42))
    elif self.orientation == "left":
      if self.colorless:
        window.addstr(self.turtY + 3,self.turtX-4, "/##\\")
        window.addstr(self.turtY+4, self.turtX-4, "\##/")
      else:
        window.addstr(self.turtY + 3,self.turtX-4, "/##\\", curses.color_pair(42))
        window.addstr(self.turtY+4, self.turtX-4, "\##/", curses.color_pair(42))

  # Remove food from eat action
  def removeFood(self, window):
    if self.orientation == "right":
      window.addstr(self.turtY+3, self.turtX+len(self.turtArr[3]), "    ")
      window.addstr(self.turtY+4, self.turtX+len(self.turtArr[3]), "    ")
    elif self.orientation == "left":
      window.addstr(self.turtY+3,self.turtX-4, "    ")
      window.addstr(self.turtY+4,self.turtX-4, "    ")

  # Perform Feed action
  def feedTurtle(self, window):
    self.removeTurtle(window)
    self.feedAnimation()
    self.drawFood(window)
    self.drawTurtle(window)

  # Manages and executes the Action queue
  def getAction(self, rows, cols, biome, window):
    # Whenever the queue gets smaller than 10 moves, generate more moves
    if len(self.actionQueue) < 10:
      for i in range(0, 20):
        # random int for selecting type of action
        tmp = random.randint(0, 11)
        tmp2 = -1
        if tmp <= 3:
          # generate random number of steps for this action
          tmp2 = random.randint(5, 20)
          # add value to the queue
          self.actionQueue += [["mvr", tmp2]]
          # add transition step to the queue
          self.actionQueue += [["tr"]]
        elif tmp <= 6:
          # generate random number of steps for this action
          tmp2 = random.randint(5, 20)
          # add action and number of performances to queue
          self.actionQueue += [["mvl", tmp2]]
          # add transition to queue
          self.actionQueue += [["tr"]]
        elif tmp <= 9:
          # generate random number of steps for this action
          tmp2 = random.randint(5, 30)
          # add action and number of performances to queue
          self.actionQueue += [["idl", tmp2]]
          # add transition step to queue
          self.actionQueue += [["tr"]]
        elif tmp <= 11:
          # generate random number of performances for this action
          tmp2 = random.randint(5, 30)
          # add action and number of performances to queue
          self.actionQueue += [["slp", tmp2]]
          # add transition step to queue
          self.actionQueue += [["tr"]]

          #======================
          # QUEUE INJECTION SITE
          #self.actionQueue = [["mvl", 40]] + self.actionQueue
          #======================
    # If the action Queue is > 10 and turtle is in water, sometimes make him go up or down
    if self.curTerrain == "water":
      tmp = random.randint(0, 30)
      if tmp <= 3:
        self.actionQueue = [["mvup", 1], ["tr"]] + self.actionQueue
      elif tmp <= 6:
        self.actionQueue = [["mvdown", 1], ["tr"]] + self.actionQueue
    # If/When actionQueue is > 10, do next item in queue
    if self.actionQueue[0][0] == "mvr":
      # Check to make sure movement stays in bounds, else idle
      dX, dY, chgTer = biome.changeAnimalCoords(self.turtX, self.turtY, len(self.turtArr[0]), len(self.turtArr), "right")
      if dX != -1:
        self.curTerrain = chgTer
        self.moveTurtle("right", dX, dY, window)
      else:
        self.idleTurtle(window)
      # If there is more than 1 move left in this action, subtract 1 from
      # performances left to perform
      if self.actionQueue[0][1] > 1:
        self.actionQueue[0][1] -= 1
      # Else remove action from queue
      else:
        self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "mvl":
      dX, dY, chgTer = biome.changeAnimalCoords(self.turtX, self.turtY, len(self.turtArr[0]), len(self.turtArr), "left")
      # Check to make sure movement stays in bounds, else idle
      if dX != -1:
        self.curTerrain = chgTer
        self.moveTurtle("left", dX, dY, window)
      else:
        self.idleTurtle(window)
      # If there are performances left, subtract one
      if self.actionQueue[0][1] > 1:
        self.actionQueue[0][1] -= 1
      # If this is last performance, remove action from queue
      else:
        self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "mvup":
      dX, dY, chgTer = biome.changeAnimalCoords(self.turtX, self.turtY, len(self.turtArr[0]), len(self.turtArr), "up")
      # Check bounds, else idle
      if dY != -512:
        self.curTerrain = chgTer
        self.moveTurtle("up", dX, dY, window)
        # Always remove because i only generate them in sets of 1
      else:
        self.idleTurtle(window)
      self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "mvdown":
      dX, dY, chgTer = biome.changeAnimalCoords(self.turtX, self.turtY, len(self.turtArr[0]), len(self.turtArr), "down")
      # Check bounds, else idle
      if dY != -512:
        self.curTerrain = chgTer
        self.moveTurtle("down", dX, dY, window)
        # Always remove because i only generate them in sets of 1
      else:
        self.idleTurtle(window)
      self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "idl":
      self.idleTurtle(window)
      # If there are performances left, subtract one
      if self.actionQueue[0][1] > 1:
        self.actionQueue[0][1] -= 1
      # If this is the last performance, remove from queue
      else:
        self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "tr":
      self.transition(window)
      self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "slp":
      if self.curTerrain != "water":
        self.sleepTurtle(window)
      else:
        self.idleTurtle(window)
      # If there are preformances left, subtract one
      if self.actionQueue[0][1] > 1:
        self.actionQueue[0][1] -= 1
      # If this is the last performance, remove from queue
      else:
        self.actionQueue = self.actionQueue[1:]
    elif self.actionQueue[0][0] == "eat":
      # Make sure that adding the food on the proper side of the turtle won't go out of bounds.
      if self.orientation == "right" and self.turtX + len(self.turtArr[0]) + 4 > cols:
        self.changeDir("left")
      # Make sure that adding the food on the proper side of the turtle won't go out of bounds.
      elif self.orientation == "left" and self.turtX - 4 < 0:
        self.changeDir("right")
      # If there are performances left, subtract one
      if self.actionQueue[0][1] > 1:
        self.feedTurtle(window)
        self.actionQueue[0][1] -= 1
      # If there are no performances left, remove action from queue
      else:
        self.removeFood(window)
        self.transition(window)
        self.actionQueue = self.actionQueue[1:]

  # Perform Feed action
  def feed(self):
    self.actionQueue = [self.actionQueue[0]] + [["eat",10]] + self.actionQueue[1:]

  def getMaxLen(self):
    t = 0
    for i in len(self.turtArr):
      if len(i) > t:
        t = len(i)
    return t


  def setDir(self, ori):
    self.orientation = ori
    if ori == "right":
      self.turtArr = self.DEFAULT_TURTLE
    elif ori == "left":
      self.turtArr = self.LEFT_TURTLE

  def getArr(self):
    return self.turtArr
  def getDir(self):
    return self.orientation
