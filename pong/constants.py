from math import ceil

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Time since last logic update
DELTATIME = 5 # In milliseconds; 5 ms = physics update @ 200 Hz

WALL_THICKNESS = 4

GAMEAREA_WIDTH = ceil(WINDOW_WIDTH * 0.95)
GAMEAREA_HEIGHT = ceil(WINDOW_HEIGHT * 0.9)
GAMEAREA_X = ceil((WINDOW_WIDTH / 2.0) - (GAMEAREA_WIDTH / 2.0))
GAMEAREA_Y = ceil((WINDOW_HEIGHT - GAMEAREA_HEIGHT - (WALL_THICKNESS / 2.0)))
 
GAME_FPS = 120.0
GAME_SPEED = 1
 
STATE_MAINMENU = 1
STATE_GAME = 2
STATE_CHOOSEMODE = 3
STATE_PAUSE = 4

ACTION_NEWGAME = 1
ACTION_QUIT = 2
ACTION_MODE1P = 3
ACTION_MODE2P = 4

GAMEOBJECT_PADDLE = 1
GAMEOBJECT_BALL = 2
GAMEOBJECT_WALL = 3

PLAYER_ONE = 0
PLAYER_TWO = 1

DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

BALL_BOUNCESPEEDUP = 25 # How many bounces it takes to double the speed of the ball
BALL_STARTINGSPEED = GAMEAREA_WIDTH * 0.005
PADDLE_STARTINGSPEED = GAMEAREA_HEIGHT * 0.003

BALL_COLOR = BLUE
PADDLE_COLOR = BLACK
WALL_COLOR = RED

PADDLE_THICKNESS = 3
PADDLE_HEIGHT = ceil(GAMEAREA_HEIGHT * 0.20)
PADDLE_WIDTH = ceil(PADDLE_HEIGHT * 0.15)

BALL_THICKNESS = 0
BALL_SIZE = 10