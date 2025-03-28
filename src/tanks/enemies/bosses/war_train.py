import pygame

from ....extras import Settings, ResourceManager
from ..enemy import Enemy
from ....weapons import Shotgun, RocketLauncher, ReboungGun
from ....weapons.bullets import Rocket


class WarTrain(Enemy):
    def __init__(self, x, y):
        super().__init__(100, 2.5, x, y, Settings.RESIZE_PLAYER, Settings.RESIZE_PLAYER, "horizontal", tank_level="_boss3", elite=False)
        self.imagen = ResourceManager.load_and_scale_image("body_boss3.png",Settings.RESIZE_PLAYER*14, Settings.RESIZE_PLAYER*2)
        self.rect_element = self.imagen.get_rect(topleft=(x, y))
        self.rect_element.y = y + Settings.TILE_SIZE/2
        self.mask = pygame.mask.from_surface(self.imagen)
        self.muerto = False
        self.armas = [Shotgun(self, (-370*Settings.RESOLUTION_SCALE, 0)),
                      RocketLauncher(self, (-270*Settings.RESOLUTION_SCALE, 0)),
                      ReboungGun(self, (0, 0)),
                      Shotgun(self, (100*Settings.RESOLUTION_SCALE, 0)),
                      RocketLauncher(self, (350*Settings.RESOLUTION_SCALE, 0)),
                      ReboungGun(self, (420*Settings.RESOLUTION_SCALE, 0)),
                      Shotgun(self, (470*Settings.RESOLUTION_SCALE, 0))
                      ]
        self.tiempos_ultimo_disparo = [0,0,0,0,0,0,0]

        for i in range(5):
            self.armas[i].imagen_canon_base = pygame.transform.scale(self.armas[i].imagen_canon_base, (Settings.TILE_SIZE*3, Settings.TILE_SIZE*3))
            self.armas[i].imagen_canon = pygame.transform.scale(self.armas[i].imagen_canon,(Settings.TILE_SIZE * 3, Settings.TILE_SIZE * 3))

        self.colision_layer_balas = Settings.CollisionLayer.BULLET_ENEMY
        self.attack_range = 3000
        self.in_screen = False

    def update(self, jugador, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(Settings.EVENTO_BOSS_MUERTO))
            jugador.vida = jugador.vida_inicial
            self.eliminar = True

        if not self.in_screen and self.en_la_misma_pantalla(jugador):
            ResourceManager.load_and_play_wav("boss_battle_loop.wav", -1)
            self.in_screen =  True

        if self.rect_element.x <= Settings.ANCHO * 3:
            self.rect_element.x += 2
        else:
            self.rect_element.x = -self.imagen.get_width()

        self.mask = pygame.mask.from_surface(self.imagen)

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]
        start = ((self.rect_element.centerx // Settings.TILE_SIZE) % 32, (self.rect_element.centery // Settings.TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // Settings.TILE_SIZE) % 32, (jugador.rect_element.centery // Settings.TILE_SIZE) % 18)

        for arma in self.armas:
            arma.update(mundo, jugador)
            arma.update_secundaria(jugador, mundo)

        distancia = self.distancia_jugador(jugador)
        if distancia < self.attack_range:
            self.manejar_ataque(mundo, pantalla_binaria, start, goal)

    def manejar_ataque(self, mundo, pantalla_binaria, start, goal):
        for i, arma in enumerate(self.armas):  # Obtener el índice y el arma
            if self.in_screen and arma.cooldown and pygame.time.get_ticks() - self.tiempos_ultimo_disparo[i] >= arma.cooldown:
                arma.activar_secundaria(mundo)
                self.tiempos_ultimo_disparo[i] = pygame.time.get_ticks()

    def en_la_misma_pantalla(self, jugador):
        return (jugador.rect_element.y // self.TILE_SIZE // 18 == self.indice_mundo_y)

    def patrullar(self):
        pass

    def calcular_direccion_canon(self, mundo, jugador, arma):
        # Obtener la posición del ratón en relación con la cámara
        dirx = jugador.rect_element.centerx - arma.x
        diry = jugador.rect_element.centery - arma.y

        return dirx, diry

    def dibujar_enemigo(self, pantalla, x, y):
        self.dibujar(pantalla, x, y)
        for arma in self.armas:
            arma.dibujar_arma(pantalla, x, y)