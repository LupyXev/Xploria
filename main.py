import pygame
from sys import exit
from player import Player
from chunk import Chunk
from blocks import *
from entity import Entity
from gui import FontRenderer
from render import Render
from general_utils import Coords

pygame.init()

WIDTH, HEIGHT = 1280, 720 #will be 40, 22.5 in IG coords
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

chunk = Chunk.get_chunk(Coords((0, 0), Coords.CHUNK_TYPE))
player = Player(chunk, Coords((10, 0), Coords.BLOCK_TYPE))
low_chunk = Chunk.get_chunk(Coords((0, 1), Coords.CHUNK_TYPE))
for i in range(16):
    low_chunk.add_obj(Dirt(Coords((i, 21), Coords.BLOCK_TYPE)))

fontrenderer = FontRenderer(screen)

if __name__ == "__main__":
    while True:
        screen.fill("white")
        player.input_movement(fps)
        Entity.update_entities(fps)

        Render.render_blocks(Chunk.loaded_chunks, screen)
        screen.blit(player.gfx, player.coords.pixel_coords)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        fontrenderer.draw_string(str(player.coords.pixel_coords), Coords((0, 0), Coords.PIXEL_TYPE), (0,0,0), size = 20, antialiased = True)

        fontrenderer.draw_string(str(player.velocity), Coords((0, 25), Coords.PIXEL_TYPE), (0,0,0), size = 20, antialiased = True)

        pygame.display.update()
        clock.tick(fps)
