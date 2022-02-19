from pygame import image, Rect

tileset = image.load("assets/nature_tileset.png")
class Block:
    #this class is a basic class, its goal is to be used as inheritance
    SIZE = 32
    TEXTURES = {} #will be ovewrited in sub classes
    GAME_TYPE = "blocks"
    def __init__(self, pos:tuple, texture_name:str):
        self.pos = tuple(pos)
        self.texture_name = texture_name
    
    @property
    def get_surface(self):
        return self.TEXTURES[self.texture_name]
    
    def data(self):
        return {
            "x_pos": self.pos[0],
            "y_pos": self.pos[1],
            "texture": self.texture_name
        }
    
class Dirt(Block):
    TEXTURES = {
        "dirt": tileset.subsurface(Rect(32, 32, 16, 16))
    }
    TYPE_NAME = "dirt"

    def __init__(self, pos:tuple, texture_name:str="dirt"):
        super().__init__(pos, texture_name)

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