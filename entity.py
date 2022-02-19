class Entity:
    #this class is a basic class, its goal is to be used as inheritance
    entities_loaded = set() #to update entities (ex: for gravity) ex: {EntityObj0x051561, EntityObj0x56118}
    def __init__(self, x_pos, y_pos, base_speed, base_jump_height, base_jump_count, gfx, collision_on=True, gravity_sensitive=True, load=True):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.pos = [x_pos, y_pos]
        
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
    def get_pos(self):
        self.pos = [self.x_pos, self.y_pos]
        return self.pos
    
    @property
    def set_pos(self, pos:tuple or list):
        self.pos = list(pos)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        
    @property
    def set_x(self, x_pos):
        self.x_pos = x_pos
        self.pos = [x_pos, self.pos[1]]
        
    @property
    def set_y(self, y_pos):
        self.x_pos = y_pos
        self.pos = [self.pos[0], y_pos]
    
    def reset_velocity(self):
        self.velocity = [0,0]