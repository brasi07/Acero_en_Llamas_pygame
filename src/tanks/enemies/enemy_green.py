from tanks.enemies.enemy import Enemy
from extras.settings import RESIZE_PLAYER

class EnemyGreen(Enemy):
    def __init__(self, x, y, modo_patrulla):
        super().__init__(5, 2, x, y, RESIZE_PLAYER, RESIZE_PLAYER, tank_level="_green")