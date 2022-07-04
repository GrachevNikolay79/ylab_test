from collections import namedtuple
from map import Map, CellState

import random as rd


class BasicEngine:
    def get_size(self):
        pass

    def turn(self, x, y, v) -> CellState:
        pass

    def check_win(self, x: int, y: int) -> (str, str, tuple):
        """
        :return:
        win_type: str ('X', 'O', 'D', 'C')

        player_name: str
        
        line: tuple(len, x1, y1, x2, y2)
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
        # self.activ_player = "user"
        # self.activ_symbol = CellState.X

    def get_map(self) -> Map:
        return self.Map

    def get_size(self) -> (int, int):
        return self.x_size, self.y_size

    def turn(self, x: int, y: int, v: str = CellState.X):
        if self.Map.is_cell_empty(x, y):
            # v = self.activ_symbol
            self.Map.set_cell(x, y, v)
            # self.__change_activ_player()
            return v
        return None

    def check_win(self, x: int, y: int) -> (str, str, tuple):
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
        x, y = self.Map.get_random_empty_cell()
        # Добавим мозгов :), проверим не является ли ход по полученным координатам проигрышем,
        # если является, еще раз получим случайные координаты, но тут уже проверять не будем
        # т.е. ошибиться можно один раз за ход
        lines = self.Map.count_lines(x, y, CellState.O)
        for line in lines:
            if line[0] >= self.win_line:
                x, y = self.Map.get_random_empty_cell()
                break
        if x is not None:
            if func_cell_on_click is None:
                self.turn(x, y, CellState.O)
            else:
                func_cell_on_click(x, y, False)
        return x, y
