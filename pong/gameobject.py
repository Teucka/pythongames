import constants
import pygame
from math import sqrt

class GameObject:
	screen = None
	type = None
	color = constants.BLACK
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
		posX = (self.oldX + ((self.x - self.oldX) * alpha))
		posY = (self.oldY + ((self.y - self.oldY) * alpha))
		if self.type == constants.GAMEOBJECT_PADDLE or self.type == constants.GAMEOBJECT_WALL:
			pygame.draw.rect(self.screen, self.color, [posX, posY, self.w, self.h], self.b)
		elif self.type == constants.GAMEOBJECT_BALL:
			pygame.draw.circle(self.screen, self.color, [int((posX + (self.w / 2.0))), int((posY + (self.w / 2.0)))], self.w, 1)

			
	def update(self):
		self.oldX = self.x
		self.oldY = self.y
		
			
class Paddle(GameObject):
	speed = 0
	player = None
	
	def __init__(self, mScreen, mPlayer):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_PADDLE, constants.PADDLE_WIDTH, constants.PADDLE_HEIGHT, 0, 0, constants.PADDLE_THICKNESS, constants.PADDLE_COLOR)
		self.player = mPlayer
		self.reset()
		
		
	def reset(self):
		if self.player == constants.PLAYER_ONE:
			self.x = (((constants.WINDOW_WIDTH + constants.GAMEAREA_WIDTH) / 2.0) - (constants.WALL_THICKNESS / 2.0) - self.w - (constants.BALL_SIZE * 2.0))
		else:
			self.x = (((constants.WINDOW_WIDTH - constants.GAMEAREA_WIDTH) / 2.0) + (constants.WALL_THICKNESS / 2.0) + (constants.BALL_SIZE * 2.0))
		self.y = ((constants.WINDOW_HEIGHT / 2.0) - (self.h / 2.0) + ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT)/2))
		self.speed = constants.PADDLE_STARTINGSPEED
		GameObject.update(self)
	
	
	def move(self, direction):
		GameObject.update(self)
		#print str(direction) + " " + str(self.speed)
		if direction == constants.DIRECTION_UP:
			self.y -= (self.speed * (constants.DELTATIME * (constants.GAME_SPEED / 5.0)))
		elif direction == constants.DIRECTION_DOWN:
			self.y += (self.speed * (constants.DELTATIME * (constants.GAME_SPEED / 5.0)))
			
			
class Ball(GameObject):
	speed = [0, 0]
	bounces = 0
	
	def __init__(self, mScreen, mX = 0, mY = 0):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_BALL, constants.BALL_SIZE, constants.BALL_SIZE, mX, mY, constants.BALL_THICKNESS, constants.BALL_COLOR)
		self.reset()
	
	
	def bounce(self, paddleH, paddleY, direction):
		# Calculate the angle (not really an angle, just a speed multiplier) at which the ball will bounce off the paddle
		angle = (((paddleY + (paddleH / 2.0) - (self.y + (constants.BALL_SIZE / 2.0))) / ((paddleH / 2.0) + constants.BALL_SIZE)) * 2.0)
		# Adjust ball speed vector's x-component depending on which paddle hit the ball
		if direction == constants.DIRECTION_LEFT:
			self.speed[0] = -constants.BALL_STARTINGSPEED
		elif direction == constants.DIRECTION_RIGHT:
			self.speed[0] = constants.BALL_STARTINGSPEED
		# Adjust ball speed vector's y-component accordingly
		self.speed[1] = (constants.BALL_STARTINGSPEED * -angle)
		# Calculate ball speed vector's length with pythagoras
		length = sqrt(pow(self.speed[0], 2) + pow(self.speed[1], 2))
		# Speed up the ball after every bounce off a paddle for added difficulty
		self.bounces += 1
		length = (length / (1 + (self.bounces / float(constants.BALL_BOUNCESPEEDUP))))
		# Normalize the ball speed
		self.speed[0] = (self.speed[0] / length) * constants.BALL_STARTINGSPEED
		self.speed[1] = (self.speed[1] / length) * constants.BALL_STARTINGSPEED
	
	
	def reset(self):
		self.speed = [constants.BALL_STARTINGSPEED, 0]
		self.bounces = 0
		self.x = (constants.WINDOW_WIDTH / 2.0) - (self.w / 2.0)
		self.y = ((constants.WINDOW_HEIGHT / 2.0) - (self.w / 2.0) + ((constants.WINDOW_HEIGHT - constants.GAMEAREA_HEIGHT) / 2.0))
		GameObject.update(self)
		
	
	def update(self):
		GameObject.update(self)
		self.x += (self.speed[0] * (constants.DELTATIME * (constants.GAME_SPEED / 10.0)))
		self.y += (self.speed[1] * (constants.DELTATIME * (constants.GAME_SPEED / 10.0)))
	
	
	def collidesWith(self, mGameObject):
		bX1 = (mGameObject.x - (mGameObject.b / 2.0))
		bY1 = (mGameObject.y - (mGameObject.b / 2.0))
		bX2 = (bX1 + mGameObject.w + (mGameObject.b))
		bY2 = (bY1 + mGameObject.h + (mGameObject.b))
		aX1 = (self.x - (self.w * 0.5))
		aY1 = (self.y - (self.w * 0.5))
		aX2 = aX1 + (self.w * 2.0)
		aY2 = aY1 + (self.w * 2.0)
		# todo: circle-square collision test
		return (aX1 < bX2 and aX2 > bX1 and aY1 < bY2 and aY2 > bY1)