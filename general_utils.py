class Coords:
    PIXEL_TYPE = 0
    BLOCK_TYPE = 1
    CHUNK_TYPE = 2

    BLOCK_SIZE = 32
    CHUNK_SIZE = 16

    def _get_coords_as_block_coords(self, coords, type):
        #conversion bc we always store coords as block coords
        if type == self.PIXEL_TYPE:
            return [c/self.BLOCK_SIZE for c in coords]
        elif type == self.BLOCK_TYPE:
            return coords
        elif type == self.CHUNK_TYPE:
            return [c*self.CHUNK_SIZE for c in coords]    
        else:
            raise ValueError("Coords type error")

    def __init__(self, coords:tuple or list, type):
        self.original_type = type
        self._coords = self._get_coords_as_block_coords(coords, type)

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
    def chunk_coords(self):
        return [c/self.CHUNK_SIZE for c in self._coords]
    
    @property
    def chunk_coords_rounded(self):
        return [c//self.CHUNK_SIZE for c in self._coords]
    

    def set_coords(self, coords:tuple or list, coords_type):
        self._coords = self._get_coords_as_block_coords(coords, coords_type)
    
    def set_x(self, x, type):
        self._coords = [self._get_coords_as_block_coords([x], type)[0], self._coords[1]]
    
    def set_y(self, y, type):
        self._coords = [self._coords[0], self._get_coords_as_block_coords([y], type)[0]]
    