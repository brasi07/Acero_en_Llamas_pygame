from extras.settings import RESIZE_PLAYER
from tanks.enemies.enemy import Enemy

class WarTrain(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 2.5, x, y, RESIZE_PLAYER, RESIZE_PLAYER, "horizontal", tank_level="_boss2", elite=False)
