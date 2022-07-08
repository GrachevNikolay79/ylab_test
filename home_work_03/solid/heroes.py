from typing import final

from mixin import GunMixin, KickMixin, LasersMixin


class BasicHero:
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack

    @staticmethod
    def find(place):
        print(place.get_antagonist())

    def _attack(self):
        pass

    def _ultimate(self):
        pass

    @final
    def attack(self):
        self._attack()

    @final
    def ultimate(self):
        if self.can_use_ultimate_attack:
            self._ultimate()

    def __repr__(self):
        return self.name


# просто супергерой, порождение темного гения голливуда
class SuperHero(BasicHero, GunMixin):

    def __init__(self, name, can_use_ultimate_attack=True):
        super(SuperHero, self).__init__(name, can_use_ultimate_attack)

    def _attack(self):
        self._fire_a_gun()


# супермен в красных труселях поверх лосин
class Superman(BasicHero, KickMixin, LasersMixin):

    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def _attack(self):
        self._roundhouse_kick()

    def _ultimate(self):
        self._incinerate_with_lasers()


# Стрелка без белки
class Strelka(BasicHero, KickMixin):

    def __init__(self):
        super(Strelka, self).__init__('Strelka', False)

    def _attack(self):
        self._roundhouse_kick()
