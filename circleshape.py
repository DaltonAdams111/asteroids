import pygame
from constants import *

class CircleShape(pygame.sprite.Sprite):
	def __init__(self, x, y, radius):
		if hasattr(self, "containers"):
			super().__init__(self.containers)
		else:
			super().__init__()

		self.position = pygame.Vector2(x, y)
		self.velocity = pygame.Vector2(0, 0)
		self.radius = radius

	def draw(self, screen):
		pass

	def update(self, dt):
		pass

	def isColliding(self, target):
		return self.position.distance_to(target.position) < self.radius + target.radius
	
	def withinBounds(self):
		return (-SCREEN_WIDTH / 2 < self.position.x < SCREEN_WIDTH * 1.5 and -SCREEN_HEIGHT / 2 < self.position.y < SCREEN_HEIGHT * 1.5)
	
	def withinScreen(self):
		return (0 < self.position.x < SCREEN_WIDTH and 0 < self.position.y < SCREEN_HEIGHT)
