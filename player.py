from entity import Entity
import pygame

class Player(Entity): 
    TYPE_NAME = 'player'
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, 3, 3, 1, pygame.image.load("assets/player.png").convert_alpha())
        self.keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE:0}

    def data(self):
        return {"data": super().data(), "type": self.TYPE_NAME}
    
    def input_movement(self):        
        self._check_inputs()
        y_mov = 0
        
        x_mov = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed
        #if self.is_jumping is False:      
        y_mov = -1 * max(self.keys[pygame.K_UP], self.keys[pygame.K_SPACE]) * self.jump_height
        #    self.is_jumping = True
            
        print(y_mov)
        
        self.velocity[0] += x_mov
        self.velocity[1] += y_mov
        
    
    def apply_movement(self, fps):
        self.velocity[1] += self.gravity * 1/fps
        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
        self.velocity[0] = 0

    def screen_bound(self):
        if self.pos[1] + self.velocity[1] + self.height > 720:
            self.velocity[1] = 0
            
        if self.pos[0] + self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.pos[0] + self.velocity[0] + self.width > 1280:
            self.velocity[0] = 0
        
    
    def _check_inputs(self):
        inputs = pygame.key.get_pressed()
        for key in self.keys.keys():
            self.keys[key] = inputs[key]