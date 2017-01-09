import constants
import pygame

class Shape:
	x = None
	y = None
	w = None
	h = None
	b = None
	type = None
	color = None
	
	def __init__(self, mType, mX, mY, mW, mH, mB = 0, mColor = constants.BLACK):
		self.type = mType
		self.x = (mX - (mW / 2.0))
		self.y = (mY - (mH / 2.0))
		self.w = mW
		self.h = mH
		self.b = mB
		self.color = mColor
		
	
	def draw(self, mScreen):
		if self.type == constants.SHAPE_RECT:
			pygame.draw.rect(mScreen, self.color, [self.x, self.y, self.w, self.h], self.b)
		elif self.type == constants.SHAPE_CIRCLE:
			pygame.draw.circle(mScreen, self.color, [int((self.x + (self.w / 2.0))), int((self.y + (self.w / 2.0)))], self.w, 0)