from abc import ABC, abstractmethod


class Place(ABC):
    @abstractmethod
    def get_antagonist(self):
        pass


class Kostroma(Place):
    city_name = 'Kostroma'

    @staticmethod
    def __get_orcs():
        print('Orcs hid in the forest')

    def get_antagonist(self):
        return self.__get_orcs()


class Tokyo(Place):
    name = 'Tokyo'

    @staticmethod
    def __get_godzilla():
        print('Godzilla stands near a skyscraper')

    def get_antagonist(self):
        return self.__get_godzilla()
