import random as rd
from collections import namedtuple


class OutOfBounds(Exception):
    pass


class InvalidValue(Exception):
    pass


CellState = namedtuple('CellState', ['EMPTY', "X", "O"])(' ', 'X', 'O')


class Map:

    def __init__(self, x_size: int, y_size: int):
        self.x_size = x_size
        self.y_size = y_size
        self.map = [CellState.EMPTY for _ in range(x_size * y_size)]

    def print_map(self):
        for y in range(self.y_size):
            print(self.map[y * self.x_size: (y + 1) * self.x_size])

    def get_cell(self, x: int, y: int) -> str:
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        return self.map[y * self.x_size + x]

    def set_cell(self, x: int, y: int, val: str, check_win=False):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        if val not in CellState:
            raise InvalidValue
        self.map[y * self.x_size + x] = val

    def is_cell_empty(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            return False
        return self.get_cell(x, y) == CellState.EMPTY

    def get_size(self) -> (int, int):
        return self.x_size, self.y_size

    def get_count_empty_cell(self) -> int:
        return len([1 for i in self.map if i == CellState.EMPTY])

    def check_for_empty_cells(self) -> bool:
        for i in self.map:
            if i == CellState.EMPTY:
                return True
        return False

    def count_lines(self, x: int, y: int, v=None) -> (str, bool):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        result_check_h = self.count_line_h(x, y, v)
        result_check_v = self.count_line_v(x, y, v)
        result_check_dm = self.count_line_dm(x, y, v)
        result_check_dn = self.count_line_dn(x, y, v)
        return result_check_h, result_check_v, result_check_dm, result_check_dn

    def count_line_v(self, x: int, y: int, v=None) -> (int, int, int, int, int):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds

        original_pos = y * self.x_size + x
        if v is None:
            v = self.map[original_pos]
        count = 1

        p = original_pos - self.x_size
        y1 = y - 1
        while y1 >= 0 and v == self.map[p]:
            count += 1
            p -= self.x_size
            y1 -= 1
        y1 += 1

        p = original_pos + self.x_size
        y2 = y + 1
        while y2 < self.y_size and v == self.map[p]:
            p += self.x_size
            y2 += 1
            count += 1
        y2 -= 1

        return count, x, y1, x, y2

    def count_line_h(self, x: int, y: int, v=None) -> (int, int, int, int, int):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        original_pos = y * self.x_size + x
        if v is None:
            v = self.map[original_pos]

        count = 1
        p = original_pos - 1
        x1 = x - 1
        while x1 >= 0 and v == self.map[p]:
            p -= 1
            x1 -= 1
            count += 1
        x1 += 1

        p = original_pos + 1
        x2 = x + 1
        while x2 < self.x_size and v == self.map[p]:
            p += 1
            x2 += 1
            count += 1
        x2 -= 1

        return count, x1, y, x2, y

    def count_line_dm(self, x: int, y: int, v=None) -> (int, int, int, int, int):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        delta = self.x_size + 1
        original_pos = y * self.x_size + x
        if v is None:
            v = self.map[original_pos]
        count = 1

        p = original_pos - delta
        y1 = y - 1
        x1 = x - 1
        while y1 >= 0 and x1 >= 0 and v == self.map[p]:
            p -= delta
            y1 -= 1
            x1 -= 1
            count += 1
        x1 += 1
        y1 += 1

        p = original_pos + delta
        y2 = y + 1
        x2 = x + 1
        while y2 < self.y_size and x2 < self.x_size and v == self.map[p]:
            p += delta
            y2 += 1
            x2 += 1
            count += 1
        x2 -= 1
        y2 -= 1

        return count, x1, y1, x2, y2

    def count_line_dn(self, x: int, y: int, v=None) -> (int, int, int, int, int):
        if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
            raise OutOfBounds
        delta = self.x_size - 1
        original_pos = y * self.x_size + x
        if v is None:
            v = self.map[original_pos]

        count = 1
        p = original_pos - delta
        y1 = y - 1
        x1 = x + 1
        while y1 >= 0 and x1 < self.x_size and v == self.map[p]:
            p -= delta
            y1 -= 1
            x1 += 1
            count += 1
        y1 += 1
        x1 -= 1

        p = original_pos + delta
        y2 = y + 1
        x2 = x - 1
        while y2 < self.y_size and x2 >= 0 and v == self.map[p]:
            p += delta
            y2 += 1
            x2 -= 1
            count += 1
        y2 -= 1
        x2 += 1

        return count, x1, y1, x2, y2

    def get_random_empty_cell(self) -> (int, int):
        empty_list = tuple(i for i, v in enumerate(self.map) if v == CellState.EMPTY)
        list_len = len(empty_list)
        if list_len == 0:
            return None, None
        elif list_len == 1:
            idx = empty_list[0]
        else:
            n = rd.randint(0, list_len - 1)
            idx = empty_list[n]
        y = idx // self.x_size
        x = idx % self.x_size
        return x, y
