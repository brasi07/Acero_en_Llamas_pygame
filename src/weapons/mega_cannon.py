import numpy as np
import pygame

from .bullets.plasma_beam import PlasmaBeam
from ..extras import RESIZE_PLAYER, TIME_FRAME, ResourceManager, COOLDOWN
from .weapon import Weapon
from .bullets import Bullet

class WeaponMegaCannon(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = None  # Guarda el tiempo de activacivación
        self.animacion = ResourceManager.load_animation("weapons_boss2.png", 128, 128, 11, RESIZE_PLAYER * 2, RESIZE_PLAYER * 2)
        self.imagen_canon_base = self.animacion[0]
        self.imagen_canon = self.imagen_canon_base
        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.activo = False
        self.cooldown = 6000
        self.atacando = False
        self.dirx, self.diry = 0,0

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, mundo, tank=None):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala = PlasmaBeam(self)
        mundo.add_bullet(bala)
        self.activo = True
        self.atacando = True

    def update_secundaria(self, tank, mundo):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= TIME_FRAME:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina


                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                # self.imagen_canon = self.imagen_canon_base

        self.atacando = False