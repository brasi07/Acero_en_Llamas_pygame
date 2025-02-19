import numpy as np
import pygame

import settings
from bullet import Bala
from elements import Elemento
from settings import CollisionLayer
from weapon import Dash


class Tank(Elemento):
    def __init__(self, hp, speed, x, y, tamaño_tile, collision_layer=CollisionLayer.NONE):
        self.hp = hp
        self.speed = speed
        self.tamaño_tile = tamaño_tile

        # Cargar sprites
        self.sprite_base = self.escalar_y_cargar("../res/entidades/jugador/bodies/body_tracks.png")
        self.sprite_base_45 = self.escalar_y_cargar("../res/entidades/jugador/bodies/body_tracks_45.png")

        self.sprite_cannon = self.escalar_y_cargar("../res/entidades/jugador/armas/tanque_canon.png")
        self.sprites = self.generar_sprites()

        super().__init__(x, y, self.sprites["abajo"], collision_layer)

        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, 0)
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

        self.direccion = "abajo"

        self.balas = []
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.angulo_cannon = 0

        # Equipamos armas
        self.equip_special(Dash())

    def equip_special(self, weapon=Dash()):
        # Equipamos armas
        self.arma_secundaria = weapon  # Equipar el Dash
        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def generar_sprites(self):
        return {
            "arriba": self.sprite_base,
            "derecha": pygame.transform.rotate(self.sprite_base, -90),
            "izquierda": pygame.transform.rotate(self.sprite_base, 90),
            "abajo": pygame.transform.rotate(self.sprite_base, 180),
            "arriba_izquierda": self.sprite_base_45,
            "arriba_derecha": pygame.transform.rotate(self.sprite_base_45, -90),
            "abajo_izquierda": pygame.transform.rotate(self.sprite_base_45, 90),
            "abajo_derecha": pygame.transform.rotate(self.sprite_base_45, 180),
            "canhon": self.sprite_cannon
        }

    def escalar_y_cargar(self, ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (self.tamaño_tile * settings.RESIZE_PLAYER, self.tamaño_tile * settings.RESIZE_PLAYER))

    def aim(self, dirx, diry):
        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diry, dirx))  # Guardar el ángulo para disparos

        # Rotar la imagen del cañón
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -self.angulo_cannon - 90)

        # Mantener el cañón centrado en el tanque
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

    def actualizar_posicion(self, movimiento_x, movimiento_y, mundo):
        colision_x = self.verificar_colision(movimiento_x, 0, mundo)
        colision_y = self.verificar_colision(0, movimiento_y, mundo)

        direccion = self.determinar_direccion(movimiento_x, movimiento_y, colision_x, colision_y)
        if direccion:
            self.direccion = direccion
            self.imagen = self.sprites[direccion]

    def determinar_direccion(self, dx, dy, colision_x, colision_y):
        direcciones = {
            (-1, -1): "arriba_izquierda",
            (1, -1): "arriba_derecha",
            (-1, 1): "abajo_izquierda",
            (1, 1): "abajo_derecha",
            (-1, 0): "izquierda",
            (1, 0): "derecha",
            (0, -1): "arriba",
            (0, 1): "abajo"
        }
        dx = -1 if dx < 0 else (1 if dx > 0 else 0)
        dy = -1 if dy < 0 else (1 if dy > 0 else 0)
        return direcciones.get((dx, dy), self.direccion)  # Usa la última dirección si no encuentra coincidencia

    def verificar_colision(self, dx, dy, mundo):
        self.rect_element.x += dx
        self.rect_element.y += dy
        colision = any(self.check_collision(e) for e in mundo.elementos_por_capa[2])
        if colision:
            self.rect_element.x -= dx
            self.rect_element.y -= dy
        return colision

    def use_special(self): #usar habilidad especial
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_uso_secundaria >= settings.COOLDOWN:
            self.arma_secundaria.activar(self)
            self.ultimo_uso_secundaria = tiempo_actual  # Reinicia el cooldown


    def disparar(self):
        cannon_tip = self.get_cannon_tip()  # Obtener la punta del cañón
        nueva_bala = Bala(cannon_tip, self.angulo_cannon, self.tamaño_tile, CollisionLayer.BULLET_PLAYER)
        self.balas.append(nueva_bala)

    def get_cannon_tip(self):
        """Calcula la punta del cañón después de la rotación"""
        angle_rad = np.radians(self.angulo_cannon)  # Convertir ángulo a radianes
        cannon_length = self.rect_canon.height // 4  # Mitad de la altura del cañón

        # Calcular desplazamiento desde el centro del cañón
        x_offset = cannon_length * np.cos(angle_rad)
        y_offset = cannon_length * np.sin(angle_rad)

        # Devolver la nueva posición del midtop corregido
        return self.rect_canon.centerx + x_offset, self.rect_canon.centery + y_offset