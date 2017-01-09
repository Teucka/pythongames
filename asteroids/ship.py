from gameobject import *
from bullet import *

class Ship(GameObject):
	angle = 0
	dir = [0, 0]
	speed = [0, 0]
	accel = 0.0
	bulletTimer = 0.0
	shieldTimer = 0.0
	
	def __init__(self, mScreen):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_SHIP, constants.SHIP_WIDTH, constants.SHIP_HEIGHT, 0, 0, 0, constants.SHIP_COLOR)
		self.reset()
		
		
	def reset(self):
		self.y = ((constants.WINDOW_HEIGHT - constants.GAMEAREA_Y) / 2.0)
		self.x = (constants.WINDOW_WIDTH / 2.0) - (self.w / 2.0)
		self.oldX = self.x
		self.oldY = self.y
		self.angle = 180
		self.dir[0] = (1.0 * sin(radians(self.angle)))
		self.dir[1] = (1.0 * cos(radians(self.angle)))
		self.speed = [0, 0]
		self.accel = 0.1
		self.bulletTimer = 0.0
		self.shieldTimer = constants.GAME_SHIELDDURATION
		
		
	def turn(self, direction):
		if direction == constants.DIRECTION_LEFT:
			if self.angle < 360:
				self.angle += 1
			else:
				self.angle = 0
			self.dir[0] = (1.0 * sin(radians(self.angle)))
			self.dir[1] = (1.0 * cos(radians(self.angle)))
		elif direction == constants.DIRECTION_RIGHT:
			if self.angle > 0:
				self.angle -= 1
			else:
				self.angle = 360
			self.dir[0] = (1.0 * sin(radians(self.angle)))
			self.dir[1] = (1.0 * cos(radians(self.angle)))
			
			
	def update(self):
		GameObject.update(self)
		self.x += self.speed[0]
		self.y += self.speed[1]
		if self.accel > -0.01 and self.accel < 0.01:
			self.accel = 0
		elif self.accel > 0:
			self.accel -= 0.01
		elif self.accel < 0:
			self.accel += 0.01
		self.bulletTimer -= (constants.DELTATIME / 1000.0)
		self.shieldTimer -= (constants.DELTATIME / 1000.0)
		
		
	def move(self, direction):
		GameObject.update(self)
		
		if direction == constants.DIRECTION_UP:
			self.accel = constants.SHIP_MAXSPEED
		elif direction == constants.DIRECTION_DOWN:
			self.accel = 0
		
		newSpeed = [((self.accel * (constants.DELTATIME * (constants.GAME_SPEED / 25.0))) * self.dir[0]), ((self.accel * (constants.DELTATIME * (constants.GAME_SPEED / 25.0))) * self.dir[1])]
		
		deltaX = abs(newSpeed[0] - self.speed[0])
		deltaY = abs(newSpeed[1] - self.speed[1])
		
		if deltaX >= deltaY:
			if deltaX == 0:
				deltaY = 0
			else:
				deltaY = ((deltaY / deltaX) * 0.005)
			deltaX = 0.005
		elif deltaY >= deltaX:
			if deltaY == 0:
				deltaX = 0
			else:
				deltaX = ((deltaX / deltaY) * 0.005)
			deltaY = 0.005

		if abs(newSpeed[0] - self.speed[0]) < 0.005:
			self.speed[0] = newSpeed[0]
		elif newSpeed[0] < self.speed[0]:
			self.speed[0] -= deltaX
		elif newSpeed[0] > self.speed[0]:
			self.speed[0] += deltaX
		if abs(newSpeed[1] - self.speed[1]) < 0.005:
			self.speed[1] = newSpeed[1]
		elif newSpeed[1] < self.speed[1]:
			self.speed[1] -= deltaY
		elif newSpeed[1] > self.speed[1]:
			self.speed[1] += deltaY

			
	def shoot(self):
		if self.bulletTimer <= 0:
			mBullet = Bullet(self.screen, self.x, self.y)
			mBullet.speed = [self.dir[0], self.dir[1]]
			self.bulletTimer = constants.SHIP_SHOOTDELAY
			return mBullet