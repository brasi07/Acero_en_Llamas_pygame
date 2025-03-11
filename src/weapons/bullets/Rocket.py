import math

import pygame

from extras.resourcesmanager import ResourceManager
from extras.settings import RESIZE_PLAYER
from weapons.bullets import Bullet


class Rocket(Bullet):
    def __init__(self, cannon_tip, angulo, tipo_colision):
        super().__init__(cannon_tip, angulo, tipo_colision)
        self.imagen = ResourceManager.load_and_scale_image("bala_cohete.png", RESIZE_PLAYER * 0.15, RESIZE_PLAYER * 0.3)
        self.imagen = pygame.transform.rotate(self.imagen, -angulo-90)
        self.rect = self.imagen.get_rect(center=self.rect_element.center)
        self.velocidad = 10
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad

