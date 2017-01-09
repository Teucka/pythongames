import constants
import pygame
from math import sqrt, ceil

class GameObject:
	screen = None
	type = None
	color = None
	enabled = True
	w = 0
	h = 0
	x = 0.0
	y = 0.0
	b = 0
	oldX = 0.0
	oldY = 0.0
	
	def __init__(self, mScreen, mType, mW, mH, mX, mY, mB, mColor):
		self.screen = mScreen
		self.type = mType
		self.w = mW
		self.h = mH
		self.x = mX
		self.y = mY
		self.b = mB
		self.oldX = mX
		self.oldY = mY
		self.color = mColor
	
	
	def draw(self, alpha = 0):
		if self.enabled:
			posX = (self.oldX + ((self.x - self.oldX) * alpha))
			posY = (self.oldY + ((self.y - self.oldY) * alpha))
			if self.type == constants.GAMEOBJECT_PADDLE or self.type == constants.GAMEOBJECT_WALL or self.type == constants.GAMEOBJECT_BRICK or self.type == constants.GAMEOBJECT_POWERUP:
				pygame.draw.rect(self.screen, self.color, [posX, posY, self.w, self.h], self.b)
			elif self.type == constants.GAMEOBJECT_BALL:
				pygame.draw.circle(self.screen, self.color, [int((posX + (self.w / 2.0))), int((posY + (self.w / 2.0)))], self.w, 0)
				#pygame.draw.rect(self.screen, self.color, [(posX - (self.w / 2.0)), (posY - (self.w / 2.0)), (self.w * 2.0), (self.h * 2.0)], 1)
	
	
	def disable(self):
		self.enabled = False
	
	
	def enable(self):
		self.enabled = True
	
	
	def update(self):
		self.oldX = self.x
		self.oldY = self.y
		
		
class PowerUp(GameObject):
	powerUp = None
	
	def __init__(self, mScreen, mPowerUp, mX, mY):
		self.powerUp = mPowerUp
		mX -= (constants.POWERUP_WIDTH / 2.0)
		mY -= (constants.POWERUP_HEIGHT / 2.0)
		if self.powerUp == constants.POWERUP_DOUBLEBALL:
			self.color = constants.POWERUP_DOUBLEBALL_COLOR
		elif self.powerUp == constants.POWERUP_EXTRAWIDTH:
			self.color = constants.POWERUP_EXTRAWIDTH_COLOR
		else:
			self.color = constants.BRICK_COLOR
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_POWERUP, constants.POWERUP_WIDTH, constants.POWERUP_HEIGHT, mX, mY, constants.POWERUP_THICKNESS, self.color)
	
	
	def update(self):
		GameObject.update(self)
		self.y += (constants.DELTATIME * (constants.GAME_SPEED / 12.5))
	
	
	def collidesWith(self, mGameObject):
		if mGameObject.enabled == False:
			return 0
		bX1 = (mGameObject.x - ceil(mGameObject.b / 2.0) + 1)
		bY1 = (mGameObject.y - ceil(mGameObject.b / 2.0) + 1)
		bX2 = (bX1 + mGameObject.w + mGameObject.b - 2)
		bY2 = (bY1 + mGameObject.h + mGameObject.b - 2)
		aX1 = self.x
		aY1 = self.y
		aX2 = (aX1 + self.w - 1)
		aY2 = (aY1 + self.h - 1)
		#pygame.draw.line(self.screen, constants.BLACK, [aX1, aY1], [aX2, aY2], 1)
		#pygame.draw.line(self.screen, constants.RED, [bX1, bY1], [bX2, bY2], 1)
		#pygame.display.flip()
		return (aX1 < bX2 and aX2 > bX1 and aY1 < bY2 and aY2 > bY1)
		
		
class Brick(GameObject):
	powerUp = None
	brickType = None
	hits = 0
	maxHits = 1
	levelX = None
	levelY = None
	
	def __init__(self, mScreen, mBrickType, mX, mY, mLevelX, mLevelY):
		self.brickType = mBrickType
		self.levelX = mLevelX
		self.levelY = mLevelY
		if self.brickType == constants.POWERUP_DOUBLEBALL or self.brickType == constants.POWERUP_EXTRAWIDTH:
			self.powerUp = PowerUp(mScreen, self.brickType, (mX + (constants.BRICK_WIDTH / 2.0)), (mY + (constants.BRICK_HEIGHT / 2.0)))
			self.powerUp.disable()
			
		if self.brickType == constants.POWERUP_DOUBLEBALL:
			self.color = constants.POWERUP_DOUBLEBALL_COLOR
		elif self.brickType == constants.POWERUP_EXPLOSION:
			self.color = constants.POWERUP_EXPLOSION_COLOR
		elif self.brickType == constants.POWERUP_COPYBALL:
			self.color = constants.POWERUP_COPYBALL_COLOR
		elif self.brickType == constants.POWERUP_EXTRAWIDTH:
			self.color = constants.POWERUP_EXTRAWIDTH_COLOR
		else:
			shade = ((1 - (int(self.brickType) / 10.0)) * 255)
			self.color = [shade, shade, shade]
			self.maxHits = int(self.brickType)
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_BRICK, constants.BRICK_WIDTH, constants.BRICK_HEIGHT, mX, mY, constants.BRICK_THICKNESS, self.color)
	
	
	def hit(self):
		self.hits += 1
		if self.hits == self.maxHits:
			self.disable()
			if self.powerUp != None:
				self.powerUp.enable()
				return self.powerUp
		elif self.powerUp == None:
			shade = ((1 - ((self.maxHits - self.hits) / 10.0)) * 255)
			self.color = [shade, shade, shade]
		return None
		
		
class Paddle(GameObject):
	speed = 0
	player = None
	
	def __init__(self, mScreen, mPlayer):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_PADDLE, constants.PADDLE_WIDTH, constants.PADDLE_HEIGHT, 0, 0, constants.PADDLE_THICKNESS, constants.PADDLE_COLOR)
		self.player = mPlayer
		self.reset()
		
	
	def reset(self):
		if self.player == constants.PLAYER_ONE:
			self.y = (constants.GAMEAREA_Y + constants.GAMEAREA_HEIGHT - (constants.WALL_THICKNESS / 2.0) - self.h - (self.b / 2.0) - 1 - (constants.BALL_SIZE * 2.0))
		else:
			self.y = (constants.GAMEAREA_Y + constants.GAMEAREA_HEIGHT - (constants.WALL_THICKNESS / 2.0) - (self.h * 2.0) - (self.b * 1.5) - 1 - (constants.BALL_SIZE * 2.0))
		self.x = (constants.WINDOW_WIDTH / 2.0) - (self.w / 2.0)
		self.oldX = self.x
		self.oldY = self.y
		self.speed = constants.PADDLE_STARTINGSPEED
		
	
	def move(self, direction):
		GameObject.update(self)
		if direction == constants.DIRECTION_LEFT:
			self.x -= (self.speed * (constants.DELTATIME * (constants.GAME_SPEED / 25.0)))
		elif direction == constants.DIRECTION_RIGHT:
			self.x += (self.speed * (constants.DELTATIME * (constants.GAME_SPEED / 25.0)))
			
			
class Ball(GameObject):
	speed = [0, 0]
	bounces = 0
	sticky = None
	
	def __init__(self, mScreen, mX = 0, mY = 0):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_BALL, constants.BALL_SIZE, constants.BALL_SIZE, mX, mY, constants.BALL_THICKNESS, constants.BALL_COLOR)
		self.reset()
	
	
	def bounce(self, paddleW, paddleX):
		# Calculate the angle (not really an angle, just a speed multiplier) at which the ball will bounce off the paddle
		angle = (((paddleX + (paddleW / 2.0) - (self.x + (constants.BALL_SIZE / 2.0))) / ((paddleW / 2.0) + constants.BALL_SIZE)))
		# Adjust ball speed vector accordingly
		self.speed[0] = (constants.BALL_STARTINGSPEED * -angle)
		self.speed[1] = -constants.BALL_STARTINGSPEED
		# Calculate ball speed vector's length with pythagoras
		length = sqrt(pow(self.speed[0], 2) + pow(self.speed[1], 2))
		# Speed up the ball after every bounce off a paddle for added difficulty
		self.bounces += 1
		length = (length / (1 + (self.bounces / float(constants.BALL_BOUNCESPEEDUP))))
		# Normalize the ball speed
		self.speed[0] = (self.speed[0] / length) * constants.BALL_STARTINGSPEED
		self.speed[1] = (self.speed[1] / length) * constants.BALL_STARTINGSPEED
		self.sticky = None
	
	
	def launch(self, paddleW, paddleX):
		self.bounces -= 1
		self.bounce(paddleW, paddleX)
	
	
	def reset(self):
		self.speed = [0, 0]
		self.bounces = 0
		self.x = -5000
		self.y = -5000
		self.oldX = -5000
		self.oldY = -5000
		self.sticky = constants.PLAYER_ONE
	
	
	def update(self):
		GameObject.update(self)
		self.x += (self.speed[0] * (constants.DELTATIME * (constants.GAME_SPEED / 20.0)))
		self.y += (self.speed[1] * (constants.DELTATIME * (constants.GAME_SPEED / 20.0)))
	
	
	def move(self, mX, mY):
		GameObject.update(self)
		self.x = mX
		self.y = mY
		if self.oldX == -5000:
			self.oldX = self.x
			self.oldY = self.y
	
	
	def collidesWith(self, mGameObject):
		if mGameObject.enabled == False:
			return 0
		bX1 = (mGameObject.x - ceil(mGameObject.b / 2.0) + 1)
		bY1 = (mGameObject.y - ceil(mGameObject.b / 2.0) + 1)
		bX2 = (bX1 + mGameObject.w + mGameObject.b - 2)
		bY2 = (bY1 + mGameObject.h + mGameObject.b - 2)
		aX1 = (self.x - (self.w / 2.0))
		aY1 = (self.y - (self.w / 2.0))
		aX2 = (aX1 + (self.w * 2.0) - 1)
		aY2 = (aY1 + (self.w * 2.0) - 1)
		#pygame.draw.line(self.screen, constants.BLACK, [aX1, aY1], [aX2, aY2], 1)
		#pygame.draw.line(self.screen, constants.GREEN, [bX1, bY1], [bX2, bY2], 1)
		#pygame.display.flip()
		# todo: circle-square collision test
		if (aX1 < bX2 and aX2 > bX1 and aY1 < bY2 and aY2 > bY1):
			if mGameObject.type == constants.GAMEOBJECT_PADDLE:
				return 1 # Hitting the paddle always causes the ball to bounce upwards
			ballMiddleX = self.oldX + (self.w / 2.0)
			ballMiddleY = self.oldY + (self.w / 2.0)
			brickMiddleX = (mGameObject.x + (mGameObject.w / 2.0))
			brickMiddleY = (mGameObject.y + (mGameObject.h / 2.0))
			
			#pygame.draw.line(self.screen, constants.BLACK, [brickMiddleX, brickMiddleY], [ballMiddleX, ballMiddleY], 1)
			#pygame.display.flip()
			
			above = False
			below = False
			left = False
			right = False
			if ballMiddleY <= (brickMiddleY - (mGameObject.h / 2.0)):
				above = True
			if ballMiddleY >= (brickMiddleY + (mGameObject.h / 2.0)):
				below = True
			if ballMiddleX <= (brickMiddleX - (mGameObject.w / 2.0)):
				left = True
			if ballMiddleX >= (brickMiddleX + (mGameObject.w / 2.0)):
				right = True
			
			Y1 = brickMiddleY
			if above and (right or left):
				Y2 = (Y1 - (mGameObject.h / 2.0))
				if right:
					X1 = (brickMiddleX + (mGameObject.w / 2.0))
					X2 = (X1 - (mGameObject.h / 2.0))
				elif left:
					X1 = (brickMiddleX - (mGameObject.w / 2.0))
					X2 = (X1 + (mGameObject.h / 2.0))
			if below and (right or left):
				Y2 = (Y1 + (mGameObject.h / 2.0))
				if right:
					X1 = (brickMiddleX + (mGameObject.w / 2.0))
					X2 = (X1 - (mGameObject.h / 2.0)) 
				elif left:
					X1 = (brickMiddleX - (mGameObject.w / 2.0))
					X2 = (X1 + (mGameObject.h / 2.0))
					
			if (above and (right or left)) or (below and (right or left)):
				#pygame.draw.line(self.screen, constants.BLACK, [brickMiddleX, brickMiddleY], [X1, Y1], 1)
				#pygame.draw.line(self.screen, constants.BLACK, [brickMiddleX, brickMiddleY], [X2, Y2], 1)
				#pygame.display.flip()
				dis1 = sqrt(pow(ballMiddleX-X1, 2) + pow(ballMiddleY-Y1, 2))
				dis2 = sqrt(pow(ballMiddleX-X2, 2) + pow(ballMiddleY-Y2, 2))
				if dis1 <= dis2:
					return 2
				else:
					return 1
			elif below or above:
				return 1
			elif left or right:
				return 2
		return 0