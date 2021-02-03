
import pygame
import os
from car import Car
from car import AutonomousCar
from car import ControllerCar
from wall import Wall
from wall import ParkingSlot
from math import copysign


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class Game:
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	WINDOW_WIDTH = 900
	WINDOW_HEIGHT = 500
	def __init__(self):
		pygame.init()
		width, height = 900, 500
		pygame.display.set_caption('Car parking with fuzzy sets')
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.fps = 60
		self.__add_game_objects()
		self.exit = False

	def draw_objects(self):
		self.screen.fill(self.WHITE)
		self.all_sprites.draw(self.screen)
		pygame.display.update()

	def __add_game_objects(self):
		self.all_sprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.car = AutonomousCar(600, 240 + 64)
		# self.car = ControllerCar(200, 140 + 64)
		self.all_sprites.add(self.car)
		# Create walls starting from 0 (x) 140 (y)
		# Center of the parking slot is 40(x)
		# Slot width is 80 px
		# Slot height is 140 px
		self.parking_slot = ParkingSlot(0, 140, 40, 80, 140)
		for w in self.parking_slot.walls:
			self.all_sprites.add(w)
			self.walls.add(w)

		self.car.walls = self.walls

	def run(self):
		car = self.car
		while not self.exit:
			dt = self.clock.get_time() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit = True			
			# self.car.update(dt)
			self.car.autonomouse_steering(dt, self.parking_slot.slot_x + self.parking_slot.slot_width/2, self.parking_slot.slot_height)
			self.draw_objects()
			self.clock.tick(self.fps)
		pygame.quit()

if __name__ == '__main__':
	game = Game()
	game.run()
