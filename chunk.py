from os.path import exists
from entity import Entity
from player import Player
from json import load, dump

class Chunk:
    #allows to save and load chunks
    CHUNK_SIZE = 16
    loaded_chunks = {} #loaded chunks by pos (ex: {(x, y): ChunkObj0x14561})
    ENTITY_TYPE_TO_CLASS = {"player": Player}

    @classmethod
    def get_chunk(cls, chunk_x_pos, chunk_y_pos):
        if (chunk_x_pos, chunk_y_pos) in cls.loaded_chunks:
            return cls.loaded_chunks[(chunk_x_pos, chunk_y_pos)]
        else:
            return cls(chunk_x_pos, chunk_y_pos)

    def __init__(self, chunk_x_pos, chunk_y_pos):
        self.x_pos = chunk_x_pos
        self.y_pos = chunk_y_pos
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