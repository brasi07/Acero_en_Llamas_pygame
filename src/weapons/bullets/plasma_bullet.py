import math

from extras.resourcesmanager import ResourceManager
from extras.settings import RESIZE_PLAYER
from weapons.bullets import Bullet


class PlasmaBullet(Bullet):
    def __init__(self, cannon_tip, angulo, tipo_colision):
        super().__init__(cannon_tip, angulo, tipo_colision)
        self.imagen = ResourceManager.load_and_scale_image("bala_plasma.png", RESIZE_PLAYER * 0.2, RESIZE_PLAYER * 0.2)
        self.angulo = math.radians(angulo)
        self.velocidad = 10
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad
        self.dano = 2
