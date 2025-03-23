from src.tanks import Player
from src.weapons import WeaponPool


class Partida:

    def __init__(self, vida, arma, objetos_clave, mundo):
        self.player = Player(vida, objetos_clave)
        WeaponPool().reset_pool(self.player)