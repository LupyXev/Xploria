from perlin_noise import PerlinNoise


class Generator:
#creat and manage map generation
    def __init__(self, seed):
        """ Need a seed to initialize"""
        self.chunk_size = 16
        self.noise = PerlinNoise(octaves=1, seed = seed)

    def generate_chunk(self, chunk_x:int, chunk_y:int):
        '''generate a chunk based on chunk position
        take 2 int for the position of the chunk 
        return a nested list of block in the chunk'''

        block_list = [[0 for x in range(self.chunk_size)] for y in range(self.chunk_size)] #create a blank chunk

        for local_y in range(self.chunk_size):
            for local_x in range(self.chunk_size): #loop for all the local positions in the chunk
                world_x = chunk_x * self.chunk_size + local_x
                world_y = chunk_y * self.chunk_size + local_y # determin the world position of a block in the chunk

                #generation specifique shenanigans

                amplitude = 30
                frequencies = .03
                base_height = 10
                
                #calculate for each block in the chunk the height of the y position block with perlin_noise
                point_height = int(
                    self.noise(world_x*frequencies)*amplitude)+base_height
                
                #test if the block tested is below the block height
                if world_y > point_height:
                    block_list[local_y][local_x] = 1
                
        return block_list

'''
#just for testing
testgenerator = Generation(seed = 8857610046016419003)
'''