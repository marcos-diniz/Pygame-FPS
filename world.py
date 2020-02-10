#from objloader import *
from wavefrontloader import *

class World:
    def __init__(self):
        self.load_objects()

    def load_objects(self):
        self._wobjects = {"MAP_V2":WavefrontObject("wavefront_files/map_v2.obj")
        }

    def draw_objects(self):
        for lobject in self._wobjects.keys():
            self._wobjects[lobject].draw()

