from ex_01 import CyclicIterator
from ex_02 import Movie
from datetime import datetime

class Range2:
    def __init__(self, stop_value: int):
        self.current = -1
        self.stop_value = stop_value - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop_value:
            self.current += 1
            return self.current
        raise StopIteration


def test_ex_01():
    print('TEST ex_01:')
    print('--== range(3) ==--')
    n = 10
    cyclic_iterator = CyclicIterator(range(3))
    for i in cyclic_iterator:
        print(i)
        n -= 1
        if n <= 0:
            break

    print('--== list ==--')
    n = 10
    ll = [1, 2, 3, 4]
    cyclic_iterator = CyclicIterator(ll)
    for i in cyclic_iterator:
        print(i)
        n -= 1
        if n <= 0:
            break

    print('--== set ==--')
    n = 10
    s = {1, 2, 3, 4}
    cyclic_iterator = CyclicIterator(s)
    for i in cyclic_iterator:
        print(i)
        n -= 1
        if n <= 0:
            break

    print('--== dict ==--')
    n = 10
    d = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
    cyclic_iterator = CyclicIterator(d.items())
    for i in cyclic_iterator:
        print(i)
        n -= 1
        if n <= 0:
            break

    print('--== Range2 ==--')
    n = 20
    cyclic_iterator = CyclicIterator(Range2(14))
    for i in cyclic_iterator:
        print(i)
        n -= 1
        if n <= 0:
            break


def test_ex_02():
    print('\nTEST ex_01:')
    m = Movie('sw', [
        (datetime(2020, 3, 25), datetime(2020, 4, 7)),
        (datetime(2020, 1, 2), datetime(2020, 1, 8)),
        (datetime(2020, 1, 7), datetime(2020, 1, 1)),
        (datetime(2020, 3, 25), datetime(2020, 4, 7))
    ])

    for d in m.schedule():
        print(d)


if __name__ == "__main__":
    test_ex_01()
    test_ex_02()