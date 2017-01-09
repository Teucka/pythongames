from constants import *
import pygame
from math import sin, cos, sqrt

class Ball:
	screen = None
	color = None
	selectedColor = None
	w = 0
	h = 0
	thickness = 0
	pos = [0, 0]
	oldPos = [0, 0]
	dragging = False
	attached = True
	dir = [0, 0]
	speed = 0
	distanceMoved = 0
	slingshotLength = 0
	
	def __init__(self, mScreen):
		self.screen = mScreen
		self.color = BALL_COLOR
		self.selectedColor = BALL_SELECTEDCOLOR
		self.w = BALL_SIZE
		self.h = BALL_SIZE
		self.thickness = BALL_THICKNESS
	
	
	def draw(self, alpha = 0):
		if self.dragging:
			color = self.selectedColor
		else:
			color = self.color
		posX = (self.oldPos[0] + ((self.pos[0] - self.oldPos[0]) * alpha))
		posY = (self.oldPos[1] + ((self.pos[1] - self.oldPos[1]) * alpha))
		pygame.draw.circle(self.screen, color, [int(posX), int(posY)], self.w, 0)
	
	
	def update(self):
		self.oldPos = self.pos
		if self.attached == False:
			self.pos[0] += self.speed[0]
			self.pos[1] += self.speed[1]
			self.distanceMoved += sqrt(pow(self.speed[0], 2) + pow(self.speed[1], 2))
			if self.pos[1] >= WINDOW_HEIGHT - self.w:
				self.pos[1] = WINDOW_HEIGHT - self.w
				self.speed = [0, 0]
			else:
				if self.distanceMoved > self.shotLength: 
					self.speed[1] += 0.02
		
		
	def select(self):
		self.dragging = True
		
		
	def deselect(self):
		self.dragging = False
		
		
	def detach(self):
		self.attached = False
		
		
	def sling(self, angle, mShotLength):
		self.deselect()
		self.detach()
		self.shotLength = mShotLength
		power = self.shotLength / SLING_LENGTH
		self.dir = [-sin(angle), -cos(angle)]
		self.speed = [BALL_STARTINGSPEED * power * self.dir[0], BALL_STARTINGSPEED * power * self.dir[1]]