import pygame
from player import Player
from chunk import Chunk
from blocks import *

pygame.init()

WIDTH, HEIGHT = 1280, 720
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

player = Player(0, 0, 3, 3)

if __name__ == "__main__":
    while True:
        screen.fill("white")
        
        player.input_movement()
        player.screen_bound() # Test Methode
        
        player.apply_movement(fps)
        screen.blit(player.gfx, player.pos)
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        pygame.display.update()
        clock.tick(fps)
