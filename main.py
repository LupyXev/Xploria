import pygame
from sys import exit
from player import Player
from chunk import Chunk
from blocks import *
from entity import Entity
from gui import FontRenderer, GuiManager
from render import Render
from general_utils import Coords
from menu.debug_menu import DebugMenu

pygame.init()

WIDTH, HEIGHT = 1280, 720 #will be 40, 22.5 in IG coords
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

chunk = Chunk.get_chunk(Coords((0, 0), Coords.CHUNK_TYPE))
player = Player(chunk, Coords((10, 0), Coords.BLOCK_TYPE))

fontrenderer = FontRenderer(screen)
gui_manager = GuiManager()
debug = DebugMenu(clock,player)

gui_manager.add_gui(debug)

if __name__ == "__main__":
    while True:
        screen.fill("white")
        player.input_movement(fps)
        Entity.update_entities(fps)
        player.update_loaded_chunks()

        Render.render_blocks(Chunk.loaded_chunks, screen)
        screen.blit(player.gfx, player.coords.pixel_coords)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            gui_manager.event_handler(event)
        
        
        gui_manager.draw_gui()
        
        pygame.display.update()
        clock.tick(fps)
