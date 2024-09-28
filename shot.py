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
		if not -SCREEN_WIDTH / 2 < self.position.x < SCREEN_WIDTH * 1.5 or not -SCREEN_HEIGHT / 2 < self.position.y < SCREEN_HEIGHT * 1.5:
			self.kill()