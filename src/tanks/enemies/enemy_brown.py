from tanks.enemies.enemy import Enemy
from extras.settings import RESIZE_PLAYER

class EnemyBrown(Enemy):
    def __init__(self, x, y, modo_patrulla):
        super().__init__(3, 2, x, y, RESIZE_PLAYER, RESIZE_PLAYER, tank_level="_brown", modo_patrulla=modo_patrulla)