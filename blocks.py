from pygame import image, Rect, transform
from general_utils import Coords

tileset = image.load("assets/nature_tileset.png")
class Block:
    #this class is a basic class, its goal is to be used as inheritance
    SIZE = 32
    width = SIZE
    height = SIZE
    TEXTURES = {} #will be ovewrited in sub classes
    GAME_TYPE = "blocks"
    def __init__(self, coords:Coords, texture_name:str):
        self.collision_on = True
        self.coords = coords
        self.texture_name = texture_name
    
    @property
    def surface(self):
        return self.TEXTURES[self.texture_name]
    
    def data(self):
        return {
            "x_pos": self.coords.x_block_coords,
            "y_pos": self.coords.y_block_coords,
            "texture_name": self.texture_name
        }
    
class Dirt(Block):
    TEXTURES = {
        "dirt": transform.scale(tileset.subsurface(Rect(16, 0, 16, 16)), (Block.SIZE, Block.SIZE))
    }
    TYPE_NAME = "dirt"

    def __init__(self, coords:Coords, texture_name:str="dirt"):
        super().__init__(coords, texture_name)

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