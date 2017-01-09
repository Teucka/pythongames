import constants
import pygame
		
class Shape:
	x = None
	y = None
	w = None
	h = None
	thickness = None
	type = None
	color = None
	
	def __init__(self, mType, mX, mY, mW, mH, mThickness = 0, mColor = constants.BLACK):
		self.type = mType
		self.x = (mX - (mW / 2.0))
		self.y = (mY - (mH / 2.0))
		self.w = mW
		self.h = mH
		self.thickness = mThickness
		self.color = mColor
	
	
	def draw(self, screen):
		if self.type == constants.SHAPE_RECT:
			pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], self.thickness)
		elif self.type == constants.SHAPE_CIRCLE:
			pygame.draw.circle(screen, self.color, [int((self.x + (self.w / 2.0))), int((self.y + (self.w / 2.0)))], self.w, 0)
		elif self.type == constants.SHAPE_SHIP:
			endPoint = [self.x, self.y]
			startPoint1 = [self.x + self.w * -0.75, self.y + -1.5 * self.h]
			startPoint2 = [self.x - self.w * -0.75, self.y + -1.5 * self.h]
			pygame.draw.line(screen, self.color, startPoint1, endPoint, 1)
			pygame.draw.line(screen, self.color, startPoint2, endPoint, 1)