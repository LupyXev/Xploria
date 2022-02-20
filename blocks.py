from pygame import image, Rect

tileset = image.load("assets/nature_tileset.png")
class Block:
    #this class is a basic class, its goal is to be used as inheritance
    SIZE = 32
    width = SIZE
    height = SIZE
    TEXTURES = {} #will be ovewrited in sub classes
    GAME_TYPE = "blocks"
    def __init__(self, x_pos, y_pos, texture_name:str):
        self.collision_on = True
        self.pos = (x_pos, y_pos)
        self.texture_name = texture_name
    
    @property
    def get_surface(self):
        return self.TEXTURES[self.texture_name]
    
    def data(self):
        return {
            "x_pos": self.pos[0],
            "y_pos": self.pos[1],
            "texture_name": self.texture_name
        }
    
class Dirt(Block):
    TEXTURES = {
        "dirt": tileset.subsurface(Rect(32, 32, 16, 16))
    }
    TYPE_NAME = "dirt"

    def __init__(self, x_pos, y_pos, texture_name:str="dirt"):
        super().__init__(x_pos, y_pos, texture_name)

    def data(self):
        return {"data": super().data(), "type": self.TYPE_NAME}


class GrassyDirt(Block):
    TEXTURES = {
        "up_left_corner": None,
        "down_left_corner": None,
        "up_right_corner": None,
        "down_right_corner": None,
        "up_edge": None
    }