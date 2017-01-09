import constants

class Menu:
	font = None
	screen = None
	items = []
	
	def __init__(self, mFont, mScreen):
		self.font = mFont
		self.screen = mScreen
		self.items = []
	
	
	def addItem(self, menuItem):
		self.items.append(menuItem)

		
class TextItem:
	text = "Text Item"
	targetX = None
	x = None
	y = None
	w = None
	
	def __init__(self, mFont, mText, mX, mY):
		self.text = mText
		self.w, h = mFont.size(mText)
		self.targetX = mX
		self.update(mFont)
		self.y = (mY - (h / 2.0))
	
	
	def update(self, mFont):
		self.w, h = mFont.size(self.text)
		self.x = (self.targetX - (self.w / 2.0))

		
class Text(Menu):
	
	def __init__(self, mFont, mScreen):
		Menu.__init__(self, mFont, mScreen)
	
	
	def draw(self):
		for i in self.items:
			surface = self.font.render(i.text, True, constants.BLACK, constants.WHITE)
			self.screen.blit(surface, [i.x, i.y])
		
		
class SelectableItem:
	text = "Selectable Item"
	action = 0
	
	def __init__(self, mText, mAction):
		self.text = mText
		self.action = mAction
	
	
class Selectable(Menu):
	
	def __init__(self, mFont, mScreen):
		Menu.__init__(self, mFont, mScreen)
	
	
	def draw(self, selection):
		iter = 0.0
		for i in self.items:
			# Selected menu item is red instead of black
			if iter == selection:
				c = constants.RED
			else:
				c = constants.BLACK
			w, h = self.font.size(i.text)
			x = (constants.WINDOW_WIDTH / 2.0) - (w / 2.0)
			y = (constants.WINDOW_HEIGHT / 2.0) - (h / 2.0)
			s = len(self.items)
			if iter == ((s / 2.0) - 0.5):
				y += 0
			elif iter < ((s / 2.0) - 0.5):
				y -= (h * 1.5) * ((s / 2.0) - 0.5)
			else:
				y += (h * 1.5) * ((s / 2.0) - 0.5)
			surface = self.font.render(i.text, True, c)
			self.screen.blit(surface, [x, y])
			iter += 1.0