from pygame import Rect
class CollideBox:
    BLOCK_SIZE = 32
    def __init__(self, block_width, block_height):
        self._width = block_width #in blocks
        self._height = block_height #in blocks
    
    @property
    def width(self): #blocks
        return self._width
    
    @property
    def height(self): #blocks
        return self._height
    
    @property
    def pixel_width(self):
        return self._width * self.BLOCK_SIZE
    
    @property
    def pixel_height(self):
        return self._height * self.BLOCK_SIZE

class Coords:
    PIXEL_TYPE = 0
    BLOCK_TYPE = 1
    CHUNK_TYPE = 2

    BLOCK_SIZE = 32
    CHUNK_SIZE = 16

    def _get_coords_as_block_coords(self, coords:tuple or list, type):
        #conversion bc we always store coords as block coords
        if type == self.PIXEL_TYPE:
            return [c/self.BLOCK_SIZE for c in coords]
        elif type == self.BLOCK_TYPE:
            return coords
        elif type == self.CHUNK_TYPE:
            return [c*self.CHUNK_SIZE for c in coords]    
        else:
            raise ValueError("Coords type error", coords)

    def __init__(self, coords:tuple or list, type, collide_box:CollideBox=None):
        self.original_type = type
        self._coords = self._get_coords_as_block_coords(coords, type)
        self._collide_box = collide_box
    
    @property
    def collide_box(self):
        return self._collide_box
    
    @collide_box.setter
    def collide_box(self, collide_box):
        self._collide_box = collide_box

    @property
    def pixel_coords(self):
        return [c*self.BLOCK_SIZE for c in self._coords]
    
    @property
    def block_coords(self):
        return self._coords
    
    @property
    def x_block_coord(self):
        return self._coords[0]
    @property
    def y_block_coord(self):
        return self._coords[1]
    
    @property
    def x_pixel_coord(self):
        return self._coords[0] * self.BLOCK_SIZE
    @property
    def y_pixel_coord(self):
        return self._coords[1] * self.BLOCK_SIZE

    @property
    def chunk_coords(self):
        return [c/self.CHUNK_SIZE for c in self._coords]
    
    @property
    def chunk_coords_rounded(self):
        return tuple([int(c//self.CHUNK_SIZE) for c in self._coords])
    
    @property
    def bottom_right_block_coords(self):
        if self._collide_box is None:
            raise ValueError("bottom_right_block_coords method called but there is no collide_box (=None) for this obj")
        return (self._coords[0] + self._collide_box.width, self._coords[1] + self._collide_box.height)

    def set_coords(self, coords:tuple or list, coords_type):
        self._coords = self._get_coords_as_block_coords(coords, coords_type)
    
    def set_x(self, x, type):
        self._coords = [self._get_coords_as_block_coords([x], type)[0], self._coords[1]]
    
    def set_y(self, y, type):
        self._coords = [self._coords[0], self._get_coords_as_block_coords([y], type)[0]]    
    
    def mouvement_coords(self, destination):
        #destination is a Coords obj
        return Coords((destination.x_block_coord - self.x_block_coord, destination.y_block_coord - self.y_block_coord), self.BLOCK_TYPE) #xDest - xSelf ; yDest - ySelf