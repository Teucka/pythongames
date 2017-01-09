from math import ceil, floor

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (95, 95, 0)
GRAY = (95, 95, 95)
 
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Time since last logic update
DELTATIME = 5 # In milliseconds; 5 ms = physics update @ 200 Hz

LEVEL_WIDTH = 10
LEVEL_HEIGHT = 10

WALL_THICKNESS = 6

GAMEAREA_WIDTH = ceil(WINDOW_WIDTH * 0.95)
GAMEAREA_HEIGHT = ceil(WINDOW_HEIGHT * 0.9)
GAMEAREA_X = ceil((WINDOW_WIDTH / 2.0) - (GAMEAREA_WIDTH / 2.0))
GAMEAREA_Y = ceil((WINDOW_HEIGHT - GAMEAREA_HEIGHT - (WALL_THICKNESS / 2.0)))

GAME_SPEED = 2.0
GAME_STARTINGSHIPS = 3
GAME_SCOREEXTRASHIP = 1000 # How many points is needed for an extra ship
GAME_STARTINGASTEROIDS = 10 # How many asteroids there are in level 1
GAME_ASTEROIDMINSPEED = 0.15
GAME_ASTEROIDMAXSPEED = 1.0
GAME_SHIELDDURATION = 2.5

BULLET_SPEED = 6.0
BULLET_TIMETOLIVE = 5.0 # How many seconds bullets stay on screen

SHIP_MAXSPEED = 3.0
SHIP_SHOOTDELAY = 0.5 # How often can the ship shoot (in seconds)

STATE_MAINMENU = 1
STATE_GAME = 2
STATE_PAUSE = 3
STATE_GAMEOVER = 4
STATE_VICTORY = 5

ACTION_NEWGAME = 1
ACTION_QUIT = 2

GAMEOBJECT_SHIP = 1
GAMEOBJECT_WALL = 2
GAMEOBJECT_ASTEROID = 3
GAMEOBJECT_BULLET = 4

DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

SHIP_SPEED = 0.5

SHIP_WIDTH = 10
SHIP_HEIGHT = 15

ASTEROID_COLOR = BLACK
SHIP_COLOR = BROWN
WALL_COLOR = RED
BULLET_COLOR = BLUE
SHIELD_COLOR = GREEN

ASTEROID_THICKNESS = 0
ASTEROID_SIZE = 15

BULLET_THICKNESS = 0
BULLET_SIZE = 2

SHIELD_THICKNESS = 3

SHAPE_RECT = 1
SHAPE_CIRCLE = 2
SHAPE_SHIP = 3