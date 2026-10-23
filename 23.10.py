class Actor:
    def __init__(self, map_handler, x: int, y: int):
        self._map_handler = map_handler
        self.__Position = {"x": x, "y": y}
        self.__Acted = False

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
        dirs = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dx, dy = dirs[dir]
        tg_x = self.__Position["x"] + dx
        tg_y = self.__Position["y"] + dy

        if 0 <= tg_x < self._map_handler.n and 0 <= tg_y < self._map_handler.n:
            if self._map_handler.read_cell(tg_x, tg_y) is None:
                self._map_handler._map[self.__Position["y"]][self.__Position["x"]] = None
                self._map_handler._map[tg_y][tg_x] = self
                self.__Position = {"x": tg_x, "y": tg_y}
                self.__Acted = True

    

    def attack(self, dir):
        dirs = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dx, dy = dirs[dir]
        tg_x = self.__Position["x"] + dx
        tg_y = self.__Position["y"] + dy

        self.__Acted = True
        if 0 <= tg_x < self._map_handler.n and 0 <= tg_y < self._map_handler.n:
            tg = self._map_handler.read_cell(tg_x, tg_y)
            if isinstance(tg, Actor):
                tg.die()

    def die(self):
        cur_x = self.__Position["x"]
        cur_y = self.__Position["y"]
        if 0 <= cur_x < self._map_handler.n and 0 <= cur_y < self._map_handler.n:
            if self._map_handler._map[cur_y][cur_x] is self:
                self._map_handler._map[cur_y][cur_x] = None
        self.__Position = {"x": -1, "y": -1}
        self.__Acted = False


class MapHandler:
    def __init__(self, size: int):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Размерность должна быть целым числом > 0")
        self._n = size
        self._map = [[None for _ in range(size)] for _ in range(size)]

    @property
    def n(self):
        return self._n

    def read_cell(self, x: int, y: int):
        if 0 <= x < self._n and 0 <= y < self._n:
            return self._map[y][x]
        return None

    def create_actor(self, x: int, y: int):
        if not (0 <= x < self._n and 0 <= y < self._n):
            raise IndexError("Координаты спавна вне пределов карты")
        if self._map[y][x] is not None:
            raise ValueError("Клетка уже занята")
        actor = Actor(self, x, y)
        self._map[y][x] = actor
        return actor

    def new_map(self, n: int):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Размерность нового поля должна быть целым числом > 0")
        for y in range(self._n):
            for x in range(self._n):
                cell_item = self._map[y][x]
                if isinstance(cell_item, Actor):
                    cell_item.die()
        self._n = n
        self._map = [[None for _ in range(n)] for _ in range(n)]
