import pygame
from constants import *

class Tile:
	screen = None
	pos = [0, 0]
	
	def __init__(self, mScreen, mPos):
		self.screen = mScreen
		self.pos = mPos
		
		
	def draw(self):
			if self.ball.dragging:
				pygame.draw.line(self.screen, SLING_COLOR, self.ball.pos, self.initialPos, 1)
			if self.ball != None:
				self.ball.draw(alpha)