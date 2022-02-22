from entity import Entity
import pygame
from general_utils import Coords

class Player(Entity): 
    TYPE_NAME = 'player'
    def __init__(self, chunk, coords:Coords):
        super().__init__(chunk, coords, 10, 20, 1, pygame.image.load("assets/player.png").convert_alpha())
        self.keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE:0}
        self.air_x_resistance = 8
        self.chunk_load_distance = 1 #a chunks radius

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
    
    def update_loaded_chunks(self):
        player_chunk_x, player_chunk_y = self.chunk.coords.chunk_coords_rounded
        min_x_chunk, max_x_chunk = player_chunk_x - self.chunk_load_distance, player_chunk_x + self.chunk_load_distance
        min_y_chunk, max_y_chunk = player_chunk_y - self.chunk_load_distance, player_chunk_y + self.chunk_load_distance
        #unload chunks
        for chunk_coords, chunk in tuple(self.chunk.loaded_chunks.items()): #converting in tuple bc this dict will be modified
            if chunk_coords[0] < min_x_chunk or chunk_coords[0] > max_x_chunk:
                chunk.unload()
            elif chunk_coords[1] < min_y_chunk or chunk_coords[1] > max_y_chunk:
                print(chunk_coords)
                chunk.unload()

        #load chunks
        for x_chunk in range(min_x_chunk, max_x_chunk + 1):
            for y_chunk in range(min_y_chunk, max_y_chunk + 1):
                self.chunk.get_chunk(Coords((x_chunk, y_chunk), Coords.CHUNK_TYPE)) #will load the chunk if it is not loaded
