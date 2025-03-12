import numpy as np
import pygame

from extras.settings import RESIZE_PLAYER, COOLDOWN
from weapons.bullets.bullet import Bullet
from extras.resourcesmanager import ResourceManager

class Weapon:
    def __init__(self, tank):
        self.tank = tank
        self.imagen_canon_base = ResourceManager.cargar_canon(0, "weapons", tank.tank_level)
        self.imagenes_accesorio_base = None
        self.imagen_bala = ResourceManager.load_and_scale_image("bala_base.png", RESIZE_PLAYER * 0.07, RESIZE_PLAYER * 0.07)

        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.rect_accesorio = None

        self.cooldown = COOLDOWN

        self.angulo_cannon = 0
        self.balas = []

    def activar(self):
        nueva_bala = Bullet(self)
        self.balas.append(nueva_bala)

    def update(self, mundo, tank=None):
        # Calcular la dirección del cañón
        dirx, diry = self.tank.calcular_direccion_canon(mundo, tank)
        
        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diry, dirx))  # Guardar el ángulo para disparos

        self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, -self.angulo_cannon - 90)
        self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)

        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def cambio_de_arma(self):
        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

    def dibujar_balas(self, pantalla, x, y):
        for bala in self.balas:
            bala.draw(pantalla, x, y)

    def dibujar_arma(self, pantalla, x, y):
        if self.imagen_accesorio: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            pantalla.blit(self.imagen_accesorio, (self.tank.rect_element.centerx - self.rect_accesorio.width // 2 - x, self.tank.rect_element.centery - self.tank.rect_element.height // 2 - y))

        pantalla.blit(self.imagen_canon, (self.tank.rect_element.centerx - self.rect_canon.width // 2 - x, self.tank.rect_element.centery - self.rect_canon.height // 2 - y))

    def dibujar_minas(self,mundo):
        pass

    def activar_secundaria(self, tank, mundo):
        pass

    def update_secundaria(self, tank, mundo):
        pass

    def get_pickable_image(self):
        return self.imagen_canon_base










