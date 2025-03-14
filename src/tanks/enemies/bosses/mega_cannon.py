import pygame
from ....extras.settings import RESIZE_PLAYER
from ..enemy import Enemy
from ....weapons.mega_cannon import WeaponMegaCannon

class MegaCannon(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 0, x, y, RESIZE_PLAYER, RESIZE_PLAYER, "torreta", tank_level="_boss2", elite=False)
        self.muerto = False
        self.arma = WeaponMegaCannon

    def update(self, jugador, mundo):
        if self.vida <= 0:
            self.muerto = True
            self.vida = 20

        self.arma.update_secundaria(self, mundo)

    def gestionar_armas(self, mundo):
        if pygame.mouse.get_pressed()[1]:
            self.usar_arma_especial(mundo)