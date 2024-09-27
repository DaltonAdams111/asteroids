import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, SHOT_RADIUS)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, 2)

	def update(self, dt):
		self.position += self.velocity * dt
		if self.position.x < -SCREEN_BOUNDARY_X or self.position.x > SCREEN_BOUNDARY_X:
			self.kill()
		if self.position.y < -SCREEN_BOUNDARY_Y or self.position.y > SCREEN_BOUNDARY_Y:
			self.kill()