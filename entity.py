class Entity:
    #this class is a basic class, its goal is to be used as inheritance
    entities_loaded = set() #to update entities (ex: for gravity) ex: {EntityObj0x051561, EntityObj0x56118}
    def __init__(self, x_pos, y_pos, width, height, collision_on=True, gravity_sensitive=True, load=True):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.pos = (x_pos, y_pos)
        self.width = width
        self.height = height
        self.collision_on = collision_on
        self.gravity_sensitive = gravity_sensitive
        self.velocity = (0, 0) #(x, y)

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