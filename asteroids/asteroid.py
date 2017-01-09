from gameobject import *

class Asteroid(GameObject):
	hits = 0
	size = 1
	dir = [0, 0]
	speed = 0
	
	def __init__(self, mScreen, mX, mY, mSize):
		self.size = mSize
		width = int(constants.ASTEROID_SIZE * (0.25 + (mSize * 0.75)))
		self.w = width
		self.h = width
		self.dir = [random.uniform(-1, 1), random.uniform(-1, 1)]
		self.speed = random.uniform(constants.GAME_ASTEROIDMINSPEED, constants.GAME_ASTEROIDMAXSPEED)
		GameObject.__init__(self, mScreen, constants.GAMEOBJECT_ASTEROID, width, width, mX, mY, constants.ASTEROID_THICKNESS, constants.ASTEROID_COLOR)
	
	
	def update(self):
		GameObject.update(self)
		self.x += self.speed * self.dir[0]
		self.y += self.speed * self.dir[1]
		
		
	def collidesWith(self, mGameObject):
		if mGameObject.enabled == False or self.enabled == False:
			return 0
		
		for i in range(0, 2):
			startPoint = [mGameObject.x, mGameObject.y]
			if i == 0:
				endPoint = [mGameObject.x - mGameObject.dir[0] * constants.SHIP_HEIGHT + constants.SHIP_WIDTH * 0.5 * mGameObject.dir[1], mGameObject.y - mGameObject.dir[1] * constants.SHIP_HEIGHT - constants.SHIP_WIDTH * 0.5 * mGameObject.dir[0]]
			else:
				endPoint = [mGameObject.x - mGameObject.dir[0] * constants.SHIP_HEIGHT - constants.SHIP_WIDTH * 0.5 * mGameObject.dir[1], mGameObject.y - mGameObject.dir[1] * constants.SHIP_HEIGHT + constants.SHIP_WIDTH * 0.5 * mGameObject.dir[0]]
				
			centerSphere = [(self.x + (self.w * 0.5)), (self.y + (self.h * 0.5))]
			a = numpy.dot([endPoint[0] - startPoint[0], endPoint[1] - startPoint[1]], [endPoint[0] - startPoint[0], endPoint[1] - startPoint[1]])
			b = 2.0 * numpy.dot([startPoint[0] - centerSphere[0], startPoint[1] - centerSphere[1]], [endPoint[0] - startPoint[0], endPoint[1] - startPoint[1]])
			c = numpy.dot([startPoint[0] - centerSphere[0], startPoint[1] - centerSphere[1]], [startPoint[0] - centerSphere[0], startPoint[1] - centerSphere[1]]) - self.w * self.w
			
			discriminant = b * b -4 * a * c;
			
			if discriminant >= 0:
				discriminant = sqrt(discriminant)
				t1 = (-b - discriminant)/(2*a)
				t2 = (-b + discriminant)/(2*a)
				if t1 >= 0 and t1 <= 1:
					return 1
				elif t2 >= 0 and t2 <= 1:
					return 1
		return 0