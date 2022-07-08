from typing import Union
from heroes import Superman, SuperHero, Strelka, BasicHero
from places import Kostroma, Tokyo, Exoplanet, Place
from media import TV, Radio, Newspapers


def save_the_place(hero: BasicHero, place: Place, news_media: Union[list, tuple]):
    hero.find(place)
    hero.attack()
    hero.ultimate()
    for cnm in news_media:
        cnm.create_news(hero, place)


if __name__ == '__main__':
    tv = TV()
    radio = Radio()
    newspapers = Newspapers()

    save_the_place(Superman(), Kostroma(), (tv, ))
    print('-' * 20)
    save_the_place(SuperHero('Chack Norris', False), Tokyo(), (tv, radio))

    print('-' * 20)
    save_the_place(Strelka(), Exoplanet(), [newspapers, tv, radio])
