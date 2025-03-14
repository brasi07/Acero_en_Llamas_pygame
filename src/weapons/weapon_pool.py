import random

from ..singleton import SingletonMeta
from ..weapons import Dash, MineLauncher, Shotgun, ReboungGun, RocketLauncher

class WeaponPool(metaclass=SingletonMeta):

    def __init__(self):
        from ..tanks import Player
        self.pool = [Dash(Player()), Shotgun(Player()), RocketLauncher(Player()), ReboungGun(Player()), MineLauncher(Player())]
        self.number = random.randint(0, len(self.pool) - 1)

    def random_weapon(self):
        self.number = random.randint(0, len(self.pool) - 1)
        return self.pool[self.number]

    def set_enemy_weapon(self, enemy):

        match self.number:
            case 0:
                return Dash(enemy)
            case 1:
                return Shotgun(enemy)
            case 2:
                return RocketLauncher(enemy)
            case 3:
                return ReboungGun(enemy)
            case 4:
                return MineLauncher(enemy)
