class Actor:
    def __init__(self, map_handler, x, y):
        self._map_handler = map_handler
        self.__Position= {"x": x,"y": y}
        self.__Acted= False
    @property
    def position(self):
        return self.__Position
    @property
    def acted(self):
        return self.__Acted
    @acted.setter
    def acted(self, v: bool):
        self.__Acted = bool(v)
    def move(self, dir):
        dirs= {
            "up": (0,-1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        dx, dy = dirs[dir]
        tg_x = self.__Position["x"] + dx
        tg_y = self.__Position["y"] + dy
        if 0<=tg_x < self._map_handler.n and 0<=tg_x < self._map_handler.n:
            if self._map_handler.read_cell(tg_x,tg_y) is None:
                self._map_handler._map[self.__Position["y"]][self.__Position["x"]] = None
                self._map_handler._map[tg_y][tg_x] = self
                self.__Position = {"x": tg_x, "y" : tg_y}
                self.__Acted = True
    def attack(self, dir):
        dirs = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        dx, dy = dirs[dir]
        tg_x = self.__Position["x"] + dx
        tg_y = self.__Position["y"] + dy
        self.__Acted = True
        if 0<=tg_x < self._map_handler.n and 0<=tg_y < self._map_handler.n:
            tg = self._map_handler.read_cell(tg_x, tg_y)
            if isinstance(tg, Actor):
                target.die()
    def die(self):
        if 0 <= self.__Position["x"] < self._map_handler.n and 0 <= self.__Position["y"] < self._map_handler.n:
            if self._map_handler._map[self.__Position["x"]][self.__Position["y"]] is self:
                self._map_handler._map[self.__Position["x"]][self.__Position["y"]] = None
        self.__Position = {"x":-1, "y": -1}
        self.__Acted = False

class MapHandler:
    def __init__(self, size):
        if isinstance(size, int):
            if size <=0:
                raise ValueError("размерность должна быть > 0")
            self._n = size
        self._map = [[None for _ in range(n)] for _ in range(n)]
    @property
    def n(self):
        return self._n
    def read_cell(self, x, y):
        try:
            if x>=0 and y>=0:
                return self._map(x,y)
        except ValueError: "x и y не должны быть за пределом поля"

    def new_map(self, n):
        if n==-1:
            self._map= [[None for _ in range(self._n)] for _ in range(self._n)]
        elif n!=0:
            self._map = [[None for _ in range(n)] for _ in range(n)]
        else:
            raise ValueError("размерность нового поля не должна быть 0")

    def create_actor(self, x: int, y: int):
        actor = Actor(x,y)
        self._map[y][x]=actor
        return actor