import random
from ..weapons import Shotgun, ReboungGun, RocketLauncher

class WeaponPool(object):

    pool = []

    @classmethod
    def reset_pool(cls, player):
        cls.pool = [Shotgun(player), RocketLauncher(player), ReboungGun(player)]
        cls.number = random.randint(0, len(cls.pool) - 1)

    @classmethod
    def random_weapon(cls):
        cls.number = random.randint(0, len(cls.pool) - 1)
        return cls.pool[cls.number]

    @classmethod
    def set_enemy_weapon(cls, enemy):

        match cls.number:
            case 0:
                return Shotgun(enemy)
            case 1:
                return RocketLauncher(enemy)
            case 2:
                return ReboungGun(enemy)

