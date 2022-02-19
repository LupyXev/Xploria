from entity import Entity
import pygame

class Player(Entity): 
    TYPE_NAME = 'player'
    def __init__(self, x_pos, y_pos, baseSpeed, baseJumpHight):
        super().__init__(x_pos, y_pos, baseSpeed, baseJumpHight, pygame.image.load("assets/player.png").convert_alpha())
        self.keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE:0}

    def data(self):
        return {"data": super().data(), "type": self.TYPE_NAME}
    
    def InputMovement(self):
        if self.gravity < 5:
            self.gravity += 1
            
        y_mov = self.gravity # temporary
        
        self._CheckInputs()
        x_mov = ((self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed)

        self.velocity = [x_mov, y_mov]
            
    def ApplyMovement(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        self.resetVelocity()

    def ScreenBound(self):
        if self.pos[1] + self.velocity[1] + self.height > 720:
            self.velocity[1] = 0
            
        if self.pos[0] + self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.pos[0] + self.velocity[0] + self.width > 1280:
            self.velocity[0] = 0
        
    
    def _CheckInputs(self):
        inputs = pygame.key.get_pressed()
        for key in self.keys.keys():
            self.keys[key] = inputs[key]