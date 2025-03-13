import pygame
from extras import settings
from weapons.bullets.bullet import Bullet
from extras.resourcesmanager import ResourceManager
from weapons.weapon import Weapon

class Shotgun(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "turret_01_mk4"
        self.tiempo_inicio = None  # Guarda el tiempo de activacivación
        self.animacion = ResourceManager.load_animation(f"{self.nombre_sprite}.png", 128, 128, 8)

        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, mundo, tank=None):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bullet(self)
        bala_izquierda = Bullet(self, self.angulo_cannon - 15)
        bala_derecha = Bullet(self, self.angulo_cannon + 15)

        mundo.add_bullet(bala_central)
        mundo.add_bullet(bala_izquierda)
        mundo.add_bullet(bala_derecha)
        self.activo = True

    def update_secundaria(self, tank, mundo):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= settings.TIME_FRAME:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina

                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                self.imagen_canon = self.imagen_canon_base