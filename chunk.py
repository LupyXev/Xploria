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
        if (chunk_x_pos, chunk_y_pos) in loaded_chunks:
            return loaded_chunks[(chunk_x_pos, chunk_y_pos)]
        else:
            return cls.__init__(chunk_x_pos, chunk_y_pos)

    def __init__(self, chunk_x_pos, chunk_y_pos):
        self.x_pos = chunk_x_pos
        self.y_pos = chunk_y_pos
        self.objects = {} #by position in the map tuple ex:{(2, 3): Obj0x13256156}

        #--- LOADING CHUNCK ---
        if exists(f"map/{chunk_x_pos} {chunk_y_pos}.json"):
            with open(f"map/{chunk_x_pos} {chunk_y_pos}.json", "r") as f:
                json_data = load(f)
            for obj_json in json_data:
                entity_obj = self.ENTITY_TYPE_TO_CLASS[obj_json["type"]](**obj_json["data"]) #inits the entity
                self.objects[(entity_obj.pos)] = entity_obj

    def add_object(self, object):
        self.objects[(object.pos)] = object
    
    def save(self):
        json_data = []
        for object in self.objects.values():
            json_data.append(object.data())
        with open(f"map/{self.x_pos} {self.y_pos}.json", "w") as f:
            dump(json_data, f)