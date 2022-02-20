import pygame
from player import Player
from chunk import Chunk
from blocks import *
from entity import Entity
from gui import FontRenderer
from render import Render

pygame.init()

WIDTH, HEIGHT = 1280, 720 #will be 40, 22.5 in IG coords
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

chunk = Chunk.get_chunk(0, 0)
player = Player(chunk, 0, 0)

fontrenderer = FontRenderer(screen)

if __name__ == "__main__":
    while True:
        screen.fill("white")
        player.input_movement()
        Entity.update_entities(fps)

        player.screen_bound() # Test Methode
        
        player.apply_movement(fps)
        Render.render_blocks(Chunk.loaded_chunks, screen)
        screen.blit(player.gfx, player.pos)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        fontrenderer.draw_string(str(player.pos), (0,0), (0,0,0), size = 20, antialiased = True)

        pygame.display.update()
        clock.tick(fps)
