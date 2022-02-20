import pygame

class FontRenderer:
    #this class is used to render string on the screen 
    def __init__(self, screen, font = pygame.font.get_default_font()):
        self.display = screen #the diplay surface
        self.font = font #the font to render (can be change)
    
    def draw_string(self,string:str, pos:tuple, color:tuple, size:int=10, antialiased:bool=False):

        self.font_object = pygame.font.Font(self.font, size)
        text_surface = self.font_object.render(string, antialiased, color)

        text_rect = text_surface.get_rect(topleft = pos)
        self.display.blit(text_surface, text_rect)