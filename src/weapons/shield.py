import pygame
from ..extras import ResourceManager, RESIZE_PLAYER
from .weapon import Weapon

class Shield(Weapon):
    def __init__(self, tank, posicion=None):
        super().__init__(tank, posicion)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.imagenes_accesorio_base = ResourceManager.load_and_scale_image("escudo.png", RESIZE_PLAYER, RESIZE_PLAYER)
        self.imagen_escudo_roto = ResourceManager.load_and_scale_image("escudo_roto.png", RESIZE_PLAYER, RESIZE_PLAYER)
        self.imagen_accesorio = self.imagenes_accesorio_base
        self.under_weapon = False
        self.proteger = True
        self.vida_owner = self.tank.vida_inicial
        self.cooldown = 10000

    def activar_secundaria(self, mundo, tank=None):
        self.imagen_accesorio = self.imagenes_accesorio_base
        self.proteger = True

    def update_secundaria(self, tank, mundo):
        if self.tank.vida < self.vida_owner and self.proteger:
            self.tank.vida = self.tank.vida + 1
            self.proteger = False
            self.imagen_accesorio = self.imagen_escudo_roto
        self.vida_owner = self.tank.vida

    def get_pickable_image(self):
        return self.imagenes_accesorio_base

