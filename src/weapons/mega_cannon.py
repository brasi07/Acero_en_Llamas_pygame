import numpy as np
import pygame

from .bullets.plasma_beam import PlasmaBeam
from ..extras import RESIZE_PLAYER, TIME_FRAME, ResourceManager, COOLDOWN
from .weapon import Weapon

class WeaponMegaCannon(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = None  # Guarda el tiempo de activacivación
        self.animacion = ResourceManager.load_animation("weapons_boss2.png", 128, 128, 11, RESIZE_PLAYER * 2, RESIZE_PLAYER * 2)
        self.imagen_canon_base = self.animacion[0]
        self.imagen_canon = self.imagen_canon_base
        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.activo = False
        self.cooldown = 5000
        self.dirx, self.diry = 0,0

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, mundo, tank=None):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala = PlasmaBeam(self)
        mundo.add_bullet(bala)
        self.activo = True

    def update(self, mundo, tank=None):
        # Calcular la dirección del cañón
        if not self.activo:
            self.dirx, self.diry = self.tank.calcular_direccion_canon(mundo, tank)
        
            # Calcular el ángulo del cañón
            self.angulo_cannon = np.degrees(np.arctan2(self.diry, self.dirx))  # Guardar el ángulo para disparos
            self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, -self.angulo_cannon - 90)
            self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)

    def update_secundaria(self, tank, mundo):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= 200:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina


                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                # self.imagen_canon = self.imagen_canon_base