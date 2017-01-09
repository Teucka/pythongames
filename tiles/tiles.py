import pygame
from constants import *
import level, player
import tile
import time
import os.path #os.path.isfile

currentMilliseconds = lambda: int(round(time.time() * 1000))

# Setup
pygame.init()
pygame.display.set_caption("Tiles")
pygame.mouse.set_visible(0)

class Game:
	font = pygame.font.SysFont('Calibri', 25, True, False)
	screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
	clock = pygame.time.Clock()
	done = False
	# Store all key presses
	keys = [0] * 500
	# Level
	level = None
	# Player
	player = None

	
def initGame():
	filename = os.path.join(os.getcwd(), "map.png")
	print "Trying to open " + filename
	tileset = loadTileset(filename, TILE_SIZE, TILE_SIZE)
	Game.level = level.Level(Game.screen, tileset)
	print "Tileset loaded"
	if loadLevel() == False:
		return False
	filename = os.path.join(os.getcwd(), "player.png")
	print "Trying to open " + filename
	loadPlayer(filename)
	return True
	
	
def loadPlayer(filename):
	playerImage = pygame.image.load(filename).convert()
	playerImage.set_colorkey(WHITE)
	Game.player = player.Player(Game.screen, Game.level.getStartingPoint(), playerImage)
	
	
def loadTileset(filename, width, height):
	image = pygame.image.load(filename).convert()
	imageW, imageH = image.get_size()
	tiles = []
	for x in range(0, (imageW / width)):
		line = []
		tiles.append(line)
		for y in range(0, (imageH / height)):
			rect = ((x * width), (y * height), width, height)
			line.append(image.subsurface(rect))
	return tiles
	
	
def fileAccessible(filepath, mode):
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
    return True
	
	
def loadLevel():
	filename = os.path.join(os.getcwd(), "1.map")
	print "Trying to open " + filename
	if fileAccessible(filename, 'r'):
		with open(filename) as f:
			levelData = f.readlines()
			levelWidth = len(levelData[0]) - 1
			levelHeight = len(levelData)
			Game.level.setMap(levelData, levelWidth, levelHeight)
		print "Level data loaded"
	else:
		print "Couldn't open file " + str(filename)
		return False
	
	filename = os.path.join(os.getcwd(), "1.col")
	print "Trying to open " + filename
	if fileAccessible(filename, 'r'):
		with open(filename) as f:
			collisionData = f.readlines()
			Game.level.setCollisionMap(collisionData, levelWidth, levelHeight)
		print "Collision data loaded"
	else:
		print "Couldn't open file " + str(filename)
		return False
	return True
	
	
def movePlayer(dir):
	walkable = 0
	offset = (1 - Game.player.speed)
	
	if dir == DIRECTION_UP:
		walkable = Game.level.isWalkable(Game.player.pos[0], Game.player.pos[1] - Game.player.speed)
		if walkable > 0:
			walkable = Game.level.isWalkable(Game.player.pos[0] + offset, Game.player.pos[1] - Game.player.speed)
	elif dir == DIRECTION_DOWN:
		walkable = Game.level.isWalkable(Game.player.pos[0], Game.player.pos[1] + Game.player.speed + offset)
		if walkable > 0:
			walkable = Game.level.isWalkable(Game.player.pos[0] + offset, Game.player.pos[1] + Game.player.speed + offset)
	elif dir == DIRECTION_LEFT:
		walkable = Game.level.isWalkable(Game.player.pos[0] - Game.player.speed, Game.player.pos[1])
		if walkable > 0:
			walkable = Game.level.isWalkable(Game.player.pos[0] - Game.player.speed, Game.player.pos[1] + offset)
	elif dir == DIRECTION_RIGHT:
		walkable = Game.level.isWalkable(Game.player.pos[0] + Game.player.speed + offset, Game.player.pos[1])
		if walkable > 0:
			walkable = Game.level.isWalkable(Game.player.pos[0] + Game.player.speed + offset, Game.player.pos[1] + offset)
		
	if walkable > 0:
		Game.player.move(dir)
	
	
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
		elif event.type == pygame.KEYUP:
			Game.keys[event.key] = 0
				
	if Game.keys[pygame.K_w]:
		movePlayer(DIRECTION_UP)
	if Game.keys[pygame.K_s]:
		movePlayer(DIRECTION_DOWN)
	if Game.keys[pygame.K_a]:
		movePlayer(DIRECTION_LEFT)
	if Game.keys[pygame.K_d]:
		movePlayer(DIRECTION_RIGHT)
		
		
def render(alpha = 0):
		# First, clear the screen to WHITE. Don't put other drawing commands
		# above this, or they will be erased with this command.
		Game.screen.fill(WHITE)
	 
		Game.level.draw()
		Game.player.draw(alpha)
	 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
 
 
# -------- Main Program Loop -----------
if __name__ == '__main__':
	# Initialize game menus and game objects
	if initGame() == False:
		Game.done = True
	
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
			Game.player.update()
					
			accumulator -= DELTATIME
			t += DELTATIME
			
		alpha = accumulator / DELTATIME
		
		render(alpha)
		
		if FPSTimer >= 1000:
			FPSTimer -= 1000
			pygame.display.set_caption("Tiles FPS: " + str(FPS))
			FPS = 0
 
pygame.quit()