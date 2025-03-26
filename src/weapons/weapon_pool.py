import random
from ..weapons import Shotgun, ReboungGun, RocketLauncher, Weapon

class WeaponPool(object):

    pool = []

    @classmethod
    def reset_pool(cls, player):
        cls.pool = [Weapon(player), Shotgun(player), RocketLauncher(player), ReboungGun(player)]
        cls.number = random.randint(1, len(cls.pool) - 1)

    @classmethod
    def random_weapon(cls):
        cls.number = random.randint(1, len(cls.pool) - 1)
        return cls.pool[cls.number]

    @classmethod
    def set_enemy_weapon(cls, enemy):

        match cls.number:
            case 1:
                return Shotgun(enemy)
            case 2:
                return RocketLauncher(enemy)
            case 3:
                return ReboungGun(enemy)

    @classmethod
    def get_weapon(cls, num):
        return cls.pool[num]

    @classmethod
    def get_weapon_number(cls, player):
        i = 1
        while i < len(cls.pool):
            if player.arma is cls.pool[i]:
                return i
            i += 1

        return 0