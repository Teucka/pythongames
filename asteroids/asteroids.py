import constants
import pygame
import menu
import shape
import gameobject
import asteroid, ship, bullet
from math import ceil, floor, sqrt
import random
import time

currentMilliseconds = lambda: int(round(time.time() * 1000))

# Setup
pygame.init()
pygame.display.set_caption("Asteroids")
pygame.mouse.set_visible(0)

class Game:
	font = pygame.font.SysFont('Calibri', 25, True, False)
	screen = pygame.display.set_mode([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT])
	
	clock = pygame.time.Clock()
	random.seed()
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
	shapes = None
	# Main loop while not done
	done = False
	# Ship game object
	ship = None
	# List of all bullet game objects
	bullets = []
	# Wall (game area) game object
	wall = None
	# Store all key presses
	keys = [0] * 500
	# Game score
	score = 0
	# How many players (1 = vs. AI)
	numPlayers = 1
	
	# ASTEROIDS STUFF
	asteroids = []
	asteroidsLeft = 0
	levelNow = 1
	shipsLeft = constants.GAME_STARTINGSHIPS
	extraShipsGiven = 0

	
def initGame():
	# Create "main menu" selectable menu items
	mMenu = menu.Selectable(Game.font, Game.screen)
	mMenuItem = menu.SelectableItem("New Game", constants.ACTION_NEWGAME)
	mMenu.addItem(mMenuItem)
	mMenuItem = menu.SelectableItem("Quit", constants.ACTION_QUIT)
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

	
def updateShipIndicator():
	Game.shapes = []
	
	for i in range(0, Game.shipsLeft):
		width = 10
		height = 15
		mShape = shape.Shape(constants.SHAPE_SHIP, (constants.GAMEAREA_X + (constants.SHIP_WIDTH * 1.0 + 5) * (i + 1) - (constants.SHIP_WIDTH * 0.5)), (constants.GAMEAREA_Y - (constants.SHIP_HEIGHT * 0.5)), (constants.SHIP_WIDTH / 1.5), (constants.SHIP_HEIGHT / 1.5), 0, constants.SHIP_COLOR)
		Game.shapes.append(mShape)
		
		
def loadLevel():
	Game.asteroids[:] = []
	Game.bullets[:] = []
	Game.ship = None
	Game.wall = None
	
	# Player's ship
	mGameObject = ship.Ship(Game.screen)
	Game.ship = mGameObject
	Game.ship.enable()
	# The game area
	mGameObject = gameobject.GameObject(Game.screen, constants.GAMEOBJECT_WALL, constants.GAMEAREA_WIDTH, constants.GAMEAREA_HEIGHT, constants.GAMEAREA_X, constants.GAMEAREA_Y, constants.WALL_THICKNESS, constants.WALL_COLOR)
	Game.wall = mGameObject
	# Ships left indicator
	updateShipIndicator()
	# Asteroids
	sizes = []
	asteroidCount = int(ceil(constants.GAME_STARTINGASTEROIDS * (0.925 + (Game.levelNow * 0.075))))
	sizeCount = 0

	if Game.levelNow == 1:
		for j in range(0, asteroidCount):
			sizes.append(1)
	elif Game.levelNow == 2:
		for j in range(0, int(ceil(asteroidCount * 0.5))):
			sizes.append(1)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.5))):
			sizes.append(2)
			sizeCount += 1
	elif Game.levelNow == 3:
		for j in range(0, int(ceil(asteroidCount * 0.3))):
			sizes.append(1)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.7))):
			sizes.append(2)
			sizeCount += 1
	elif Game.levelNow == 3:
		for j in range(0, int(ceil(asteroidCount * 0.4))):
			sizes.append(1)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.5))):
			sizes.append(2)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.1))):
			sizes.append(3)
			sizeCount += 1
	elif Game.levelNow == 4:
		for j in range(0, int(ceil(asteroidCount * 0.3))):
			sizes.append(1)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.45))):
			sizes.append(2)
			sizeCount += 1
		for j in range(0, int(ceil(asteroidCount * 0.25))):
			sizes.append(3)
			sizeCount += 1
	elif Game.levelNow == 4:
		for j in range(0, int(ceil(asteroidCount * 0.20))):
			sizes.append(1)
		for j in range(0, int(ceil(asteroidCount * 0.4))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.4))):
			sizes.append(3)
	elif Game.levelNow == 5:
		for j in range(0, int(ceil(asteroidCount * 0.20))):
			sizes.append(1)
		for j in range(0, int(ceil(asteroidCount * 0.25))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.55))):
			sizes.append(3)
	elif Game.levelNow == 6:
		for j in range(0, int(ceil(asteroidCount * 0.10))):
			sizes.append(1)
		for j in range(0, int(ceil(asteroidCount * 0.30))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.60))):
			sizes.append(3)
	elif Game.levelNow == 7:
		for j in range(0, int(ceil(asteroidCount * 0.10))):
			sizes.append(1)
		for j in range(0, int(ceil(asteroidCount * 0.20))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.70))):
			sizes.append(3)
	elif Game.levelNow == 8:
		for j in range(0, int(ceil(asteroidCount * 0.20))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.80))):
			sizes.append(3)
	elif Game.levelNow == 9:
		for j in range(0, int(ceil(asteroidCount * 0.15))):
			sizes.append(2)
		for j in range(0, int(ceil(asteroidCount * 0.85))):
			sizes.append(3)
	elif Game.levelNow == 10:
		for j in range(0, asteroidCount):
			sizes.append(3)

	side = random.randint(1, 4)
	for i in range(0, asteroidCount):
		if side > constants.DIRECTION_RIGHT:
			side = constants.DIRECTION_UP
			
		x = 0
		y = 0
		
		if side is constants.DIRECTION_UP:
			x = random.randint(Game.wall.x, Game.wall.x + Game.wall.w)
			y = Game.wall.y
		elif side is constants.DIRECTION_DOWN:
			x = random.randint(Game.wall.x, Game.wall.x + Game.wall.w)
			y = Game.wall.y + Game.wall.h
		elif side is constants.DIRECTION_LEFT:
			x = Game.wall.x
			y = random.randint(Game.wall.y, Game.wall.y + Game.wall.h)
		elif side is constants.DIRECTION_RIGHT:
			x = Game.wall.x + Game.wall.w
			y = random.randint(Game.wall.y, Game.wall.y + Game.wall.h)
			
		mGameObject = asteroid.Asteroid(Game.screen, x, y, sizes.pop())
		Game.asteroids.append(mGameObject)
		side += 1

	Game.asteroidsLeft = len(Game.asteroids)
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
			Game.levelNow = 1
			newGame()
	return False
	
	
def updateScore(score = None):
	if score != None:
		Game.score = score
	Game.currentTexts[0].items[0].text = str(Game.score)
	Game.currentTexts[0].items[0].update(Game.font)
	
	
def newGame(nextLevel = False):
	changeState(constants.STATE_GAME)
	if nextLevel:
		# Advance to the next level
		Game.levelNow += 1
	else:
		# Start a completely new game
		Game.levelNow = 1
		Game.shipsLeft = constants.GAME_STARTINGSHIPS
		Game.extraShipsGiven = 0
		updateScore(0)
	if Game.levelNow > 10:
		changeState(constants.STATE_VICTORY)
	else:
		loadLevel()
		
		
def drawMenu():
	if Game.state == constants.STATE_MAINMENU:
		Game.currentMenu = Game.menus[0]
	if Game.currentMenu != None:
		Game.currentMenu.draw(Game.menuSelection)
		
		
def drawTexts():
	if Game.currentTexts != None:
		for t in Game.currentTexts:
			t.draw()
			
			
def drawShapes():
	if Game.shapes != None:
		for s in Game.shapes:
			s.draw(Game.screen)
			
			
def drawObjects(alpha = 0):
	if Game.ship != None:
		Game.ship.draw(alpha)
	if Game.asteroids != None:
		for a in Game.asteroids:
			a.draw(alpha)
	if Game.bullets != None:
		for b in Game.bullets:
			b.draw(alpha)
	if Game.wall != None:
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
	elif mState == constants.STATE_PAUSE:
		Game.state = constants.STATE_PAUSE
		Game.currentTexts.append(Game.texts[1])
		Game.currentMenu = None
	elif mState == constants.STATE_GAMEOVER:
		Game.state = constants.STATE_GAMEOVER
		Game.texts[2].items[0].text = "Game Over! Score: " + str(Game.score)
		Game.texts[2].items[0].update(Game.font)
		Game.currentTexts.append(Game.texts[2])
		Game.currentMenu = None
	elif mState == constants.STATE_VICTORY:
		Game.state = constants.STATE_VICTORY
		Game.texts[2].items[0].text = "Victory! Score: " + str(Game.score)
		Game.texts[2].items[0].update(Game.font)
		Game.currentTexts.append(Game.texts[2])
		Game.currentMenu = None

		
def hitAsteroid(mAsteroid, mBullet = None):
	returnValue = 0
	mAsteroid.disable()
	
	if mBullet != None:
		mBullet.disable()
		
	Game.score += mAsteroid.size * 10
	
	if mAsteroid.size > 1:
		Game.asteroidsLeft += 1
		mGameObject = asteroid.Asteroid(Game.screen, mAsteroid.x, mAsteroid.y, (mAsteroid.size - 1))
		Game.asteroids.append(mGameObject)
		mGameObject = asteroid.Asteroid(Game.screen, mAsteroid.x, mAsteroid.y, (mAsteroid.size - 1))
		Game.asteroids.append(mGameObject)
	else:
		Game.score += 5
		Game.asteroidsLeft -= 1
		if Game.asteroidsLeft == 0:
			newGame(True)
			returnValue = 1
			
	if Game.score >= (Game.extraShipsGiven + 1) * constants.GAME_SCOREEXTRASHIP:
		Game.extraShipsGiven += 1
		Game.shipsLeft += 1
		updateShipIndicator()
		
	updateScore()
	return returnValue
	
	
def checkCollisions():
	s = Game.ship

	for b in Game.bullets:
		# Check whether any of the bullets collide with the walls
		wallLeftX = (Game.wall.x + (Game.wall.thickness / 2.0) + (b.w / 2.0) + 1)
		wallRightX = (Game.wall.x + Game.wall.w - (Game.wall.thickness / 2.0) - (b.w * 1.5))
		
		if b.x <= wallLeftX and b.speed[0] < 0:
			# Bullet reached the left side
			b.x = constants.GAMEAREA_WIDTH + constants.GAMEAREA_X
			b.oldX = b.x
		elif b.x >= wallRightX and b.speed[0] > 0:
			# Bullet reached the right side
			b.x = constants.GAMEAREA_X
			b.oldX = b.x
		elif b.speed[1] > 0 and b.y >= (Game.wall.y + Game.wall.h - (Game.wall.thickness / 2.0) - (b.w * 1.5)):
			# Bullet reached the bottom side
			b.y = constants.GAMEAREA_Y
			b.oldY = b.y
		elif b.speed[1] < 0 and b.y <= (Game.wall.y + (Game.wall.thickness / 2.0) + (b.w / 2.0)):
			# Bullet reached the top side
			b.y = constants.WINDOW_HEIGHT
			b.oldY = b.y
			
		# Check whether any of the bullets collide with any of the asteroids
		for a in Game.asteroids:
			if a.enabled and b.enabled:
				if b.collidesWith(a):
					# The bullet hit the asteroid
					if hitAsteroid(a, b):
						return
						
	for a in Game.asteroids:
		# Check whether any of the asteroids collide with the walls
		wallLeftX = (Game.wall.x + (Game.wall.thickness / 2.0) + (a.w / 2.0) + 1)
		wallRightX = (Game.wall.x + Game.wall.w - (Game.wall.thickness / 2.0) - (a.w * 1.5))
		
		if a.x <= wallLeftX and a.dir[0] < 0:
			# Asteroid reached the left side
			a.x = constants.GAMEAREA_WIDTH + constants.GAMEAREA_X
			a.oldX = a.x
		elif a.x >= wallRightX and a.dir[0] > 0:
			# Asteroid reached the right side
			a.x = constants.GAMEAREA_X
			a.oldX = a.x
		elif a.dir[1] > 0 and a.y >= (Game.wall.y + Game.wall.h - (Game.wall.thickness / 2.0) - (a.w * 1.5)):
			# Asteroid reached the bottom side
			a.y = constants.GAMEAREA_Y
			a.oldY = a.y
		elif a.dir[1] < 0 and a.y <= (Game.wall.y + (Game.wall.thickness / 2.0) + (a.w / 2.0)):
			# Asteroid reached the top side
			a.y = constants.WINDOW_HEIGHT
			a.oldY = a.y
			
	if s.shieldTimer <= 0:
		# Check whether any of the asteroids collide with the ship
		for a in Game.asteroids:
			if a.enabled:
				if a.collidesWith(s):
					# The asteroid hit the ship
					if hitAsteroid(a):
						return
						
					Game.shipsLeft -= 1
					
					if Game.shipsLeft == -1:
						changeState(constants.STATE_GAMEOVER)
						Game.asteroids = []
						Game.ship = None
						Game.bullets = []
						
					updateShipIndicator()
					s.reset()
			
			
def moveShip():
	s = Game.ship
	s.update()
	
	if Game.keys[pygame.K_UP]:
		s.move(constants.DIRECTION_UP)
	elif Game.keys[pygame.K_DOWN]:
		s.move(constants.DIRECTION_DOWN)
	if Game.keys[pygame.K_LEFT]:
		s.turn(constants.DIRECTION_LEFT)
	elif Game.keys[pygame.K_RIGHT]:
		s.turn(constants.DIRECTION_RIGHT)
		
	# Check whether the ship is inside a wall
	shipWallTop = (Game.wall.y + (Game.wall.thickness * 0.5))
	shipWallBottom = ceil(constants.GAMEAREA_Y + Game.wall.h - (Game.wall.thickness * 0.5))
	shipWallLeft = (Game.wall.x + (Game.wall.thickness * 0.5))
	shipWallRight = ceil(constants.GAMEAREA_X + Game.wall.w - (Game.wall.thickness * 0.5))
	
	if s.y < shipWallTop:
		# Ship is inside the top wall
		s.y = shipWallBottom
		s.oldY = s.y
	elif s.y > shipWallBottom:
		# Ship is inside the bottom wall
		s.y = shipWallTop
		s.oldY = s.y
	elif s.x < shipWallLeft:
		# Ship is inside the left wall
		s.x = shipWallRight
		s.oldX = s.x
	elif s.x > shipWallRight:
		# Ship is inside the right wall
		s.x = shipWallLeft
		s.oldX = s.x

	if Game.keys[pygame.K_SPACE]:
		# Space shoots
		b = s.shoot()
		if b != None:
			Game.bullets.append(b)
			
			
def moveBullets():
	for b in Game.bullets:
		b.update()
		if b.enabled == False:
			Game.bullets.remove(b)
			
			
def moveAsteroids():
	for a in Game.asteroids:
		a.update()
		if a.enabled == False:
			Game.asteroids.remove(a)
			
			
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
				elif Game.state == constants.STATE_PAUSE or Game.state == constants.STATE_GAMEOVER or Game.state == constants.STATE_VICTORY:
					# Pressing escape while the game is paused or in the game over / victory screen brings you back to main menu
					changeState(constants.STATE_MAINMENU)
				elif Game.state == constants.STATE_GAME:
					# Pressing escape while in the game pauses the game
					changeState(constants.STATE_PAUSE)
			elif event.key == pygame.K_UP:
				if Game.state == constants.STATE_MAINMENU:
					# Navigate up in the menu
					return navigateMenu(1)
			elif event.key == pygame.K_DOWN:
				if Game.state == constants.STATE_MAINMENU:
					# Navigate down in the menu
					return navigateMenu(0)
			elif event.key == pygame.K_RETURN:
				if Game.state == constants.STATE_MAINMENU:
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
			newGame(1)
		elif Game.state == constants.STATE_GAMEOVER or Game.state == constants.STATE_VICTORY:
			# Start a new game
			newGame()
		Game.keys[pygame.K_n] = 0
		
	return False

	
def render(alpha = 0):
		# First, clear the screen to WHITE. Don't put other drawing commands
		# above this, or they will be erased with this command.
		Game.screen.fill(constants.WHITE)
	 
		if Game.state == constants.STATE_GAME or Game.state == constants.STATE_PAUSE or Game.state == constants.STATE_GAMEOVER or Game.state == constants.STATE_VICTORY:
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
					moveShip()
					moveBullets()
					moveAsteroids()
					
					checkCollisions()
					if Game.numPlayers == 0:
						moveAI()
						
				accumulator -= constants.DELTATIME
				t += constants.DELTATIME
				
			alpha = accumulator / constants.DELTATIME
		
		render(alpha)
		
		if FPSTimer >= 1000:
			FPSTimer -= 1000
			pygame.display.set_caption("Asteroids FPS: " + str(FPS))
			FPS = 0
 
pygame.quit()