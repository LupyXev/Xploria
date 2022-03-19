from general_utils import Coords
from pygame import Surface
class Entity:
    #this class is a basic class, its goal is to be used as inheritance
    entities_loaded = set() #to update entities (ex: for gravity) ex: {EntityObj0x051561, EntityObj0x56118}

    @classmethod
    def update_entities(cls, fps):
        for entity in cls.entities_loaded:
            if entity.collision_on:
                entity._update_with_gravity(fps)
                entity.chunk = entity.chunk.get_chunk(entity.coords)

    def __init__(self, chunk, coords:Coords, base_speed, base_jump_height, base_jump_count, texture:Surface, collision_on=True, gravity_sensitive=True, load=True):
        self.coords = coords
        self.chunk = chunk
        
        self.collision_on = collision_on
        self.gravity_sensitive = gravity_sensitive
        self.velocity = [0, 0] #(x_block, y_block)
        
        self.BASE_SPEED = base_speed
        self.BASE_JUMP_HEIGHT = base_jump_height
        self.BASE_JUMP_COUNT = base_jump_count 
        self.speed = base_speed # can be modified (ex:buff/nerf)
        self.jump_height = base_jump_height # can be modified (ex:buff/nerf)
        self.is_jumping = False # jumping state to disable flying issues
        self.jump_count = base_jump_count # prototype
        
        self.texture = texture
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        
        self.gravity = 0.981 #Modifying this value will affect gravity's resistance
        self.on_ground = None

        if load:
            self.load()
    
    def _update_with_gravity(self, fps):
        if not self.on_ground:
            self.velocity[1] += self.gravity * 1/fps
        
        if self.velocity == [0, 0]:
            return
        
        wanted_coords = Coords([self.coords.x_block_coord + self.velocity[0], self.coords.block_coords[1] + self.velocity[1]], Coords.BLOCK_TYPE, self.coords.collide_box)
        collided, final_coords, vel_multiplier = self.chunk.get_collision(
            initial_coords=self.coords,
            wanted_coords=wanted_coords,
        )
        if collided:
            self.velocity = [self.velocity[i]*vel_multiplier[i] for i in range(2)]
            if vel_multiplier[1] == 0:
                self.on_ground = True
            else:
                self.on_ground = False
        else:
            self.on_ground = False
        self.coords = final_coords

    def data(self):
        return {
            "x_pos": self.block_coords[0],
            "y_pos": self.block_coords[1],
            "width": self.width,
            "height": self.height
        } #collision and gravity sensitive not needed for saving bc the Entity type will provide it by default
    
    def load(self):
        self.loaded = True
        self.entities_loaded.add(self)

    def unload(self):
        #it unloads the entity
        self.loaded = False
        self.entities_loaded.remove(self)
    
    
    
    def reset_velocity(self):
        self.velocity = [0,0]