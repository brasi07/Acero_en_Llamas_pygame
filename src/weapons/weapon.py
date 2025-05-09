import math

import numpy as np
import pygame
from ..extras import Settings, ResourceManager
from .bullets import Bullet

class Weapon:
    def __init__(self, tank, posicion=None):
        self.tank = tank
        self.desplazamientox, self.desplazamientoy = 0,0

        if posicion:
            self.desplazamientox, self.desplazamientoy = posicion

        self.x, self.y = self.desplazamientox + tank.rect_element.centerx, self.desplazamientoy + tank.rect_element.centery

        self.imagen_canon_base = ResourceManager.cargar_canon(0, "weapons", tank.tank_level)
        self.imagenes_accesorio_base = None
        self.imagen_bala = ResourceManager.load_and_scale_image("bala_base.png", Settings.RESIZE_PLAYER * 0.07, Settings.RESIZE_PLAYER * 0.07)

        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

        self.rect_canon = self.imagen_canon.get_rect(center=(self.x, self.y))
        self.rect_accesorio = None
        self.cooldown = Settings.COOLDOWN

        self.under_weapon = True
        self.angulo_cannon = 0

    def activar(self, mundo):
        ResourceManager.play_sound("normal_shot.wav", 0, 0.04)
        nueva_bala = Bullet(self)
        mundo.add_bullet(nueva_bala)

    def update(self, mundo, tank=None):
        self.x, self.y = self.desplazamientox + self.tank.rect_element.centerx, self.desplazamientoy + self.tank.rect_element.centery

        # Calcular la dirección del cañón
        dirx, diry = self.tank.calcular_direccion_canon(mundo, tank, self)
        
        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diry, dirx))  # Guardar el ángulo para disparos

        self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, -self.angulo_cannon - 90)
        self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)

    def get_cannon_tip(self, desplazamiento_lateral=0, desplazamiento_frontal=0):
        """Calcula la punta del cañón después de la rotación, permitiendo desplazamiento en ambos ejes."""

        cannon_length = self.rect_canon.height // 4  # Largo del cañón
        angle_rad = math.radians(self.angulo_cannon)

        # Desplazamiento en la dirección del cañón (frontal)
        x_offset = (cannon_length + desplazamiento_frontal) * np.cos(angle_rad)
        y_offset = (cannon_length + desplazamiento_frontal) * np.sin(angle_rad)

        # Desplazamiento lateral (perpendicular al cañón)
        x_lateral_offset = desplazamiento_lateral * np.cos(angle_rad + np.pi / 2)  # 90° perpendiculares
        y_lateral_offset = desplazamiento_lateral * np.sin(angle_rad + np.pi / 2)

        # Calcular posición final
        cannon_x = self.x + x_offset + x_lateral_offset
        cannon_y = self.y + y_offset + y_lateral_offset

        return cannon_x, cannon_y

    def cambio_de_arma(self):
        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

    def dibujar_arma(self, pantalla, x, y):
        if self.imagen_accesorio and self.under_weapon: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            pantalla.blit(self.imagen_accesorio, (self.x - self.rect_accesorio.width // 2 - x, self.y - self.tank.rect_element.height // 2 - y))

        pantalla.blit(self.imagen_canon, (self.x - self.rect_canon.width // 2 - x, self.y - self.rect_canon.height // 2 - y))

        if self.imagen_accesorio and not self.under_weapon: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            pantalla.blit(self.imagen_accesorio, (self.x - self.rect_accesorio.width // 2 - x, self.y - self.tank.rect_element.height // 2 - y))

    def dibujar_minas(self,mundo):
        pass

    def activar_secundaria(self, mundo, tank=None):
        pass

    def update_secundaria(self, tank, mundo):
        pass

    def get_pickable_image(self):
        return self.imagen_canon_base










