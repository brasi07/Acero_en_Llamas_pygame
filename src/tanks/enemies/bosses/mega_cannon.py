import pygame

from ..astar import raycasting
from ....extras import RESIZE_PLAYER, TILE_SIZE, ResourceManager, EVENTO_BOSS_MUERTO, CollisionLayer
from ..enemy import Enemy
from ....weapons import WeaponMegaCannon

class MegaCannon(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 0, x, y, RESIZE_PLAYER, RESIZE_PLAYER, "torreta", tank_level="_boss2", elite=False)
        self.imagen = ResourceManager.load_and_scale_image("body_boss2.png", RESIZE_PLAYER*2, RESIZE_PLAYER*2)
        self.rect_element = self.imagen.get_rect(topleft=(self.x-TILE_SIZE/2, self.y-TILE_SIZE/3))
        self.mask = pygame.mask.from_surface(self.imagen)
        self.muerto = False
        self.arma = WeaponMegaCannon(self)
        self.colision_layer_balas = CollisionLayer.BULLET_BOSS2
        self.attack_range = 450


    def update(self, jugador, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(EVENTO_BOSS_MUERTO))
            jugador.vida = jugador.vida_inicial
            self.eliminar = True

        if not self.en_la_misma_pantalla(jugador):
            return

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]
        start = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // TILE_SIZE) % 32, (jugador.rect_element.centery // TILE_SIZE) % 18)

        self.arma.update(mundo, jugador)
        self.arma.update_secundaria(jugador, mundo)
        distancia = self.distancia_jugador(jugador)
        if distancia < self.attack_range:
            self.manejar_ataque(mundo, pantalla_binaria, start, goal)

    def manejar_ataque(self, mundo, pantalla_binaria, start, goal):
       if self.arma.cooldown and pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= self.arma.cooldown:
            self.arma.activar_secundaria(mundo)
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()
