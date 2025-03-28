import math
import time
from ...extras import Settings, ResourceManager
from .bullet import Bullet
import pygame


class ExplosionBullet(Bullet):
    """
    Bala que explota inmediatamente en la posición del tanque,
    haciendo daño en un área circular (radio) a todos los elementos
    dentro de dicho rango, incluido el propio tanque.
    No tiene arma asociada.
    """

    def __init__(self, weapon, tank, world,radio_explosion=Settings.BOMB_SIZE, dano=1):
        super().__init__(arma=weapon, angulo=0, desplazamiento_lateral=0, desplazamiento_frontal=0,)
        self.sprites_colision= [ResourceManager.load_and_scale_image(f"expl{i}.png", Settings.BOMB_SIZE, Settings.BOMB_SIZE)
                        for i in range(1, 11)]
        # Invalidamos la lógica de trayectoria, porque no se mueve
        self.arma = weapon
        self.angle_rad = 0
        self.vel_x = 0
        self.vel_y = 0

        # Posición de la explosión en el tanque
        self.x = tank.rect_element.centerx
        self.y = tank.rect_element.centery
        self.imagen = ResourceManager.load_and_scale_image("mirilla.png", Settings.BOMB_SIZE,
                                                           Settings.BOMB_SIZE)
        self.rect_element = self.imagen.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagen)

        # Parámetros de daño
        self.dano = dano
        self.radio_explosion = radio_explosion

        # Forzamos la capa de colisión (si tu tanque tiene otro atributo, cámbialo)
        self.colision_layer = tank.colision_layer_balas
        self.tiempo=pygame.time.get_ticks()

    def explotar(self, mundo):
        from ...tanks.player import Player
        ResourceManager.play_sound("8bit_bomb_explosion.wav")

        # Aplicar daño a todos los elementos en el radio
        for e in mundo.elementos_por_capa_y_pantalla[2][self.fila_pantalla][self.col_pantalla]:
            if isinstance(e,Player):
                dx = e.rect_element.centerx - self.x
                dy = e.rect_element.centery - self.y
                dist = math.hypot(dx, dy)

                #print(f"{e.rect_element.x} {e.rect_element.x} {dist} {self.radio_explosion*25}")
                if dist <= self.radio_explosion*25:
                    e.recibir_dano(self.dano)


    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Solo avanza la animación si está colisionando (explosion)."""
        if pygame.time.get_ticks() - self.tiempo >= 3000:
            self.tiempo=pygame.time.get_ticks()
            self.imagen=None
            self.iniciar_colision()
            self.explotar(mundo)
        """Actualiza la posición de la bala y verifica colisiones."""
        if self.colisionando:
            return self.actualizar_colision()


        return False
