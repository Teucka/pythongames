import constants
import pygame
import menu
import shape
import gameobject
from math import ceil, floor, sqrt
import os.path #os.path.isfile
import time

currentMilliseconds = lambda: int(round(time.time() * 1000))

# Setup
pygame.init()
pygame.display.set_caption("Arkanoid")
pygame.mouse.set_visible(0)


class Game:
	font = pygame.font.SysFont('Calibri', 25, True, False)
	screen = pygame.display.set_mode([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT])
	
	clock = pygame.time.Clock()
	# Game state (main menu, game...) todo: pause
	state = constants.STATE_MAINMENU
	# Text items
	texts = []
	currentTexts = []
	# Menus
	menus = []
	menuSelection = 0
	currentMenu = None
	# Shapes
	shapes = []
	# Main loop while not done
	done = False
	# List of all paddle game objects
	paddles = []
	# List of all ball game objects
	balls = []
	# Wall (game area) game object
	wall = None
	# Store all key presses
	keys = [0] * 500
	# Game score
	score = 0
	# How many players
	numPlayers = 1
	
	# ARKANOID STUFF
	level = []
	bricks = []
	bricksLeft = 0
	powerUps = []
	levelNow = 1
	ballsLeft = constants.GAME_STARTINGBALLS
	extraBallsGiven = 0

	
def initGame():
	# Create "main menu" selectable menu items
	mMenu = menu.Selectable(Game.font, Game.screen)
	mMenuItem = menu.SelectableItem("New Game", constants.ACTION_NEWGAME)
	mMenu.addItem(mMenuItem)
	mMenuItem = menu.SelectableItem("Quit", constants.ACTION_QUIT)
	mMenu.addItem(mMenuItem)
	Game.menus.append(mMenu)
	# Create "choose mode" selectable menu items
	mMenu = menu.Selectable(Game.font, Game.screen)
	mMenuItem = menu.SelectableItem("1 Player", constants.ACTION_MODE1P)
	mMenu.addItem(mMenuItem)
	mMenuItem = menu.SelectableItem("2 Players", constants.ACTION_MODE2P)
	mMenu.addItem(mMenuItem)
	Game.menus.append(mMenu)
	# Create "score" text
	mText = menu.Text(Game.font, Game.screen)
	mTextItem = menu.TextItem(Game.font, str(Game.score), (constants.WINDOW_WIDTH / 2.0), ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT) / 2.0) - (constants.WALL_THICKNESS / 2.0))
	mText.addItem(mTextItem)
	Game.texts.append(mText)
	# Create pause text
	mText = menu.Text(Game.font, Game.screen)
	mTextItem = menu.TextItem(Game.font, "P Unpauses", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mText.addItem(mTextItem)
	mTextItem = menu.TextItem(Game.font, "ESC Returns to Main Menu", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mTextItem.y += mTextItem.h
	mText.addItem(mTextItem)
	Game.texts.append(mText)
	# Create game over text
	mText = menu.Text(Game.font, Game.screen)
	mTextItem = menu.TextItem(Game.font, "Game Over!", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mText.addItem(mTextItem)
	mTextItem = menu.TextItem(Game.font, "N Starts a New Game", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mTextItem.y += mTextItem.h
	mText.addItem(mTextItem)
	mTextItem = menu.TextItem(Game.font, "ESC Returns to Main Menu", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mTextItem.y += (mTextItem.h * 2.0)
	mText.addItem(mTextItem)
	Game.texts.append(mText)

	
def fileAccessible(filepath, mode):
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
 
    return True


def ballLost(ball):
	if len(Game.balls) == 1:
		if Game.ballsLeft == 0:
			changeState(constants.STATE_GAMEOVER)
		Game.balls = []
		Game.powerUps = []
		Game.paddles[constants.PLAYER_ONE].reset()
		if Game.numPlayers == 2:
			Game.paddles[constants.PLAYER_TWO].reset()
		mGameObject = gameobject.Ball(Game.screen)
		Game.balls.append(mGameObject)
		Game.ballsLeft -= 1
		updateBallIndicator()
	else:
		Game.balls.remove(ball)

		
def updateBallIndicator():
	Game.shapes = []
	for i in range(0, Game.ballsLeft):
		mShape = shape.Shape(constants.SHAPE_CIRCLE, (constants.GAMEAREA_X + (constants.BALL_SIZE * 3.0) * (i + 1) - (constants.BALL_SIZE * 2.0)), (constants.GAMEAREA_Y - (constants.BALL_SIZE * 2.0)), constants.BALL_SIZE, constants.BALL_SIZE, constants.BALL_THICKNESS, constants.BALL_COLOR)
		Game.shapes.append(mShape)

		
def loadLevel():
	Game.bricks[:] = []
	Game.paddles[:] = []
	Game.balls = []
	Game.powerUps = []
	Game.wall = None
	level = [[]]
	
	# Load the level from a file
	filename = os.path.join(os.getcwd(), str(Game.levelNow) + ".txt")
	print "Trying to open " + filename
	
	if fileAccessible(filename, 'r') == True:
		with open(filename) as f:
			level = f.readlines()
		constants.LEVEL_WIDTH = len(level[0]) - 1
		constants.LEVEL_HEIGHT = len(level)
	else:
		print "Could not open " + filename
		print "Creating a dummy level"
		Game.levelNow = 0
		constants.LEVEL_WIDTH = 10
		constants.LEVEL_HEIGHT = 6
		level = [['1' for x in range(constants.LEVEL_WIDTH)] for x in range(constants.LEVEL_HEIGHT)]
	
	# Adjust the dimensions of bricks, paddles and game area
	constants.BRICK_WIDTH = ceil(constants.WINDOW_WIDTH * (1.0 / (constants.LEVEL_WIDTH + 15)))
	if constants.BRICK_THICKNESS == 0:
		constants.GAMEAREA_WIDTH = ceil(constants.WALL_THICKNESS + ((constants.BRICK_WIDTH + constants.BRICK_THICKNESS) * constants.LEVEL_WIDTH) + 1)
	else:
		constants.GAMEAREA_WIDTH = ceil(constants.WALL_THICKNESS + ((constants.BRICK_WIDTH + constants.BRICK_THICKNESS) * constants.LEVEL_WIDTH))
	constants.GAMEAREA_X = ceil((constants.WINDOW_WIDTH / 2.0) - (constants.GAMEAREA_WIDTH / 2.0))
	
	constants.BALL_STARTINGSPEED = constants.WINDOW_HEIGHT * 0.006
	constants.PADDLE_STARTINGSPEED = constants.WINDOW_WIDTH * 0.005
	constants.PADDLE_WIDTH = ceil(constants.WINDOW_WIDTH * 0.10)
	constants.PADDLE_HEIGHT = ceil(constants.PADDLE_WIDTH * 0.125)
	
	# Create game objects
	# Player 1 paddle
	mGameObject = gameobject.Paddle(Game.screen, constants.PLAYER_ONE)
	Game.paddles.append(mGameObject)
	# Player 2 paddle
	mGameObject = gameobject.Paddle(Game.screen, constants.PLAYER_TWO)
	Game.paddles.append(mGameObject)
	# The ball
	mGameObject = gameobject.Ball(Game.screen)
	Game.balls.append(mGameObject)
	# The game area
	mGameObject = gameobject.GameObject(Game.screen, constants.GAMEOBJECT_WALL, constants.GAMEAREA_WIDTH, constants.GAMEAREA_HEIGHT, constants.GAMEAREA_X, constants.GAMEAREA_Y, constants.WALL_THICKNESS, constants.WALL_COLOR)
	Game.wall = mGameObject
	# Balls left indicator
	updateBallIndicator()
	
	if Game.numPlayers == 1:
		Game.paddles[constants.PLAYER_TWO].disable()
	elif Game.numPlayers == 2:
		Game.paddles[constants.PLAYER_TWO].enable()
	
	for i in range(0, constants.LEVEL_HEIGHT):
		for j in range(0, constants.LEVEL_WIDTH):
			if level[i][j] != '0':
				if constants.BRICK_THICKNESS == 0:
					padding = 1
				else:
					padding = 0
				mGameObject = gameobject.Brick(Game.screen, level[i][j], (constants.GAMEAREA_X + floor(constants.WALL_THICKNESS / 2.0) + ceil(constants.BRICK_THICKNESS / 2.0) + ((constants.BRICK_WIDTH + constants.BRICK_THICKNESS) * j) + padding), (constants.GAMEAREA_Y + floor(constants.WALL_THICKNESS / 2.0) + ceil(constants.BRICK_THICKNESS / 2.0) + ((constants.BRICK_HEIGHT + constants.BRICK_THICKNESS) * i) + padding), i, j)
				Game.bricks.append(mGameObject)
			print level[i][j],
		print ""

	Game.bricksLeft = len(Game.bricks)
	print "level loaded"

	
def navigateMenu(navigation):
	if navigation == 0: # Move down in the menu
		if Game.menuSelection == (len(Game.currentMenu.items) - 1):
			Game.menuSelection = 0
		else:
			Game.menuSelection += 1
	elif navigation == 1: # Move up in the menu
		if Game.menuSelection == 0:
			Game.menuSelection = (len(Game.currentMenu.items) - 1)
		else:
			Game.menuSelection -= 1
	elif navigation == 2: # Select menu item
		action = Game.currentMenu.items[Game.menuSelection].action
		if action == constants.ACTION_QUIT:
			return True
		elif action == constants.ACTION_NEWGAME:
			changeState(constants.STATE_CHOOSEMODE)
		elif action == constants.ACTION_MODE1P or action == constants.ACTION_MODE2P:
			if action == constants.ACTION_MODE1P:
				Game.numPlayers = 1
			else:
				Game.numPlayers = 2
			Game.levelNow = 1
			newGame()
	return False

	
def updateScore(score = None):
	if score != None:
		Game.score = score
	Game.currentTexts[0].items[constants.PLAYER_ONE].text = str(Game.score)
	Game.currentTexts[0].items[constants.PLAYER_ONE].update(Game.font)

	
def newGame(nextLevel = False):
	changeState(constants.STATE_GAME)
	if nextLevel:
		# Advance to the next level
		Game.levelNow += 1
		updateScore()
	else:
		# Start a completely new game
		Game.levelNow = 1
		Game.ballsLeft = constants.GAME_STARTINGBALLS
		Game.extraBallsGiven = 0
		updateScore(0)
	loadLevel()

	
def drawMenu():
	if Game.state == constants.STATE_MAINMENU:
		Game.currentMenu = Game.menus[0]
	elif Game.state == constants.STATE_CHOOSEMODE:
		Game.currentMenu = Game.menus[1]
	if Game.currentMenu != None:
		Game.currentMenu.draw(Game.menuSelection)

		
def drawTexts():
	if Game.currentTexts != None:
		for t in Game.currentTexts:
			t.draw()

			
def drawShapes():
	for s in Game.shapes:
		s.draw(Game.screen)


def drawObjects(alpha = 0):
	for p in Game.paddles:
		p.draw(alpha)
	for b in Game.balls:
		b.draw(alpha)
	for c in Game.bricks:
		c.draw(alpha)
	for u in Game.powerUps:
		u.draw(alpha)
	Game.wall.draw()

	
def changeState(mState):
	Game.menuSelection = 0
	if mState == constants.STATE_MAINMENU:
		Game.state = constants.STATE_MAINMENU
		Game.currentTexts[:] = []
		Game.currentMenu = Game.menus[0]
		Game.shapes = []
	elif mState == constants.STATE_GAME:
		Game.state = constants.STATE_GAME
		Game.currentTexts[:] = []
		Game.currentTexts.append(Game.texts[0])
		Game.currentMenu = None
	elif mState == constants.STATE_CHOOSEMODE:
		Game.state = constants.STATE_CHOOSEMODE
		Game.currentTexts[:] = []
		Game.currentMenu = Game.menus[1]
		Game.shapes = []
	elif mState == constants.STATE_PAUSE:
		Game.state = constants.STATE_PAUSE
		Game.currentTexts.append(Game.texts[1])
		Game.currentMenu = None
	elif mState == constants.STATE_GAMEOVER:
		Game.state = constants.STATE_GAMEOVER
		Game.currentTexts.append(Game.texts[2])
		Game.currentMenu = None

		
def distance(obj1, obj2, useOldPos1 = False, useOldPos2 = False):
	obj = []
	obj.append(obj1)
	obj.append(obj2)
	old = []
	old.append(useOldPos1)
	old.append(useOldPos2)
	pos = [[0 for x in range(2)] for x in range(2)]
	for i in range(0, 2):
		if obj[i].type == constants.GAMEOBJECT_BRICK or obj[i].type == constants.GAMEOBJECT_PADDLE:
			if old[i]:
				pos[i][0] = (obj[i].oldX + (obj[i].w / 2.0))
				pos[i][1] = (obj[i].oldY + (obj[i].h / 2.0))
			else:
				pos[i][0] = (obj[i].x + (obj[i].w / 2.0))
				pos[i][1] = (obj[i].y + (obj[i].h / 2.0))
		elif obj[i].type == constants.GAMEOBJECT_BALL:
			if old[i]:
				pos[i][0] = obj[i].oldX + (obj[i].w / 2.0)
				pos[i][1] = obj[i].oldY + (obj[i].w / 2.0)
			else:
				pos[i][0] = obj[i].x + (obj[i].w / 2.0)
				pos[i][1] = obj[i].y + (obj[i].w / 2.0)
	return abs(sqrt(pow(pos[0][0]-pos[1][0], 2) + pow(pos[0][1]-pos[1][1], 2)))

	
def hitBrick(brick, ball):
	powerUp = brick.hit()
	if ord(brick.brickType) < ord('0') or ord(brick.brickType) > ord('9'):
		if powerUp != None:
			Game.powerUps.append(powerUp)
		elif brick.brickType == constants.POWERUP_EXPLOSION:
			# All nearby bricks take a hit
			for c in Game.bricks:
				if c.enabled:
					if (abs(c.levelX - brick.levelX) + abs(c.levelY - brick.levelY)) <= constants.POWERUP_EXPLOSION_RADIUS:
						if hitBrick(c, ball):
							return 1
		elif brick.brickType == constants.POWERUP_COPYBALL:
			# An extra ball
			mGameObject = gameobject.Ball(Game.screen)
			mGameObject.sticky = None
			mGameObject.move(brick.x, brick.y)
			mGameObject.speed[0] = ball.speed[0]
			mGameObject.speed[1] = ball.speed[1]
			Game.balls.append(mGameObject)
		Game.score += 50
	if brick.enabled == True:
		Game.score += 10
	else:
		Game.score += 50
		Game.bricksLeft -= 1
		if Game.bricksLeft == 0:
			newGame(True)
			return 1
	if Game.score >= (Game.extraBallsGiven + 1) * constants.GAME_SCOREEXTRABALL:
		Game.extraBallsGiven += 1
		Game.ballsLeft += 1
		updateBallIndicator()
	updateScore()
	return 0

	
def checkCollisions():
	p1 = Game.paddles[constants.PLAYER_ONE]
	p2 = Game.paddles[constants.PLAYER_TWO]

	for b in Game.balls:
		# Check whether any of the balls collide with the paddles
		wallLeftX = (Game.wall.x + (Game.wall.b / 2.0) + (b.w / 2.0) + 1)
		wallRightX = (Game.wall.x + Game.wall.w - (Game.wall.b / 2.0) - (b.w * 1.5))
		if b.speed[1] > 0 and b.collidesWith(p1):
				b.bounce(p1.w, p1.x)
		elif Game.numPlayers > 1 and b.speed[1] > 0 and b.collidesWith(p2):
				b.bounce(p2.w, p2.x)
		elif b.x <= wallLeftX:
			# Ball reached the left side
			if b.sticky != None:
				# Ball is stickied to a paddle; move the ball a bit in order to prevent it from sliding inside the wall
				b.x = wallLeftX
			elif b.speed[0] < 0:
				# Bounce off the wall
				b.speed[0] *= -1
		elif b.x >= wallRightX:
			# Ball reached the right side
			if b.sticky != None:
				# Ball is stickied to a paddle; move the ball a bit in order to prevent it from sliding inside the wall
				b.x = wallRightX
			elif b.speed[0] > 0:
				# Bounce off the wall
				b.speed[0] *= -1
		elif b.speed[1] > 0 and b.y >= (Game.wall.y + Game.wall.h - (Game.wall.b / 2.0) - (b.w * 1.5)):
			# Ball reached the floor; destroy the ball
			ballLost(b)
		elif b.speed[1] < 0 and b.y <= (Game.wall.y + (Game.wall.b / 2.0) + (b.w / 2.0)):
			# Ball reached the roof; change its direction
			b.speed[1] *= -1
		else:
			# Check whether any of the balls collide with any of the bricks
			hitsX = []
			hitsY = []
			changeX = False
			changeY = False
			for c in Game.bricks:
				if c.enabled:
					col = b.collidesWith(c)
					if col == 1:
						# The ball hit the top or bottom of a brick
						changeY = True
						hitsY.append(c)
					elif col == 2:
						# The ball hit a side of a brick
						changeX = True
						hitsX.append(c)
			if changeX and changeY:
				# The ball hit a side of one brick and top/bottom of another
				if len(hitsY) == 1 and len(hitsX) == 1:
					# The ball hit exactly two bricks
					if hitsX[0].x == hitsY[0].x or hitsX[0].y == hitsY[0].y:
						# The bricks are on the same axis: the one which is farther from the ball wasn't really hit!
						hXdis = distance(b, hitsX[0], True)
						hYdis = distance(b, hitsY[0], True)
						if hXdis < hYdis:
							changeY = False
						elif hYdis < hXdis:
							changeX = False
			if changeX:
				for h in hitsX:
					if hitBrick(h, b):
						return # No more bricks left; stop collision tests
				b.speed[0] *= -1
			if changeY:
				for h in hitsY:
					if hitBrick(h, b):
						return # No more bricks left; stop collision tests
				b.speed[1] *= -1
	for u in Game.powerUps:
		if u.enabled:
			if u.y >= (Game.wall.y + Game.wall.h - (Game.wall.b / 2.0)):
				# A falling power-up left the game area
				u.disable()
			else:
				for p in Game.paddles:
					if p.enabled and u.collidesWith(p):
						# A falling power-up hit a paddle
						if u.powerUp == constants.POWERUP_DOUBLEBALL:
							# An extra ball for the player: stick it on the paddle
							mGameObject = gameobject.Ball(Game.screen)
							mGameObject.sticky = p.player
							Game.balls.append(mGameObject)
						elif u.powerUp == constants.POWERUP_EXTRAWIDTH:
							# Increase the width of the paddle
							p.x -= (p.w * 0.125)
							p.w *= 1.25
						u.disable()

						
def movePaddle(mPlayer, mDirection):
	Game.paddles[mPlayer].move(mDirection)
	# Check whether the paddle hit a wall
	x = Game.paddles[mPlayer].x
	w = Game.paddles[mPlayer].w
	b = Game.paddles[mPlayer].b
	paddleWallLeft = (Game.wall.x + (Game.wall.b / 2.0) + ceil(b / 2.0))
	paddleWallRight = ceil(constants.GAMEAREA_X + Game.wall.w - w - (Game.wall.b / 2.0) - (b / 2.0))
	
	if mDirection == constants.DIRECTION_LEFT and x < paddleWallLeft:
		# Paddle hit the left wall
		Game.paddles[mPlayer].x = paddleWallLeft
	elif mDirection == constants.DIRECTION_RIGHT and x > paddleWallRight:
		# Paddle hit the right wall
		Game.paddles[mPlayer].x = paddleWallRight

		
def movePaddles():
	for p in Game.paddles:
		p.update()
	p1 = Game.paddles[constants.PLAYER_ONE]
	p2 = Game.paddles[constants.PLAYER_TWO]
	if Game.numPlayers >= 1:
		if Game.keys[pygame.K_LEFT]:
			movePaddle(constants.PLAYER_ONE, constants.DIRECTION_LEFT)
		elif Game.keys[pygame.K_RIGHT]:
			movePaddle(constants.PLAYER_ONE, constants.DIRECTION_RIGHT)
		if Game.keys[pygame.K_UP]:
			# Up arrow launches the ball(s)
			for b in Game.balls:
				if b.sticky == constants.PLAYER_ONE:
					b.launch(p1.w, p1.x)
			Game.keys[pygame.K_UP] = 0
	if Game.numPlayers == 2:
		if Game.keys[pygame.K_a]:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_LEFT)
		elif Game.keys[pygame.K_d]:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_RIGHT)
		if Game.keys[pygame.K_w]:
			# W launches the ball(s)
			for b in Game.balls:
				if b.sticky == constants.PLAYER_TWO:
					b.launch(p2.w, p2.x)
			Game.keys[pygame.K_w] = 0

			
def moveBalls():
	for b in Game.balls:
		if b.sticky != None:
			p = Game.paddles[b.sticky]
			x = p.x + (p.w / 1.75) - (b.w / 2.0)
			y = ((p.y - ceil(p.b / 2.0) - (b.w * 1.5)) + 1)
			b.move(x, y)
		else:
			b.update()

			
def movePowerUps():
	for u in Game.powerUps:
		u.update()

		
def handleInput():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return True
		elif event.type == pygame.KEYDOWN:
			# Store all key presses
			Game.keys[event.key] = 1
			if event.key == pygame.K_ESCAPE:
				if Game.state == constants.STATE_MAINMENU:
					# Pressing escape in main menu quits
					return True
				elif Game.state == constants.STATE_CHOOSEMODE or Game.state == constants.STATE_PAUSE or Game.state == constants.STATE_GAMEOVER:
					# Pressing escape while the game is paused or in the mode selection screen or in the game over screen brings you back to main menu
					changeState(constants.STATE_MAINMENU)
				elif Game.state == constants.STATE_GAME:
					# Pressing escape while in the game pauses the game
					changeState(constants.STATE_PAUSE)
			elif event.key == pygame.K_UP:
				if Game.state == constants.STATE_MAINMENU or Game.state == constants.STATE_CHOOSEMODE:
					# Navigate up in the menu
					return navigateMenu(1)
			elif event.key == pygame.K_DOWN:
				if Game.state == constants.STATE_MAINMENU or Game.state == constants.STATE_CHOOSEMODE:
					# Navigate down in the menu
					return navigateMenu(0)
			elif event.key == pygame.K_RETURN:
				if Game.state == constants.STATE_MAINMENU or Game.state == constants.STATE_CHOOSEMODE:
					# Enter selects a menu item
					return navigateMenu(2)
		elif event.type == pygame.KEYUP:
			# The key is no longer being held down
			Game.keys[event.key] = 0

	if Game.keys[pygame.K_p]:
		# P (un)pauses the game
		if Game.state == constants.STATE_GAME:
			changeState(constants.STATE_PAUSE)
		elif Game.state == constants.STATE_PAUSE:
			changeState(constants.STATE_GAME)
		Game.keys[pygame.K_p] = 0
	
	if Game.keys[pygame.K_n]:
		# N advances to next level or starts a new game
		if Game.state == constants.STATE_GAME:
			# Advance to next level
			newGame(True)
		elif Game.state == constants.STATE_GAMEOVER:
			# Start a new game
			newGame()
		Game.keys[pygame.K_n] = 0
	return False


def render(alpha = 0):
		# First, clear the screen to WHITE. Don't put other drawing commands
		# above this, or they will be erased with this command.
		Game.screen.fill(constants.WHITE)
	 
		if Game.state == constants.STATE_GAME or Game.state == constants.STATE_PAUSE or Game.state == constants.STATE_GAMEOVER:
			drawObjects(alpha)
		drawMenu()
		drawTexts()
		drawShapes()
	 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()


# -------- Main Program Loop -----------
if __name__ == '__main__':
	# Initialize game menus and game objects
	initGame()
	
	FPS = 0
	FPSTimer = 0
	
	t = 0.0;
	
	currentTime = currentMilliseconds();
	accumulator = 0.0
	
	alpha = 0.0
	
	render()
	while not Game.done:
		Game.done = handleInput()
		newTime = currentMilliseconds()
		frameTime = newTime - currentTime
		currentTime = newTime
		FPSTimer += frameTime
		FPS += 1
		
		if Game.state == constants.STATE_GAME:
			accumulator += frameTime

			while accumulator >= constants.DELTATIME:
				if Game.state == constants.STATE_GAME:
					movePaddles()
					moveBalls()
					movePowerUps()
					checkCollisions()
				accumulator -= constants.DELTATIME
				t += constants.DELTATIME
				
			alpha = accumulator / constants.DELTATIME
		
		render(alpha)
		if FPSTimer >= 1000:
			FPSTimer -= 1000
			pygame.display.set_caption("Arkanoid FPS: " + str(FPS))
			FPS = 0
 
pygame.quit()
