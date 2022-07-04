from collections import namedtuple
from map import Map, CellState

import random as rd


class BasicEngine:
    def get_size(self):
        pass

    def turn(self, x, y) -> CellState:
        pass

    def check_win(self, x: int, y: int) -> (bool, str, tuple):
        """
        :return:
        win: bool
        paler_name: str
        """
        pass

    def think(self, func_cell_on_click=None) -> (int, int):
        pass


WinType = namedtuple('WinTypes', ['Win_X', "Win_O", "Draw", "Continue"])('X', 'O', 'D', 'C')


class Engine(BasicEngine):

    def __init__(self, x_size: int, y_size: int, win_line=5):
        self.Map = Map(x_size, y_size)
        self.x_size = x_size
        self.y_size = y_size
        self.win_line = win_line
        self.activ_player = "user"
        self.activ_symbol = CellState.X

    def get_map(self) -> Map:
        return self.Map

    def get_size(self) -> (int, int):
        return self.x_size, self.y_size

    def turn(self, x: int, y: int):
        if self.Map.is_cell_empty(x, y):
            s = self.activ_symbol
            self.Map.set_cell(x, y, s)
            self.__change_activ_player()
            return s
        return None

    def __change_activ_player(self):
        if self.activ_player == "user":
            self.activ_player = "bender"
            self.activ_symbol = CellState.O
        else:
            self.activ_player = "user"
            self.activ_symbol = CellState.X

    def check_win(self, x: int, y: int) -> (bool, str, tuple):
        if not self.Map.check_for_empty_cells():
            return WinType.Draw, None, None
        wt = WinType.Continue
        v = self.Map.get_cell(x, y)
        lines = self.Map.count_lines(x, y, v)
        # print(lines)
        for line in lines:
            if line[0] >= self.win_line:
                if v == CellState.X:
                    v = CellState.O
                    wt = WinType.Win_O
                else:
                    v = CellState.X
                    wt = WinType.Win_X
                return wt, v, line
        return wt, None, None

    def think(self, func_cell_on_click=None) -> (int, int):
        if self.Map.check_for_empty_cells():
            x = rd.randint(0, self.x_size)
            y = rd.randint(0, self.y_size)

            if x < 0 or x > self.x_size:
                print("X out of range", x)
            if y < 0 or y > self.y_size:
                print("Y out of range", y)

            while not self.Map.is_cell_empty(x, y):
                x = rd.randint(0, self.x_size)
                y = rd.randint(0, self.y_size)

            if func_cell_on_click is None:
                self.turn(x, y)
            else:
                func_cell_on_click(x, y, False)
            return x, y
