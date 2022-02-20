from os.path import exists
from json import load, dump
from player import Player
from blocks import *

class Chunk:
    #allows to save and load chunks
    CHUNK_SIZE = 16 #this is x and y size
    loaded_chunks = {} #loaded chunks by pos (ex: {(x, y): ChunkObj0x14561})
    ENTITY_TYPE_TO_CLASS = {
        "player": Player,
        "dirt": Dirt
    }

    @classmethod
    def get_chunk(cls, x_pos, y_pos):
        chunk_x_pos, chunk_y_pos = round(x_pos//16), round(y_pos//16)
        if (chunk_x_pos, chunk_y_pos) in cls.loaded_chunks:
            return cls.loaded_chunks[(chunk_x_pos, chunk_y_pos)]
        else:
            return cls(chunk_x_pos, chunk_y_pos)
    
    @classmethod
    def get_collision(cls, x, y, return_y_upper_collision=False):
        chunk = cls.get_chunk(x, y)
        y_upper_collision = None
        for object in tuple(chunk.objects.values()): #in tuple to avoid problems when modifying objects
            if object.collision_on:
                if object.pos[0] <= x <= object.pos[0] + object.width:
                    #in x collide box
                    if object.pos[1] <= y <= object.pos[1] + object.height:
                        #in collide box
                        if not return_y_upper_collision: return True
                        elif y_upper_collision is None or y_upper_collision > object.pos[1] + object.height: # > bc the coords y starts from the upper screen part to the lower
                            y_upper_collision = object.pos[1] + object.height
        
        if not return_y_upper_collision: return False

        if return_y_upper_collision: return y_upper_collision

    def __init__(self, chunk_x_pos, chunk_y_pos):
        self.chunk_x_pos = chunk_x_pos
        self.chunk_y_pos = chunk_y_pos
        self.objects = {} #by position in the map tuple ex:{(2, 3): Obj0x13256156}

        #--- LOADING CHUNCK ---
        if exists(f"save/map/{chunk_x_pos} {chunk_y_pos}.json"):
            with open(f"save/map/{chunk_x_pos} {chunk_y_pos}.json", "r") as f:
                json_data = load(f)
            for game_type_objs in json_data.values():
                for obj_json in game_type_objs:
                    entity_obj = self.ENTITY_TYPE_TO_CLASS[obj_json["type"]](**obj_json["data"]) #inits the entity
                    self.objects[(entity_obj.pos)] = entity_obj

    def add_obj(self, object):
        self.objects[(object.pos)] = object
    
    def save(self):
        json_data = {
            "entities": [],
            "blocks": []
        }
        for object in self.objects.values():
            json_data[object.GAME_TYPE].append(object.data())
        with open(f"save/map/{self.x_pos} {self.y_pos}.json", "w") as f:
            dump(json_data, f)