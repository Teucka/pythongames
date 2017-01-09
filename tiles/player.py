import pygame
from constants import *

class Player:
	screen = None
	pos = [0, 0]
	oldPos = [0, 0]
	image = None
	speed = 0
	
	def __init__(self, mScreen, mPos, mImage):
		self.screen = mScreen
		self.pos = mPos
		self.image = mImage
		self.speed = ((GAME_PLAYERSPEED * 0.01) * GAME_SPEED)
		
		
	def update(self):
		self.oldPos[0] = self.pos[0]
		self.oldPos[1] = self.pos[1]
		
		
	def move(self, dir):
		if dir == DIRECTION_UP:
			self.pos[1] -= self.speed
		elif dir == DIRECTION_DOWN:
			self.pos[1] += self.speed
		elif dir == DIRECTION_LEFT:
			self.pos[0] -= self.speed
		elif dir == DIRECTION_RIGHT:
			self.pos[0] += self.speed
		
		
	def draw(self, alpha = 0):
		posX = (self.oldPos[0] + ((self.pos[0] - self.oldPos[0]) * alpha))
		posY = (self.oldPos[1] + ((self.pos[1] - self.oldPos[1]) * alpha))
		self.screen.blit(self.image, ((posX * TILE_SIZE), (posY * TILE_SIZE)))