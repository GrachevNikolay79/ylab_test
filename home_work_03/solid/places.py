from abc import ABC, abstractmethod
from typing import Union


class Place(ABC):
    _name = ''

    def __init__(self, name: Union[str, list]):
        self._name = name

    @abstractmethod
    def get_antagonist(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def __repr__(self):
        return self.get_name()


class Kostroma(Place):

    def __init__(self):
        super(Kostroma, self).__init__('Kostroma')

    def get_antagonist(self) -> str:
        return 'Orcs hid in the forest'

    def get_name(self) -> str:
        return self._name


class Tokyo(Place):

    def __init__(self):
        super(Tokyo, self).__init__('Tokyo')

    def get_antagonist(self) -> str:
        return 'Godzilla stands near a skyscraper'

    def get_name(self) -> str:
        return self._name


class Exoplanet(Place):

    def __init__(self):
        super(Exoplanet, self).__init__([34566.23455, 95483.56455, 1234.33452])

    def get_antagonist(self) -> str:
        return 'Aliens hiding in asteroids'

    def get_name(self) -> str:
        return 'Exoplanet at '+str(self._name)

