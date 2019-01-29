import termios, fcntl, os, struct, time, sys, random
import curses
from curses import wrapper
from Turtle import Turtle
from SimpleTank import SimpleTank
from SimpleTankWithWater import SimpleTankWithWater

def getTerminalSize():
  fd = open(os.ctermid(), 'r')
  packed = fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
  rows, cols, h_pixels, v_pixels = struct.unpack('HHHH', packed)
  return rows, cols

def main(stdscr):
  curses.curs_set(0)
  curses.start_color()
  curses.use_default_colors()
  stdscr.nodelay(True)
  colorless = False

  # Check for disable color
  for arg in sys.argv[1:]:
    if arg == "colorless":
      colorless = True

  # Initialize color pairs
  '''
    0-128 are for text color
    129-244 are for background color
    245-255 are dynamic based on what the program needs for merging
  '''
  for i in range(0, curses.COLORS/2):
    curses.init_pair(i+1, 2*i, -1)
  for i in range(0, (curses.COLORS/2)-11):
    curses.init_pair(i+1+(curses.COLORS/2), 0, 2*i)

  random.seed(time.time())

  rows, cols = getTerminalSize()
  grid = [[" " for y in range(0, cols)] for x in range(0, rows)]
  animalX = cols/2
  animalY = rows-12
  # rows, cols
#  turtle = Turtle(animalX, animalY-6, "turtle", colorless)
  turtle = Turtle(animalX, animalY, "turtle", colorless)
  if colorless is True:
    tank = SimpleTankWithWater(cols, rows, animalY + len(turtle.getArr()), 155, 132, 0, colorless)
  else:
    tank = SimpleTankWithWater(cols, rows, animalY + len(turtle.getArr()), 155, 132, 50, colorless)
  while True:
    # Draw animals then tank so that tank will fill blank space of animals
    turtle.getAction(rows, cols, tank, stdscr)
    tank.drawGround(stdscr)
    # Refresh screen
    stdscr.refresh()
    time.sleep(1)
    # Check for feeding animal
    input = stdscr.getch()
    if input == ord("f"):
      turtle.feed()
      input = ''

wrapper(main)

