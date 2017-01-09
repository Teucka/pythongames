import constants
import pygame
import menu
import gameobject
from math import ceil
import time

currentMilliseconds = lambda: int(round(time.time() * 1000))

# Setup
pygame.init()
pygame.display.set_caption("Pong")
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
	score = [0, 0]
	# How many players (1 = vs. AI)
	numPlayers = 1

	
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
	# Create "score" texts
	mText = menu.Text(Game.font, Game.screen)
	mTextItem = menu.TextItem(Game.font, str(Game.score[constants.PLAYER_ONE]), (constants.WINDOW_WIDTH / 2.0) + (constants.WINDOW_WIDTH / 6), ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT) / 2.0) - (constants.WALL_THICKNESS / 2.0))
	mText.addItem(mTextItem)
	mTextItem = menu.TextItem(Game.font, str(Game.score[constants.PLAYER_TWO]), (constants.WINDOW_WIDTH / 2.0) - (constants.WINDOW_WIDTH / 6), ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT) / 2.0) - (constants.WALL_THICKNESS / 2.0))
	mText.addItem(mTextItem)
	Game.texts.append(mText)
	# Create pause text
	mText = menu.Text(Game.font, Game.screen)
	mTextItem = menu.TextItem(Game.font, "'P' Unpauses 'Esc' Quits", (constants.WINDOW_WIDTH / 2.0), (constants.WINDOW_HEIGHT / 3))
	mText.addItem(mTextItem)
	Game.texts.append(mText)
	# Player 1 paddle
	mGameObject = gameobject.Paddle(Game.screen, constants.PLAYER_ONE)
	Game.paddles.append(mGameObject)
	# Player 2 paddle
	mGameObject = gameobject.Paddle(Game.screen, constants.PLAYER_TWO)
	Game.paddles.append(mGameObject)
	# Ball
	mGameObject = gameobject.Ball(Game.screen)
	Game.balls.append(mGameObject)
	# Game area
	mGameObject = gameobject.GameObject(Game.screen, constants.GAMEOBJECT_WALL, constants.GAMEAREA_WIDTH, constants.GAMEAREA_HEIGHT, constants.GAMEAREA_X, constants.GAMEAREA_Y, constants.WALL_THICKNESS, constants.WALL_COLOR)
	Game.wall = mGameObject

	
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
		elif action == constants.ACTION_MODE1P:
			Game.numPlayers = 1
			newGame()
		elif action == constants.ACTION_MODE2P:
			Game.numPlayers = 2
			newGame()
	return False
	
	
def updateScore(score1 = None, score2 = None):
	if score1 != None:
		Game.score[0] = score1
	if score2 != None:
		Game.score[1] = score2
	Game.currentTexts[0].items[constants.PLAYER_ONE].text = str(Game.score[constants.PLAYER_ONE])
	Game.currentTexts[0].items[constants.PLAYER_ONE].update(Game.font)
	Game.currentTexts[0].items[constants.PLAYER_TWO].text = str(Game.score[constants.PLAYER_TWO])
	Game.currentTexts[0].items[constants.PLAYER_TWO].update(Game.font)
	
	
def newGame(winner = -1):
	changeState(constants.STATE_GAME)

	for b in Game.balls:
		b.reset()
	
	if winner == constants.PLAYER_ONE:
		Game.score[0] += 1
	elif winner == constants.PLAYER_TWO:
		Game.score[1] += 1
		# The ball always moves towards the winner at start
		Game.balls[0].speed = [-constants.BALL_STARTINGSPEED, 0]
	else:
		Game.score = [0, 0]
		
	# Update score texts
	updateScore()
	
	# Reset paddle positions
	for p in Game.paddles:
		p.reset()
		
		
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
			
			
def drawObjects(alpha = 0):
	for p in Game.paddles:
		p.draw(alpha)
	for b in Game.balls:
		b.draw(alpha)
	Game.wall.draw()
	
	
def changeState(mState):
	Game.menuSelection = 0
	if mState == constants.STATE_MAINMENU:
		Game.state = constants.STATE_MAINMENU
		Game.currentTexts[:] = []
		Game.currentMenu = Game.menus[0]
	elif mState == constants.STATE_GAME:
		Game.state = constants.STATE_GAME
		Game.currentTexts[:] = []
		Game.currentTexts.append(Game.texts[0])
		Game.currentMenu = None
	elif mState == constants.STATE_CHOOSEMODE:
		Game.state = constants.STATE_CHOOSEMODE
		Game.currentTexts[:] = []
		Game.currentMenu = Game.menus[1]
	elif mState == constants.STATE_PAUSE:
		Game.state = constants.STATE_PAUSE
		Game.currentTexts.append(Game.texts[1])
		Game.currentMenu = None

		
def checkCollisions():
	p1 = Game.paddles[constants.PLAYER_ONE]
	p2 = Game.paddles[constants.PLAYER_TWO]

	for b in Game.balls:
		# Check whether any of the balls collide with the paddles
		if b.speed[0] > 0 and b.collidesWith(p1):
				b.bounce(p1.h, p1.y, constants.DIRECTION_LEFT)
		elif b.speed[0] < 0 and b.collidesWith(p2):
				b.bounce(p2.h, p2.y, constants.DIRECTION_RIGHT)
		elif b.x <= (Game.wall.x + (b.w / 2.0) + (Game.wall.b / 2.0)):
			# Ball reached the left side; player 1 wins
			newGame(constants.PLAYER_ONE)
		elif b.x >= (Game.wall.x + Game.wall.w - (b.w * 1.5) - (Game.wall.b / 2.0)):
			# Ball reached the right side; player 2 wins
			newGame(constants.PLAYER_TWO)
		elif (b.speed[1] > 0 and b.y >= (Game.wall.y + Game.wall.h - (Game.wall.b / 2.0) - (b.w * 1.5))) or (b.speed[1] < 0 and b.y <= (Game.wall.y + (Game.wall.b / 2.0) + (b.w / 2.0))):
			# Ball is touching a wall; change its direction
			b.speed[1] *= -1
			
			
def movePaddle(mPlayer, mDirection):
	Game.paddles[mPlayer].move(mDirection)
	# Check whether the paddle hit a wall
	y = Game.paddles[mPlayer].y
	h = Game.paddles[mPlayer].h
	b = Game.paddles[mPlayer].b
	if y < (Game.wall.y + (Game.wall.b / 2.0) + ceil(b / 2.0)):
		# Paddle hit the upper wall
		Game.paddles[mPlayer].y = (Game.wall.y + (Game.wall.b / 2.0) + ceil(b / 2.0))
	elif y > (constants.WINDOW_HEIGHT - h - Game.wall.b - (b / 2.0)):
		# Paddle hit the lower wall
		Game.paddles[mPlayer].y = (constants.WINDOW_HEIGHT - h - Game.wall.b - (b / 2.0))
		
	
def movePaddles():
	if Game.keys[pygame.K_UP]:
		movePaddle(constants.PLAYER_ONE, constants.DIRECTION_UP)
	elif Game.keys[pygame.K_DOWN]:
		movePaddle(constants.PLAYER_ONE, constants.DIRECTION_DOWN)
	if Game.numPlayers == 2:
		if Game.keys[pygame.K_w]:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_UP)
		elif Game.keys[pygame.K_s]:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_DOWN)
	
	
def moveAI():
	ball = Game.balls[0]
	ai = Game.paddles[constants.PLAYER_TWO]
	paddleRealSpeed = (Game.paddles[constants.PLAYER_TWO].speed * (constants.DELTATIME * (constants.GAME_SPEED / 5.0)))
	if ball.speed[0] > 0:
		# The ball is moving away from AI's paddle; move to the middle
		if ai.y <= (((constants.WINDOW_HEIGHT / 2.0) - (ai.h / 2.0) + ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT)/2)) - paddleRealSpeed):
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_DOWN)
		elif ai.y > (((constants.WINDOW_HEIGHT / 2.0) - (ai.h / 2.0) + ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT)/2)) + paddleRealSpeed):
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_UP)
	elif ball.speed[0] < 0:
		# The ball is moving towards AI's paddle; try to center the paddle with the ball
		if (ball.y + (ball.w / 2.0)) > (ai.y + (ai.h / 2.0)) and (ball.y - (ai.y + (ai.h / 2.0))) >= paddleRealSpeed:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_DOWN)
		elif (ball.y + (ball.w / 2.0)) < (ai.y + (ai.h / 2.0)) and ((ai.y + (ai.h / 2.0)) - ball.y) >= paddleRealSpeed:
			movePaddle(constants.PLAYER_TWO, constants.DIRECTION_UP)
	
	
def updateObjects():
	for p in Game.paddles:
		p.update()
	for b in Game.balls:
		b.update()
		

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
				elif Game.state == constants.STATE_CHOOSEMODE or Game.state == constants.STATE_PAUSE:
					# Pressing escape while the game is paused or in the mode selection screen brings you back to main menu
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
					# Select the menu item
					return navigateMenu(2)
		elif event.type == pygame.KEYUP:
			# The key is no longer being held down
			Game.keys[event.key] = 0

	if Game.state == constants.STATE_GAME:
		if Game.keys[pygame.K_p]:
			changeState(constants.STATE_PAUSE)
			Game.keys[pygame.K_p] = 0
	elif Game.state == constants.STATE_PAUSE:
		if Game.keys[pygame.K_p]:
			changeState(constants.STATE_GAME)
			Game.keys[pygame.K_p] = 0
	return False

	
def render(alpha = 0):
		# First, clear the screen to WHITE. Don't put other drawing commands
		# above this, or they will be erased with this command.
		Game.screen.fill(constants.WHITE)
	 
		if Game.state == constants.STATE_GAME or Game.state == constants.STATE_PAUSE:
			drawObjects(alpha)
		drawMenu()
		drawTexts()
	 
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
				updateObjects()
				movePaddles()
				checkCollisions()
				if Game.numPlayers == 1:
					moveAI()
				accumulator -= constants.DELTATIME
				t += constants.DELTATIME
				
			alpha = accumulator / constants.DELTATIME
		
		render(alpha)
		if FPSTimer >= 1000:
			FPSTimer -= 1000
			pygame.display.set_caption("Pong FPS: " + str(FPS))
			FPS = 0
 
pygame.quit()