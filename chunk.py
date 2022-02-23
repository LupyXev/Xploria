from os.path import exists
from json import load, dump
from player import Player
from blocks import *
from general_utils import Coords
from generation import Generator

class Chunk:
    #allows to save and load chunks
    CHUNK_SIZE = 16 #this is x and y size
    BLOCK_SIZE = 32
    loaded_chunks = {} #loaded chunks by pos (ex: {(x, y): ChunkObj0x14561})
    ENTITY_TYPE_TO_CLASS = {
        "player": Player,
        "dirt": Dirt
    }
    generator = Generator(8857610046016419003)

    @classmethod
    def get_chunk(cls, coords:Coords):
        chunk_coords = tuple(coords.chunk_coords_rounded)
        if chunk_coords in cls.loaded_chunks:
            return cls.loaded_chunks[chunk_coords]
        else:
            print("loading chunk", coords.chunk_coords_rounded)
            return cls(coords)
    
    @classmethod
    def get_collision(cls, initial_coords:Coords, future_coords:Coords, height, return_y_collision=False):
        chunk = cls.get_chunk(future_coords)
        y_collision = None
        for object in tuple(chunk.objects.values()): #in tuple to avoid problems when modifying objects
            if object.collision_on:
                if object.coords.block_coords[0] <= initial_coords.block_coords[0] <= object.coords.block_coords[0] + object.width / cls.BLOCK_SIZE:
                    #in x collide box
                    if initial_coords.block_coords[1] + height / cls.BLOCK_SIZE <= object.coords.block_coords[1] <= future_coords.block_coords[1] + height / cls.BLOCK_SIZE:
                        #will cross collide box, from higher to lower
                        if not return_y_collision: return True
                        elif y_collision is None or y_collision > object.coords.block_coords[1] + object.height / cls.BLOCK_SIZE: # > bc the coords y starts from the upper screen part to the lower
                            y_collision = object.coords.block_coords[1] - height / cls.BLOCK_SIZE
                    
                    elif initial_coords.block_coords[1] >= object.coords.block_coords[1] <= future_coords.block_coords[1] + height / cls.BLOCK_SIZE:
                        #will cross collide box, from lower to higher
                        if not return_y_collision: return True
                        elif y_collision is None or y_collision < object.coords.block_coords[1] + object.height / cls.BLOCK_SIZE: # < bc the coords y starts from the lower screen part to the upper
                            y_collision = object.coords.block_coords[1] + object.height / cls.BLOCK_SIZE

        if not return_y_collision: return False

        if return_y_collision: return y_collision

    def __init__(self, coords:Coords):
        self.coords = coords
        self.objects = {} #by position in the map tuple ex:{(2, 3): Obj0x13256156}
        chunk_x_pos, chunk_y_pos = coords.chunk_coords_rounded

        #--- LOADING CHUNCK ---
        if exists(f"save/map/{chunk_x_pos} {chunk_y_pos}.json"):
            with open(f"save/map/{chunk_x_pos} {chunk_y_pos}.json", "r") as f:
                json_data = load(f)
            for game_type_objs in json_data.values():
                for obj_json in game_type_objs:
                    entity_coords = Coords((obj_json["data"].pop("x_pos"), obj_json["data"].pop("y_pos")), Coords.BLOCK_TYPE)
                    entity_obj = self.ENTITY_TYPE_TO_CLASS[obj_json["type"]](entity_coords, **obj_json["data"]) #inits the entity
                    self.objects[tuple(entity_obj.coords.block_coords)] = entity_obj
        else:
            #generating new chunk
            block_list = self.generator.generate_chunk(*coords.chunk_coords_rounded)
            for in_chunk_y in range(len(block_list)):
                for in_chunk_x in range(len(block_list[in_chunk_y])):
                    value = block_list[in_chunk_y][in_chunk_x]
                    if value == 1:
                        self.add_obj(Dirt(Coords((self.coords.block_coords[0] + in_chunk_x, self.coords.block_coords[1] + in_chunk_y), Coords.BLOCK_TYPE)))
                    if value == 2:
                        self.add_obj(GrassyDirt(Coords((self.coords.block_coords[0] + in_chunk_x, self.coords.block_coords[1] + in_chunk_y), Coords.BLOCK_TYPE)))
        
        self.loaded_chunks[(chunk_x_pos, chunk_y_pos)] = self

    def add_obj(self, object):
        self.objects[(object.coords.block_coords)] = object
    
    def save(self):
        json_data = {
            "entities": [],
            "blocks": []
        }
        for object in self.objects.values():
            json_data[object.GAME_TYPE].append(object.data())
        with open(f"save/map/{self.coords.chunk_coords_rounded[0]} {self.coords.chunk_coords_rounded[1]}.json", "w") as f:
            dump(json_data, f)
    
    def unload(self):
        print("unloading chunk", self.coords.chunk_coords_rounded)
        #self.save()
        self.loaded_chunks.pop(self.coords.chunk_coords_rounded)