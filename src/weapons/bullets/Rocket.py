import math

import pygame

from ...extras.resourcesmanager import ResourceManager
from ...extras.settings import RESIZE_PLAYER
from .bullet import Bullet


class Rocket(Bullet):
    def __init__(self, arma, desplazamiento_lateral):
        super().__init__(arma, desplazamiento_lateral=desplazamiento_lateral)
        self.imagen = ResourceManager.load_and_scale_image("bala_cohete.png", RESIZE_PLAYER * 0.15, RESIZE_PLAYER * 0.3)
        self.imagen = pygame.transform.rotate(self.imagen, -arma.angulo_cannon-90)
        self.rect = self.imagen.get_rect(center=self.rect_element.center)
        self.velocidad = 10
        self.vel_x = math.cos(self.angle_rad) * self.velocidad
        self.vel_y = math.sin(self.angle_rad) * self.velocidad

