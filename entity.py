class Entity:
    #this class is a basic class, its goal is to be used as inheritance
    entities_loaded = set() #to update entities (ex: for gravity) ex: {EntityObj0x051561, EntityObj0x56118}

    @classmethod
    def update_entities(cls, fps):
        for entity in cls.entities_loaded:
            if entity.collision_on:
                entity._update_with_gravity(fps)

    def __init__(self, chunk, x_pos, y_pos, base_speed, base_jump_height, base_jump_count, gfx, collision_on=True, gravity_sensitive=True, load=True):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._pos = [x_pos, y_pos]
        self.chunk = chunk
        
        self.collision_on = collision_on
        self.gravity_sensitive = gravity_sensitive
        self.velocity = [0, 0] #(x, y)
        
        self.BASE_SPEED = base_speed
        self.BASE_JUMP_HEIGHT = base_jump_height
        self.BASE_JUMP_COUNT = base_jump_count 
        self.speed = base_speed # can be modified (ex:buff/nerf)
        self.jump_height = base_jump_height # can be modified (ex:buff/nerf)
        self.is_jumping = False # jumping state to disable flying issues
        self.jump_count = base_jump_count # prototype
        
        self.gfx = gfx # (Coming soon) Entity texture
        self.rect = self.gfx.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        
        self.gravity = 9.81 #Modifying this value will affect gravity's resistance

        if load:
            self.load()
    
    def _update_with_gravity(self, fps):
        self.velocity[1] += self.gravity * 1/fps
        future_y_pos = self.pos[1] + self.velocity[1]
        y_upper_collision = self.chunk.get_collision(self.x_pos, future_y_pos, True)
        if y_upper_collision is not None:
            #will collide
            self.velocity[1] = 0 #bc when it touches the ground, velocity y must be 0
            self.y_pos = y_upper_collision #it is on ground

    def data(self):
        return {
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
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
    
    @property  
    def pos(self):
        self._pos = [self._x_pos, self._y_pos]
        return self._pos
    
    @pos.setter
    def pos(self, pos:tuple or list):
        self._pos = list(pos)
        self._x_pos = pos[0]
        self._y_pos = pos[1]
    
    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos):
        self._x_pos = x_pos
        self.pos = [x_pos, self.pos[1]]
    
    @property
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos):
        self._y_pos = y_pos
        self.pos = [self.pos[0], y_pos]
    
    def reset_velocity(self):
        self.velocity = [0,0]