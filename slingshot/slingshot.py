import pygame
from constants import *
import ball, sling
import time

currentMilliseconds = lambda: int(round(time.time() * 1000))

# Setup
pygame.init()
pygame.display.set_caption("Slingshot")
pygame.mouse.set_visible(1)

class Game:
	font = pygame.font.SysFont('Calibri', 25, True, False)
	screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
	clock = pygame.time.Clock()
	done = False
	# Store all key presses
	keys = [0] * 500
	# Slingshot ball
	sling = None
	balls = []
	
	
def initGame():
	pos = [(WINDOW_WIDTH * 0.5), (WINDOW_HEIGHT * 0.5)]
	mBall = ball.Ball(Game.screen)
	mSling = sling.Sling(Game.screen, mBall, pos)
	Game.sling = mSling
	
	
def handleInput():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return True
		elif event.type == pygame.KEYDOWN:
			# Store all key presses
			Game.keys[event.key] = 1
			if event.key == pygame.K_ESCAPE:
				# Pressing escape quits
				return True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: # Left mousebutton
				if Game.sling.isHit(pygame.mouse.get_pos()):
					Game.sling.startDragging(pygame.mouse.get_pos())
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1 and Game.sling.ball.dragging == True: # Left mousebutton
				if slingBall() == False:
					Game.sling.ball.dragging = False
					Game.sling.reset()
				
				
def slingBall():
	if Game.sling.letGo():
		Game.balls.append(Game.sling.ball)
		mBall = ball.Ball(Game.screen)
		Game.sling.attach(mBall)
		return True
	return False
				
				
def drawObjects(alpha = 0):
	if Game.balls != None:
		for b in Game.balls:
			b.draw(alpha)
	if Game.sling != None:
		Game.sling.draw(alpha)
	
	
def updateObjects():
	if Game.sling.ball.dragging:
		Game.sling.drag(pygame.mouse.get_pos())
	if Game.balls != None:
		for b in Game.balls:
			b.update()

			
def render(alpha = 0):
		# First, clear the screen to WHITE. Don't put other drawing commands
		# above this, or they will be erased with this command.
		Game.screen.fill(WHITE)
	 
		drawObjects(alpha)
	 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
 
 
# -------- Main Program Loop -----------
if __name__ == '__main__':
	# Initialize game objects
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
		
		accumulator += frameTime

		while accumulator >= DELTATIME:
			updateObjects()
					
			accumulator -= DELTATIME
			t += DELTATIME
			
		alpha = accumulator / DELTATIME
		
		render(alpha)
		
		if FPSTimer >= 1000:
			FPSTimer -= 1000
			pygame.display.set_caption("Slingshot FPS: " + str(FPS))
			FPS = 0
 
pygame.quit()