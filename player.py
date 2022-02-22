from entity import Entity
import pygame
from general_utils import Coords

class Player(Entity): 
    TYPE_NAME = 'player'
    def __init__(self, chunk, coords:Coords):
        super().__init__(chunk, coords, 10, 20, 1, pygame.image.load("assets/player.png").convert_alpha())
        self.keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE:0}
        self.air_x_resistance = 8

    def data(self):
        return {"data": super().data(), "type": self.TYPE_NAME}
    
    def input_movement(self, fps):        
        self._check_inputs()
        if self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT] == 0: #no input movement on x
            if abs(self.velocity[0]) < 0.003: #no velocity
                self.velocity[0] = 0
            self.velocity[0] *= 1 - 1/((1/self.air_x_resistance) * fps)
        else:
            self.velocity[0] = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed / 100
        
        if self.on_ground:
            self.velocity[1] += -1 * max(self.keys[pygame.K_UP], self.keys[pygame.K_SPACE]) * self.jump_height * 1/fps
            self.on_ground = False
    
    def _check_inputs(self):
        inputs = pygame.key.get_pressed()
        for key in self.keys.keys():
            self.keys[key] = inputs[key]