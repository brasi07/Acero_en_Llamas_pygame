from .enemy import Enemy
from ...extras import RESIZE_PLAYER

class EnemyBrown(Enemy):
    def __init__(self, x, y, modo_patrulla, elite=False):
        super().__init__(3, 2, x, y, RESIZE_PLAYER, RESIZE_PLAYER, modo_patrulla, elite, tank_level="_brown")