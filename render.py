import pygame
from chunk import Chunk
from blocks import *

class Render:
    scrolling = [0,0]
    
    @classmethod
    def render_blocks(self,loaded_chunks,screen):
        '''function which handle graphics on the display'''
        chunks = [chunk for chunk in loaded_chunks.values()] 
        for chunk in chunks :
            for object in chunk.objects.values():
                screen.blit(object.surface, (object.coords.pixel_coords[0] - self.scrolling[0], object.coords.pixel_coords[1]-self.scrolling[1]))
                #screen.set_at(object.coords.pixel_coords, (255, 255, 0))
    @classmethod
    def render_player(self, player, screen):
        screen.blit(player.texture, (player.coords.pixel_coords[0]-self.scrolling[0], player.coords.pixel_coords[1]-self.scrolling[1]))

    @classmethod
    def calculate_scrolling(self, player, screen):
        SCREEN_SIZE = screen.get_size()
        self.scrolling[0] += (player.coords.pixel_coords[0] - self.scrolling[0]-SCREEN_SIZE[0]//2)//5
        self.scrolling[1] += (player.coords.pixel_coords[1] - self.scrolling[1] - SCREEN_SIZE[1]//2)//10