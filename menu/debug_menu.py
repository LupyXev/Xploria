import pygame
from gui import Gui, FontRenderer



class DebugMenu(Gui):
    def __init__(self, clock, player):
        super().__init__("debug")
        self.player = player
        self.clock = clock
    
    def draw(self):
        fr = FontRenderer(self.display)
        player_pos_str = "x: " + str(int(self.player.pos[0])) + " y: " + str(int(self.player.pos[1]))
        fr.draw_string(player_pos_str, (0,0), (255,0,255), size = 20, antialiased = True)
        fr.draw_string("fps: "+str(int(self.clock.get_fps())), (0,20), (255,0,255), 20)
