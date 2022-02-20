import pygame
from player import Player
from chunk import Chunk
from blocks import *
from entity import Entity

pygame.init()

WIDTH, HEIGHT = 1280, 720 #will be 40, 22.5 in IG coords
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

chunk = Chunk.get_chunk(0, 0)
chunk.add_obj(Dirt(2, 22))
player = Player(chunk, 0, 0)

if __name__ == "__main__":
    while True:
        screen.fill("white")
        
        player.input_movement()
        Entity.update_entities(fps)

        player.screen_bound() # Test Methode
        
        player.apply_movement(fps)

        print(player.pos)

        screen.blit(player.gfx, player.pos)
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        pygame.display.update()
        clock.tick(fps)
