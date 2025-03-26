import pygame
from ..elements.interactable import Mine
from ..extras import TILE_SIZE, ResourceManager, RESIZE_PLAYER, COOLDOWN
from .weapon import Weapon

class MineLauncher(Weapon):
    def __init__(self, tank, posicion=None):
        super().__init__(tank, posicion)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.imagenes_accesorio_base = ResourceManager.load_sprites(RESIZE_PLAYER, RESIZE_PLAYER, "mines")
        self.activo = False
        self.cooldown = COOLDOWN


    def activar_secundaria(self, mundo, tank=None):
        self.activo = True
        self.tiempo_inicio = pygame.time.get_ticks()
        if self.tank.direccion == "arriba" or self.tank.direccion == "arriba_izquierda":
            posx, posy =self.tank.rect_element.centerx/TILE_SIZE, self.tank.rect_element.bottom/TILE_SIZE
        elif self.tank.direccion == "izquierda" or self.tank.direccion == "abajo_izquierda":
            posx, posy = self.tank.rect_element.right / TILE_SIZE, self.tank.rect_element.centery / TILE_SIZE
        elif self.tank.direccion == "abajo" or self.tank.direccion == "abajo_derecha":
            posx, posy = self.tank.rect_element.centerx / TILE_SIZE, self.tank.rect_element.top / TILE_SIZE
        else:
            posx, posy = self.tank.rect_element.left / TILE_SIZE, self.tank.rect_element.centery / TILE_SIZE

        nova_mina = Mine(posx, posy)
        mundo.elementos_por_capa_y_pantalla[2][nova_mina.fila_pantalla][nova_mina.col_pantalla].append(nova_mina)
        mundo.elementos_actualizables.append(nova_mina)
        mundo.add_mine(nova_mina)

    def update_secundaria(self, tank, mundo):
        tiempo_actual = pygame.time.get_ticks()
        self.imagen_accesorio = self.imagenes_accesorio_base[tank.direccion]
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio  # Milisegundos desde el inicio del Dash

    def get_pickable_image(self):
        return self.imagenes_accesorio_base["arriba"]