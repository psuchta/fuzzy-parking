import pygame

class Wall(pygame.sprite.Sprite):
	BLACK = (0,0,0)
	def __init__(self, x, y, width = 2, height = 2):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(self.BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.mask = pygame.mask.from_surface(self.image)

class ParkingSlot():
	def __init__(self, x, y, slot_x, slot_width, slot_height, wall_size = 2):
		self.x = x
		self.y = y
		self.slot_x = slot_x
		self.slot_width = slot_width
		self.slot_height = slot_height
		self.walls = pygame.sprite.Group()
		self.wall_size = wall_size
		self.__create_slot()

	def __create_slot(self):
		self.walls.add(Wall(self.x, self.y, self.slot_x - self.slot_width / 2, self.wall_size))
		# Additional wall for spare square between first vertical and horizontal line 
		self.walls.add(Wall(self.slot_x - self.slot_width / 2, self.y, self.wall_size, self.wall_size))
		self.walls.add(Wall(self.slot_x - self.slot_width / 2, self.y - self.slot_height, self.wall_size, self.slot_height))
		self.walls.add(Wall(self.slot_x - self.slot_width / 2, self.y - self.slot_height, self.slot_width, self.wall_size))
		self.walls.add(Wall(self.slot_x + self.slot_width / 2, self.y - self.slot_height, self.wall_size, self.slot_height))
		self.walls.add(Wall(self.slot_x + self.slot_width / 2, self.y, 900, self.wall_size))


