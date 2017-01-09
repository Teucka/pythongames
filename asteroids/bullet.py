from gameobject import *

class Bullet(GameObject):
	speed = [0, 0]
	timeToLive = 0
	
	def __init__(self, mScreen, mX = 0, mY = 0):
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_BULLET, constants.BULLET_SIZE, constants.BULLET_SIZE, mX, mY, constants.BULLET_THICKNESS, constants.BULLET_COLOR)
		self.reset()
		
		
	def reset(self):
		self.speed = [0, 0]
		self.timeToLive = constants.BULLET_TIMETOLIVE
		self.oldX = self.x
		self.oldY = self.y
		
		
	def update(self):
		if self.timeToLive <= 0:
			self.disable()
		else:
			self.timeToLive -= (constants.DELTATIME / 1000.0)
			
		GameObject.update(self)
		
		self.x += ((self.speed[0] * (constants.DELTATIME * (constants.GAME_SPEED / 25.0))) * constants.BULLET_SPEED)
		self.y += ((self.speed[1] * (constants.DELTATIME * (constants.GAME_SPEED / 25.0))) * constants.BULLET_SPEED)
		
		
	def move(self, mX, mY):
		GameObject.update(self)
		self.x = mX
		self.y = mY
		
		
	def collidesWith(self, mGameObject):
		if mGameObject.enabled == False or self.enabled == False:
			return 0
			
		bX1 = (mGameObject.x - (mGameObject.w / 2.0))
		bY1 = (mGameObject.y - (mGameObject.h / 2.0))
		bX2 = (bX1 + mGameObject.w * 2.0)
		bY2 = (bY1 + mGameObject.h * 2.0)
		aX1 = (self.x - (self.w / 2.0))
		aY1 = (self.y - (self.w / 2.0))
		aX2 = (aX1 + (self.w * 2.0))
		aY2 = (aY1 + (self.w * 2.0))

		#pygame.draw.line(self.screen, constants.BLACK, [aX1, aY1], [aX2, aY2], 1)
		#pygame.draw.line(self.screen, constants.GREEN, [(self.x + (self.w * 0.5)), (self.y + (self.h * 0.5))], [(mGameObject.x + (mGameObject.w * 0.5)), (mGameObject.y + (mGameObject.h * 0.5))], 1)
		#pygame.display.flip()
		if (aX1 < bX2 and aX2 > bX1 and aY1 < bY2 and aY2 > bY1):
				centerDistance = sqrt(pow(((self.x + (self.w * 0.5)) - (mGameObject.x + (mGameObject.w * 0.5))), 2) + pow(((self.y + (self.h * 0.5)) - (mGameObject.y + (mGameObject.h * 0.5))), 2))
				if centerDistance <= ((self.w + mGameObject.w)):
					return 1
		return 0