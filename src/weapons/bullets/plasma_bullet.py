import math
from ...extras import Settings, ResourceManager
from .bullet import Bullet

class PlasmaBullet(Bullet):
    def __init__(self, arma):
        super().__init__(arma)
        self.imagen = ResourceManager.load_and_scale_image("bala_plasma.png", Settings.RESIZE_PLAYER * 0.2, Settings.RESIZE_PLAYER * 0.2)
        self.velocidad = 10
        self.vel_x = math.cos(self.angle_rad) * self.velocidad
        self.vel_y = math.sin(self.angle_rad) * self.velocidad
        self.dano = 2
