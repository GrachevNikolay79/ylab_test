from abc import abstractmethod
from typing import Any, final


class BasicNews:
    @abstractmethod
    def _create_news(self, hero, place) -> str:
        pass

    @final
    def create_news(self, hero, place):
        print(self._create_news(hero, place))


class TV(BasicNews):

    def _create_news(self, hero, place):
        return f'TV showed: {hero} saved the {place}!'


class Radio(BasicNews):

    def _create_news(self, hero, place):
        return f'Radio stations talked about: {hero} saved the {place}!'


class Newspapers(BasicNews):

    def _create_news(self, hero, place):
        return f'All the newspapers wrote about: {hero} saved the {place}!'