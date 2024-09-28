import sys
import pygame
import pygame_menu
from pygame_menu import themes
from time import sleep

import pygame_menu.events
import pygame_menu.menu
import pygame_menu.themes
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

difficulty = 1
def set_difficulty(selected, value):
	global difficulty
	difficulty = value
	print(f"Difficulty: {selected[0][0]}, Value: {selected[0][1]}")

def start_game():
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (updatable, drawable, asteroids)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroidfield = AsteroidField(difficulty)

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
				main_menu.mainloop(screen)
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

main_menu = pygame_menu.menu.Menu("Main Menu", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
main_menu.add.text_input("Name: ", default="ZZZ", maxchar=3)
main_menu.add.selector("Difficulty: ", [("EASY", 2.0), ("MEDIUM", 1.0), ("HARD", 0.5)], onchange=set_difficulty)
main_menu.add.button("Play", start_game)
main_menu.add.button("Quit", pygame_menu.events.EXIT)

if __name__ == "__main__":
	main_menu.mainloop(screen)
