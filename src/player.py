import pygame
import settings
import numpy as np
import math

from settings import CollisionLayer
from elements import Elemento
from bullet import Bala
from weapon import Dash


class Player(Elemento):

    def __init__(self, x, y, tamaño_tile):
        self.tamaño_tile = tamaño_tile

        # Cargar sprites
        self.sprite_base = self.escalar_y_cargar("../res/entidades/jugador/bodies/body_tracks.png", settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)
        self.sprite_base_45 = self.escalar_y_cargar("../res/entidades/jugador/bodies/body_tracks_45.png", settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)
        self.sprites = self.generar_sprites()
        self.sprite_cannon = self.sprites["canhon"]

        # Llamamos al constructor de la clase base (Elemento)
        super().__init__(x, y, self.sprites["abajo"], CollisionLayer.PLAYER)

        # Inicialización de atributos del jugador
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, 0)
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

        self.velocidad_base = 3
        self.velocidad = self.velocidad_base
        self.direccion = "abajo"

        self.balas = []
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.angulo_cannon = 0

        # Equipamos armas
        self.arma_secundaria = Dash()  # Equipar el Dash
        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def escalar_y_cargar(self, ruta, resizex, resizey):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (resizex * self.tamaño_tile, resizey * self.tamaño_tile))

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
            "canhon": self.escalar_y_cargar("../res/entidades/jugador/armas/tanque_canon.png", settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)
        }

    def update(self, mundo):
        self.mover(mundo)
        self.gestionar_disparo()
        self.gestionar_arma_secundaria()
        self.arma_secundaria.update(self)
        self.verificar_fuera_pantalla(mundo)

        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def mover(self, mundo):
        teclas = pygame.key.get_pressed()
        movimiento_x, movimiento_y = self.obtener_movimiento(teclas)
        self.actualizar_posicion(movimiento_x, movimiento_y, mundo)

    def obtener_movimiento(self, teclas):
        movimiento_x = (-self.velocidad if teclas[pygame.K_LEFT] or teclas[pygame.K_a] else 0) + \
                       (self.velocidad if teclas[pygame.K_RIGHT] or teclas[pygame.K_d] else 0)
        movimiento_y = (-self.velocidad if teclas[pygame.K_UP] or teclas[pygame.K_w] else 0) + \
                       (self.velocidad if teclas[pygame.K_DOWN] or teclas[pygame.K_s] else 0)
        if movimiento_x and movimiento_y:
            movimiento_x *= 0.707
            movimiento_y *= 0.707
        return movimiento_x, movimiento_y

    def actualizar_posicion(self, movimiento_x, movimiento_y, mundo):
        colision_x = self.verificar_colision(movimiento_x, 0, mundo)
        colision_y = self.verificar_colision(0, movimiento_y, mundo)

        direccion = self.determinar_direccion(movimiento_x, movimiento_y, colision_x, colision_y)
        if direccion:
            self.direccion = direccion
            self.imagen = self.sprites[direccion]

    def verificar_colision(self, dx, dy, mundo):
        self.rect_element.x += dx
        self.rect_element.y += dy
        colision = any(self.check_collision(e) for e in mundo.elementos_por_capa[2])
        if colision:
            self.rect_element.x -= dx
            self.rect_element.y -= dy
        return colision

    def verificar_fuera_pantalla(self, mundo):
        if self.rect_element.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif self.rect_element.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif self.rect_element.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif self.rect_element.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

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

    def gestionar_disparo(self):
        if pygame.mouse.get_pressed()[0]:
            if pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= 1000:
                self.disparar()
                self.tiempo_ultimo_disparo = pygame.time.get_ticks()

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

    def update_cannon_position(self, mundo):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        diff_x = cursorx - (self.rect_element.centerx - mundo.camara_x)
        diff_y = cursory - (self.rect_element.centery - mundo.camara_y)

        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diff_y, diff_x))  # Guardar el ángulo para disparos

        # Rotar la imagen del cañón
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -self.angulo_cannon - 90)

        # Mantener el cañón centrado en el tanque
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

    def gestionar_arma_secundaria(self):
        if pygame.mouse.get_pressed()[2]:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_uso_secundaria >= settings.COOLDOWN:
                self.arma_secundaria.activar(self)
                self.ultimo_uso_secundaria = tiempo_actual  # Reinicia el cooldown

    def draw(self, mundo):
        for bala in self.balas:
            bala.draw(mundo.pantalla, mundo)
        self.dibujar(mundo.pantalla, mundo)
        self.update_cannon_position(mundo)
        mundo.pantalla.blit(self.imagen_canon, (self.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))