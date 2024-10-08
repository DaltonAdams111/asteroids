import pygame
import random
import time
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)
		self.spawntime = time.time()
		self.lifetime = 0

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, 2)

	def update(self, dt):
		self.position += self.velocity * dt
		self.lifetime = time.time() - self.spawntime
		if self.lifetime < 10:
			return
		if not self.withinBounds():
			self.kill()

	def split(self):
		self.kill()

		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		
		rand_angle = random.uniform(20, 50)
		ange_1 = self.velocity.rotate(rand_angle)
		ange_2 = self.velocity.rotate(-rand_angle)

		new_radius = self.radius - ASTEROID_MIN_RADIUS
		spawn_1 = Asteroid(self.position.x, self.position.y, new_radius)
		spawn_1.velocity = ange_1 * 1.2
		spawn_2 = Asteroid(self.position.x, self.position.y, new_radius)
		spawn_2.velocity = ange_2 * 1.2

	def withinScreen(self):
		return (0 - self.radius < self.position.x < SCREEN_WIDTH + self.radius and 0 - self.radius < self.position.y < SCREEN_HEIGHT + self.radius)