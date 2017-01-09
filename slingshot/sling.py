from constants import *
import pygame
from math import sqrt, atan2, pi, sin, cos

class Sling:
	screen = None
	initialPos = [0, 0]
	dragPos = [0, 0]
	ball = None
	
	def __init__(self, mScreen, mAttachedBall, mPos):
		self.screen = mScreen
		self.ball = mAttachedBall
		self.ball.pos = mPos
		self.ball.oldPos = mPos
		self.initialPos = [mPos[0], mPos[1]]
	
	
	def draw(self, alpha = 0):
			if self.ball.dragging:
				pygame.draw.line(self.screen, SLING_COLOR, self.ball.pos, self.initialPos, 1)
			if self.ball != None:
				self.ball.draw(alpha)
	
	
	def reset(self):
		self.ball.pos = [self.initialPos[0], self.initialPos[1]]
		self.ball.oldPos = self.ball.pos
		self.angle = 0
		self.len = 0
	
	
	def update(self):
		self.ball.update()
		
		
	def isHit(self, hitPos):
		dis = sqrt(pow((self.ball.pos[0] - hitPos[0]), 2) + pow((self.ball.pos[1] - hitPos[1]), 2))
		if dis <= self.ball.w:
			return True
			
			
	def attach(self, mBall):
		self.ball = mBall
		self.ball.pos = [self.initialPos[0], self.initialPos[1]]
		self.ball.oldPos = self.ball.pos
			
			
	def startDragging(self, mDragPos):
		self.dragPos = mDragPos
		self.ball.select()
		
		
	def letGo(self):
		deltaX = self.initialPos[0] - self.ball.pos[0]
		deltaY = self.initialPos[1] - self.ball.pos[1]
		len = sqrt(pow(deltaX, 2) + pow(deltaY, 2))
		if len > SLING_LENGTH / 3.0:
			angle = -(atan2(deltaY, deltaX) + pi * 0.5)
			self.ball.sling(angle, len)
			return True
		return False
		
		
	def drag(self, mDragPos):
		deltaX = self.initialPos[0] - mDragPos[0]
		deltaY = self.initialPos[1] - mDragPos[1]
		len = sqrt(pow(deltaX, 2) + pow(deltaY, 2))
		self.ball.oldPos = self.ball.pos

		if len <= SLING_LENGTH:
			self.ball.pos[0] -= (self.dragPos[0] - mDragPos[0])
			self.ball.pos[1] -= (self.dragPos[1] - mDragPos[1])
		else:
			angle = -(atan2(deltaY, deltaX) + pi * 0.5)
			self.ball.pos[0] = (SLING_LENGTH * sin(angle)) + self.initialPos[0]
			self.ball.pos[1] = (SLING_LENGTH * cos(angle)) + self.initialPos[1]
		self.dragPos = mDragPos
			