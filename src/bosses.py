import pygame

import settings
from bullet import Bala
from enemy import Enemy
from resourcesmanager import ResourceManager
from tank import Tank
from weapon import Weapon


class Mecha(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 2.5, x, y, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, tank_level="_boss1")

class MegaCannon(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 0, x, y, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, tank_level="_boss2")
        self.muerto = False
        self.arma = WeaponMegaCannon

    def update(self, jugador, mundo):
        if self.vida <= 0:
            self.muerto = True
            self.vida = 20

        self.arma.update_secundaria(self, mundo)

    def gestionar_armas(self, mundo):
        if pygame.mouse.get_pressed()[1]:
            self.usar_arma_especial(mundo)


class WeaponMegaCannon(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = None  # Guarda el tiempo de activacivación
        self.animacion = ResourceManager.load_animation("mega_canon.png", 128, 128, 11, settings.RESIZE_PLAYER * 2, settings.RESIZE_PLAYER * 2)
        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, tank, mundo):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bala(self.get_cannon_tip(), self.angulo_cannon, self.tank.colision_layer_balas)
        bala_izquierda = Bala(self.get_cannon_tip(), self.angulo_cannon - 15, self.tank.colision_layer_balas)
        bala_derecha = Bala(self.get_cannon_tip(), self.angulo_cannon + 15, self.tank.colision_layer_balas)
        self.balas.append(bala_central)
        self.balas.append(bala_izquierda)
        self.balas.append(bala_derecha)
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


class WarTrain(Tank):
    def __init__(self, x, y):
        super().__init__(20, 2.5, x, y, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)

