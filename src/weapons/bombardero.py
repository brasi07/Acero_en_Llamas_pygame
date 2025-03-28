import pygame
import math
import numpy as np

from ..extras import Settings, ResourceManager
from .weapon import Weapon
from .bullets.bullet_explosion import ExplosionBullet  # Ajusta la ruta según tu proyecto

class ExplosionWeapon(Weapon):
    """
    Arma con cañón invisible y sin animación.
    Al activarse, crea una bala explosiva que detona inmediatamente.
    """

    def __init__(self, tank, posicion=None):
        super().__init__(tank, posicion)

        # Generamos una superficie transparente de 1x1 para "ocultar" el cañón.
        self.invisible_surface = pygame.Surface((1, 1), pygame.SRCALPHA)

        # Sobrescribimos las imágenes base para que no se dibuje nada.
        self.imagen_canon_base = self.invisible_surface
        self.imagen_canon = self.invisible_surface
        self.imagen_bala = ResourceManager.load_and_scale_image("mirilla.png",Settings.RESOLUTION_SCALE*50,Settings.RESOLUTION_SCALE*50)

  # Si quieres asegurarte de que no se use ninguna bala gráfica

        # Si tu clase base Weapon ajusta rect_canon, dejamos algo mínimo:
        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)

        # Si tu arma no va a usar cooldown ni angle, puedes ignorarlo:
        self.cooldown = 0  # o cualquier valor que quieras
        self.angulo_cannon = 0

    def activar(self, mundo):
        """
        Al activar, se crea la bala explosiva (ExplosionBullet) que explota inmediatamente.
        """
        # Opcional: reproducir algún sonido de explosión o disparo.
        # ResourceManager.play_sound("8bit_bomb_explosion.wav")

        # Crear la bala que explota de inmediato
        bala_explosiva = ExplosionBullet(self,self.tank,mundo)
        mundo.add_bullet(bala_explosiva)

    def update(self, mundo, tank=None):
        """
        Si tu arma no requiere cambiar ángulos/posición, puedes dejarlo vacío o mínimo.
        """

        pass

    def dibujar_arma(self, pantalla, x, y):
        """
        No dibujamos nada, el cañón es "invisible".
        """
        pass

    def activar_secundaria(self, mundo, tank=None):
        """
        Si no tienes arma secundaria, deja esto vacío o implementa lo que necesites.
        """
        pass

    def update_secundaria(self, tank, mundo):
        pass
