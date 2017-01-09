import pygame
from constants import *
from math import floor

class Level:
	screen = None
	map = []
	width = 0
	height = 0
	tileset = []
	tilesetWidth = 0
	tilesetHeight = 0
	collisionMap = []
	startingPoint = [0, 0]
	
	def __init__(self, mScreen, mTileset):
		self.screen = mScreen
		self.tileset = mTileset
		self.tilesetWidth = len(mTileset[0]) - 1
		self.tilesetHeight = len(mTileset)
		
		
	def setMap(self, mMap, mWidth, mHeight):
		self.map = mMap
		self.width = mWidth
		self.height = mHeight
		
		
	def setCollisionMap(self, mCollisionMap, mWidth, mHeight):
		self.collisionMap = mCollisionMap
		self.width = mWidth
		self.height = mHeight
		for i in range(0, mWidth):
			for j in range(0, mHeight):
				if mCollisionMap[j][i] == COL_STARTINGPOINT:
					self.startingPoint = [i, j]
		
		
	def getStartingPoint(self):
		return self.startingPoint
		
		
	def isWalkable(self, mX, mY):
		return int(self.collisionMap[int(mY)][int(mX)])
		
		
	def draw(self):
		for i in range(0, self.width):
			for j in range(0, self.height):
				tile = int(self.map[j][i])
				x = (int(floor((tile - 1) / self.tilesetHeight)))
				y = ((tile - 1) % self.tilesetWidth)
				self.screen.blit(self.tileset[y][x], ((i * TILE_SIZE), (j * TILE_SIZE)))