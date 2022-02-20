import pygame
from chunk import Chunk
from blocks import *

class Render:
    @classmethod
    def render_blocks(self,loaded_chunks,screen):
        '''function which handle graphics on the display'''
        chunks = [chunk for chunk in loaded_chunks.values()] 
        for chunk in chunks :
            for object in chunk.objects.items():
                screen.blit(object[1].surface, object[0])
                pygame.display.update()
