import pygame
from gui import Gui, FontRenderer
from general_utils import Coords


class DebugMenu(Gui):
    def __init__(self, clock, player):
        super().__init__("debug")
        self.player = player
        self.clock = clock
    
    def draw(self):
        fr = FontRenderer(self.display)
        player_pos_str = "x: " + str(int(self.player.coords.pixel_coords[0])) + " y: " + str(int(self.player.coords.pixel_coords[1]))
        fr.draw_string(player_pos_str, Coords((0,0), Coords.PIXEL_TYPE), (255,0,255), size = 20, antialiased = True)
        fr.draw_string(f"Vel: {self.player.velocity}", Coords((0, 20), Coords.PIXEL_TYPE), (255,0,255), 20)
        fr.draw_string("fps: "+str(int(self.clock.get_fps())), Coords((0, 40), Coords.PIXEL_TYPE), (255,0,255), 20)
