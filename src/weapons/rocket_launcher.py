import pygame

from extras.resourcesmanager import ResourceManager
from extras.settings import RESIZE_PLAYER
from weapons import Weapon
from weapons.bullets.Rocket import Rocket


class RocketLauncher(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.sprites = ResourceManager.load_animation(f"weapons{tank.tank_level}_128x128.png", 128, 128, 16)
        self.imagen_canon_base = self.sprites[11]
        self.rocket_counter = 5

    def activar_secundaria(self, tank, mundo):
        if self.rocket_counter == 0:
            self.cooldown = 10000
            self.rocket_counter = 5
        else:
            self.cooldown = 200
            self.rocket_counter -= 1

        self.tiempo_inicio = pygame.time.get_ticks()
        rocket = Rocket(self.get_cannon_tip(), self.angulo_cannon, self.tank.colision_layer_balas)
        self.balas.append(rocket)

