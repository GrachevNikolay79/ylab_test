class CyclicIterator:
    def __init__(self, container):
        self.container = list(container)

    def __iter__(self):
        self.itr = iter(self.container)
        return self

    def __next__(self):
        try:
            return next(self.itr)
        except StopIteration:
            self.itr = iter(self.container)
            return next(self.itr)

