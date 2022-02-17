from entity import Entity

class Player(Entity): 
    TYPE_NAME = 'player'
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)
    
    def data(self):
        return {"data": super().data(), "type": self.TYPE_NAME}