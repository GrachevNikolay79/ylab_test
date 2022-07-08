class GunMixin:
    def fire_a_gun(self):
        print('PIU PIU')


class LasersMixin:
    def incinerate_with_lasers(self):
        print('Wzzzuuuup!')

class KickMixin:
    def roundhouse_kick(self):
        print('Bump')


class HeroBasic:
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack

    @staticmethod
    def find(place):
        place.get_antagonist()

    def attack(self):
        pass

    def ultimate(self):
        pass

    # Проблема: Герой не должен заниматься оповещениями о своей победе, это задача масс-медиа.
    # Несоблюден: Принцип единой ответственности.
    # По SOLID: Вынести оповещение в отдельный класс, занимающийся выводом информации.
    # Когда возникнут трудности? Добавьте оповещение о победе героя через газеты или через TV (на выбор)
    # а также попробуйте оповестить планеты (у которых вместа атрибута name:str используется coordinates:List[float]).
    def create_news(self, place):
        place_name = getattr(place, 'name', 'place')
        print(f'{self.name} saved the {place_name}!')


class SuperHero(HeroBasic, GunMixin):

    def __init__(self, name, can_use_ultimate_attack=True):
        super(SuperHero, self).__init__(name, can_use_ultimate_attack)

    def attack(self):
        self.fire_a_gun()


class Superman(HeroBasic, KickMixin, LasersMixin):

    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def attack(self):
        self.roundhouse_kick()

    def ultimate(self):
        self.incinerate_with_lasers()