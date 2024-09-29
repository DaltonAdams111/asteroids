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
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

main_menu = pygame_menu.menu.Menu("Main Menu", SCREEN_WIDTH, SCREEN_HEIGHT, enabled=True, theme=pygame_menu.themes.THEME_DARK)
game_over = pygame_menu.menu.Menu("Game Over", SCREEN_WIDTH, SCREEN_HEIGHT, enabled=False, theme=pygame_menu.themes.THEME_DARK)

difficulty = 1
def set_difficulty(selected, value):
	global difficulty
	difficulty = value

def mainMenu():
	main_menu.clear()
	user_name = main_menu.add.text_input("Name: ", default="ZZZ", maxchar=3)
	main_menu.add.selector("Difficulty: ", [("EASY", 2.0), ("MEDIUM", 1.0), ("HARD", 0.5)], onchange=set_difficulty)
	main_menu.add.button("Play", startGame)
	main_menu.add.button("Quit", pygame_menu.events.EXIT)
	main_menu.enable()
	main_menu.mainloop(screen)

def gameOver(score):
	game_over.clear()
	game_over.add.label("GAME OVER\n")
	game_over.add.label(f"Score: {score}\n")
	game_over.add.button("Replay", startGame)
	game_over.add.button("Main Menu", mainMenu)
	game_over.add.button("Quit", pygame_menu.events.EXIT)
	game_over.enable()
	game_over.mainloop(screen)

def startGame():
	main_menu.disable()
	game_over.disable()

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

	def update():
		for obj in updatable:
			obj.update(dt)

	def check_collisions():
		global player_score
		for asteroid in asteroids:
			if asteroid.isColliding(player):
				gameOver(player.score)
			for shot in shots:
				if asteroid.isColliding(shot):
					if not asteroid.withinScreen():
						continue
					asteroid.split()
					shot.kill()
					player.score += 1

	def draw():
		screen.fill("black")
		for obj in drawable:
			obj.draw(screen)
		pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		update()

		check_collisions()

		draw()

		dt = clock.tick(60) / 1000

if __name__ == "__main__":
	mainMenu()
