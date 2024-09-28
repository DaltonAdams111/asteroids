import sys
import pygame
import pygame_menu
from pygame_menu import themes
from time import sleep
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (updatable, drawable, asteroids)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroidfield = AsteroidField()

	dt = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("Game closed")
				print(f"Score: {player.score}")
				return

		for obj in updatable:
			obj.update(dt)

		for asteroid in asteroids:
			if asteroid.isColliding(player):
				print("Game over!")
				print(f"Score: {player.score}")
				sys.exit()
			for shot in shots:
				if asteroid.isColliding(shot):
					if not asteroid.withinScreen():
						continue
					asteroid.split()
					shot.kill()
					player.score += 1

		screen.fill("black")
		for obj in drawable:
			obj.draw(screen)

		pygame.display.flip()

		dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
