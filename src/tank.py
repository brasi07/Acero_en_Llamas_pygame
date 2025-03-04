import pygame

from interactuable import Interactuable
import settings
from elements import Elemento
from resourcesmanager import ResourceManager
from settings import CollisionLayer
from weapon import Weapon


class Tank(Elemento):

    def __init__(self, vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.NONE, tank_type="enemigos", tank_level=""):

        self.vida = vida
        self.velocidad = velocidad
        self.velocidad_base = 3

        self.tank_type = tank_type
        self.tank_level = tank_level

        # Generamos sprites para el tanque
        self.sprites = ResourceManager.load_sprites(resizex, resizey, f"body{tank_level}")
        super().__init__(x, y, self.sprites["abajo"], collision_layer)

        self.arma = Weapon(self)

        self.direccion = "abajo"
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()

        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def establecer_posicion(self, x, y):
        self.rect_element.x = x
        self.rect_element.y = y

    def actualizar_posicion(self, movimiento_x, movimiento_y, mundo):
        self.verificar_colision(movimiento_x, 0, mundo)
        self.verificar_colision(0, movimiento_y, mundo)

        direccion = self.determinar_direccion(movimiento_x, movimiento_y)
        if direccion:
            self.direccion = direccion
            self.imagen = self.sprites[direccion]

    def verificar_colision(self, dx, dy, mundo):
        self.rect_element.x += dx
        self.rect_element.y += dy

        colision = False
        for e in mundo.elementos_por_capa[2]:
            if isinstance(e, Interactuable):
                e.interactuar(self)

            if self.check_collision(e):
                colision = True
                break

        if colision:
            self.rect_element.x -= dx
            self.rect_element.y -= dy


    def determinar_direccion(self, dx, dy):
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

    def equipar_especial(self, weapon):
        # Equipamos armas
        self.arma = weapon  # Equipar el Dash
        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def usar_arma_especial(self, mundo):  # usar habilidad especial
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_uso_secundaria >= settings.COOLDOWN:
            self.arma.activar_secundaria(self, mundo)
            self.ultimo_uso_secundaria = tiempo_actual  # Reinicia el cooldown

    def recibir_dano(self, dano):
        self.vida -= dano
            



