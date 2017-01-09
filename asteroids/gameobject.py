import constants
import pygame
from math import sqrt, ceil, sin, cos, radians
import random
import numpy

class GameObject:
	screen = None
	type = None
	color = None
	enabled = True
	w = 0
	h = 0
	x = 0.0
	y = 0.0
	thickness = 0
	oldX = 0.0
	oldY = 0.0
	
	def __init__(self, mScreen, mType, mW, mH, mX, mY, mThickness, mColor):
		self.screen = mScreen
		self.type = mType
		self.w = mW
		self.h = mH
		self.x = mX
		self.y = mY
		self.thickness = mThickness
		self.oldX = mX
		self.oldY = mY
		self.color = mColor
	
	
	def draw(self, alpha = 0):
		if self.enabled:
			posX = (self.oldX + ((self.x - self.oldX) * alpha))
			posY = (self.oldY + ((self.y - self.oldY) * alpha))
			if self.type == constants.GAMEOBJECT_WALL:
				pygame.draw.rect(self.screen, self.color, [posX, posY, self.w, self.h], self.thickness)
			elif self.type == constants.GAMEOBJECT_BULLET or self.type == constants.GAMEOBJECT_ASTEROID:
				pygame.draw.circle(self.screen, self.color, [int((posX + (self.w / 2.0))), int((posY + (self.w / 2.0)))], self.w, 0)
				#pygame.draw.rect(self.screen, self.color, [(posX - (self.w / 2.0)), (posY - (self.w / 2.0)), (self.w * 2.0), (self.h * 2.0)], 1)
			elif self.type == constants.GAMEOBJECT_SHIP:
				startPoint = [posX, posY]
				endPoint1 = [posX - self.dir[0] * constants.SHIP_HEIGHT + constants.SHIP_WIDTH * 0.5 * self.dir[1], posY - self.dir[1] * constants.SHIP_HEIGHT - constants.SHIP_WIDTH * 0.5 * self.dir[0]]
				endPoint2 = [posX - self.dir[0] * constants.SHIP_HEIGHT - constants.SHIP_WIDTH * 0.5 * self.dir[1], posY - self.dir[1] * constants.SHIP_HEIGHT + constants.SHIP_WIDTH * 0.5 * self.dir[0]]
				pygame.draw.line(self.screen, self.color, startPoint, endPoint1, 1)
				pygame.draw.line(self.screen, self.color, startPoint, endPoint2, 1)
				if self.shieldTimer > 0:
					posX -= constants.SHIP_WIDTH * 0.75 * self.dir[0]
					posY -= constants.SHIP_HEIGHT * 0.5 * self.dir[1] + constants.SHIP_HEIGHT * 0.66
					pygame.draw.circle(self.screen, constants.SHIELD_COLOR, [int(posX), int(posY + (self.w))], int(self.w * 1.5), constants.SHIELD_THICKNESS)
	
	
	def disable(self):
		self.enabled = False
	
	
	def enable(self):
		self.enabled = True
	
	
	def update(self):
		self.oldX = self.x
		self.oldY = self.y