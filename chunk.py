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
        "dirt": Dirt,
        "grassy_dirt": GrassyDirt
    }
    generator = Generator(8857610046016419000)

    @classmethod
    def get_chunk(cls, coords:Coords):
        chunk_coords = tuple(coords.chunk_coords_rounded)
        if chunk_coords in cls.loaded_chunks:
            return cls.loaded_chunks[chunk_coords]
        else:
            #print("loading chunk", coords.chunk_coords_rounded)
            return cls(coords)
    
    @classmethod
    def get_collision(cls, initial_coords:Coords, wanted_coords:Coords):
        final_coords = wanted_coords
        collided = False
        velocity_multiplier = [1, 1]
        
        ini_chunk = cls.get_chunk(initial_coords)
        final_chunk = cls.get_chunk(final_coords)
        final_bottom_right_coords = Coords(final_coords.bottom_right_block_coords, Coords.BLOCK_TYPE)
        
        chunks = [final_chunk]
        if final_chunk is not ini_chunk:
            chunks.append(ini_chunk)
        if final_bottom_right_coords.chunk_coords_rounded not in (ini_chunk.coords.chunk_coords_rounded, final_chunk.coords.chunk_coords_rounded):
            #the bottom right coords chunk not in chunks
            chunks.append(cls.get_chunk(final_bottom_right_coords))

        if len(chunks) > 1:
            print(initial_coords.block_coords)
        for chunk in chunks:
            for obj in tuple(chunk.objects.values()):
                if obj.collision_on:
                    x_distance_left = final_coords.x_block_coord + final_coords.collide_box.width - obj.coords.x_block_coord
                    x_distance_right = obj.coords.x_block_coord + obj.coords.collide_box.width - final_coords.x_block_coord
                    
                    if x_distance_left >= 0 and x_distance_right >= 0:
                        #the final coords and its collide box is "inside" the x obj coords
                        y_distance_top = final_coords.y_block_coord + final_coords.collide_box.height - obj.coords.y_block_coord
                        y_distance_bottom = obj.coords.y_block_coord + obj.coords.collide_box.height - final_coords.y_block_coord

                        if y_distance_top >= 0 and y_distance_bottom >= 0:
                            #there is collision
                            collided = True
                            #we will set final coords to the face with the lower distance (can be x or y, left/right, top/bottom)
                            if min(x_distance_left, x_distance_right) < min(y_distance_top, y_distance_bottom):
                                #we will set x on final coords
                                if x_distance_left <= x_distance_right:
                                    #we set to left
                                    final_coords.set_x(obj.coords.x_block_coord - final_coords.collide_box.width, final_coords.BLOCK_TYPE)
                                    velocity_multiplier[0] = 0
                                else:
                                    #we set to right
                                    final_coords.set_x(obj.coords.x_block_coord + obj.coords.collide_box.width, final_coords.BLOCK_TYPE)
                                    velocity_multiplier[0] = 0
                            else:
                                #we will set y on final coords
                                if y_distance_top <= y_distance_bottom:
                                    #we set to top
                                    final_coords.set_y(obj.coords.y_block_coord - final_coords.collide_box.height, final_coords.BLOCK_TYPE)
                                    velocity_multiplier[1] = 0
                                else:
                                    #we set to bottom
                                    final_coords.set_y(obj.coords.y_block_coord + obj.coords.collide_box.height, final_coords.BLOCK_TYPE)
                                    velocity_multiplier[1] = -1
                                
        return collided, final_coords, velocity_multiplier

    def __init__(self, coords:Coords):
        self.coords = Coords(coords.chunk_coords_rounded, Coords.CHUNK_TYPE)
        self.objects = {} #by position in the map tuple ex:{(2, 3): Obj0x13256156}
        chunk_x_pos, chunk_y_pos = coords.chunk_coords_rounded

        #--- LOADING CHUNCK ---
        if exists(f"save/map/{chunk_x_pos} {chunk_y_pos}.json"):
            with open(f"save/map/{chunk_x_pos} {chunk_y_pos}.json", "r") as f:
                json_data = load(f)
            for game_type_objs in json_data.values():
                for obj_json in game_type_objs:
                    entity_coords = Coords((obj_json["data"].pop("x_pos"), obj_json["data"].pop("y_pos")), Coords.BLOCK_TYPE) #without the collide box (will be initialized with the obj)
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
        #print("unloading chunk", self.coords.chunk_coords_rounded)
        #self.save()
        self.loaded_chunks.pop(self.coords.chunk_coords_rounded)