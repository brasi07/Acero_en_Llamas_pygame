import pygame

from ..astar import raycasting
from ....extras import Settings, ResourceManager
from ..enemy import Enemy
from ....weapons import WeaponMegaCannon

class MegaCannon(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 0, x, y, Settings.RESIZE_PLAYER, Settings.RESIZE_PLAYER, "torreta", tank_level="_boss2", elite=False)
        self.imagen = ResourceManager.load_and_scale_image("body_boss2.png", Settings.RESIZE_PLAYER*2, Settings.RESIZE_PLAYER*2)
        self.rect_element = self.imagen.get_rect(topleft=(self.x-Settings.TILE_SIZE/2, self.y-Settings.TILE_SIZE/3))
        self.mask = pygame.mask.from_surface(self.imagen)
        self.muerto = False
        self.arma = WeaponMegaCannon(self)
        self.colision_layer_balas = Settings.CollisionLayer.BULLET_BOSS2
        self.attack_range = Settings.TILE_SIZE*20
        self.in_screen = False
        self.inicioBattle = False

    def update(self, jugador, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(Settings.EVENTO_BOSS_MUERTO))
            jugador.vida = jugador.vida_inicial
            self.eliminar = True

        if not self.en_la_misma_pantalla(jugador):
            if self.in_screen:
                ResourceManager.stop_and_unload_wav("boss_battle_loop.wav")
                self.in_screen = False
            return

        if not self.in_screen:
            ResourceManager.load_and_play_wav("boss_battle_loop.wav", -1)
            self.in_screen =  True

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]
        start = ((self.rect_element.centerx // Settings.TILE_SIZE) % 32, (self.rect_element.centery // Settings.TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // Settings.TILE_SIZE) % 32, (jugador.rect_element.centery // Settings.TILE_SIZE) % 18)

        self.arma.update(mundo, jugador)
        self.arma.update_secundaria(jugador, mundo)
        if jugador.rect_element.centery < (self.fila_pantalla+1) * Settings.ALTO:
            self.manejar_ataque(mundo, pantalla_binaria, start, goal)

    def manejar_ataque(self, mundo, pantalla_binaria, start, goal):
       if self.arma.cooldown and pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= self.arma.cooldown:
            self.arma.activar_secundaria(mundo)
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()
