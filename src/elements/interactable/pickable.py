from abc import ABC

import pygame

from .interactable import Interactable
from ...extras.settings import CollisionLayer


class Pickable(ABC, Interactable):

    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, CollisionLayer.INTERACTUABLE)
        #poner los sprites del pickable

class PickableWeapon(Pickable):

    def __init__(self, x, y, weapon):
        self.weapon = weapon
        super().__init__(x, y, weapon.get_pickable_image())
        self.direccion = 1  # 1 para bajar, -1 para subir
        self.velocidad = 5  # Cuántos píxeles se mueve en cada actualización
        self.limite_superior = self.y - 50  # Límite superior del movimiento
        self.limite_inferior = self.y + 50  # Límite inferior del movimiento
        self.ultimo_movimiento = pygame.time.get_ticks()  # Guarda el tiempo


    def interactuar(self, objeto):
        from ...tanks import Player
        if isinstance(objeto, Player) and self.check_collision(objeto):
            self.eliminar = True
            objeto.cambiar_secundaria(self.weapon)

    def update(self, jugador):
        tiempo_actual = pygame.time.get_ticks()

        # Solo actualizar cada 100 ms
        if tiempo_actual - self.ultimo_movimiento >= 100:
            self.ultimo_movimiento = tiempo_actual  # Resetear el tiempo

            # Mover en la dirección actual
            self.y += self.velocidad * self.direccion

            # Cambiar de dirección si alcanza un límite
            if self.y >= self.limite_inferior:
                self.direccion = -1  # Empieza a subir
            elif self.y <= self.limite_superior:
                self.direccion = 1  # Empieza a bajar