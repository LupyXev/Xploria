from entity import Entity

class Player(Entity): 
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)