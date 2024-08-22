import pygame
from constants import *

def main():
	pygame.init()
	running = True
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		screen.fill(000)
		pygame.display.flip()

if __name__ == "__main__":
	main()
