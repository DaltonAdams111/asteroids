import sys
import pygame
import pygame_menu
from pygame_menu import themes
from time import sleep

import pygame_menu.events
import pygame_menu.font
import pygame_menu.locals
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
high_scores = pygame_menu.menu.Menu("High Scores", SCREEN_WIDTH, SCREEN_HEIGHT, enabled=False, theme=pygame_menu.themes.THEME_DARK)

scores = []
with open("scores.txt", "r") as file:
	for line in file.readlines(-3):
		scores.append({"name": line.split(", ")[0], "score": int(line.split(", ")[1].replace("\n", ""))})

difficulty = 1
def setDifficulty(selected, value):
	global difficulty
	difficulty = value

player_name = ""
def setPlayerName(name):
	global player_name
	player_name = name

def mainMenu():
	main_menu.clear()
	main_menu.add.text_input("Name: ", default="ZZZ", valid_chars=list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"), input_type=pygame_menu.locals.INPUT_TEXT, maxchar=3, onchange=setPlayerName)
	main_menu.add.selector("Difficulty: ", [("EASY", 2.0), ("MEDIUM", 1.0), ("HARD", 0.5)], onchange=setDifficulty)
	main_menu.add.button("Play", startGame)
	main_menu.add.button("Quit", pygame_menu.events.EXIT)
	main_menu.add.button("High Scores", action=highScores)
	main_menu.enable()
	main_menu.mainloop(screen)

def gameOver(player_name, player_score):
	game_over.clear()
	game_over.add.label("GAME OVER\n")
	game_over.add.label(f"Score: {player_score}\n")
	for i in range(3):
		if player_score > scores[i]["score"]:
			scores.insert(i, {"name": player_name, "score": player_score})
			game_over.add.button(f'Save Score: {player_name}, {player_score}', action=saveScore)
			break
	
	game_over.add.button("Replay", startGame)
	game_over.add.button("Main Menu", mainMenu)
	game_over.add.button("Quit", pygame_menu.events.EXIT)
	game_over.add.button("High Scores", action=highScores)
	game_over.enable()
	game_over.mainloop(screen)

def highScores():
	high_scores.clear()
	high_scores.add.label(title=f'{scores[0]["name"]}: {scores[0]["score"]}\n{scores[1]["name"]}: {scores[1]["score"]}\n{scores[2]["name"]}: {scores[2]["score"]}\n\n')
	high_scores.add.button(title="Back", action=high_scores.disable)
	high_scores.enable()
	high_scores.mainloop(screen)

def saveScore():
	with open("scores.txt", "w") as file:
		for i in range(3):
			file.write(f'{scores[i]["name"]}, {scores[i]["score"]}\n')
	score_saved = game_over.add.label(title="Score Saved!", selectable=False)
	game_over.remove_widget(game_over.get_selected_widget())
	game_over.move_widget_index(score_saved, 4)

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

	global player_name
	if player_name == "":
		player_name = "ZZZ"
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, player_name)
	asteroidfield = AsteroidField(difficulty)

	dt = 0

	def update():
		for obj in updatable:
			obj.update(dt)

	def check_collisions():
		global player_score
		for asteroid in asteroids:
			if asteroid.isColliding(player):
				gameOver(player.name, player.score)
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
