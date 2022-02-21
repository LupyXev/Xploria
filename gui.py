import pygame

class FontRenderer:
    #this class is used to render string on the screen 
    def __init__(self, screen, font = pygame.font.get_default_font()):
        self.display = screen #the diplay surface
        self.font = font #the font to render (can be change)
    
    def draw_string(self,string:str, pos:tuple, color:tuple, size:int=10, antialiased:bool=True):

        #create a new font object with the right size and font
        self.font_object = pygame.font.Font(self.font, size)

        #create a surface with the right argument
        text_surface = self.font_object.render(string, antialiased, color)
        #create a rectangle with the position given in argument
        text_rect = text_surface.get_rect(topleft = pos)
        #draw on the screen the surcafe at the right coordinate
        self.display.blit(text_surface, text_rect)

class Gui:
    def __init__(self,name:str, backround:pygame.Surface = None):
        self.toggled = False
        self.display = pygame.display.get_surface()
        self.name = name
        self.backround = backround
    
    def toggle_gui(self):
        self.toggled = not self.toggled
    
class GuiManager:
    def __init__(self) -> None:
        self.all_gui = dict()
        self.list_event = dict()

    def add_gui(self,gui:Gui):
        if type(gui) != type(gui):
            raise ValueError("gui must be a Gui object")

        self.all_gui[gui.name] = gui
    
    def draw_gui(self):
        for gui in self.all_gui.keys():
            if self.all_gui[gui].toggled:
                self.all_gui[gui].draw()
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.all_gui["debug"].toggle_gui()
    
