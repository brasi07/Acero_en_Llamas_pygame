import pygame
from elements.interactable.mine import Mine
from extras.settings import TILE_SIZE
from weapons.weapon import Weapon

class MineLauncher(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = pygame.time.get_ticks()
        # self.imagenes_accesorio_base = self.tank.generar_sprites(settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, "jugador", "armas/mina")
        self.activo = False

    def activar_secundaria(self, tank, mundo):
        self.activo = True
        self.tiempo_inicio = pygame.time.get_ticks()
        nova_mina = Mine(self.tank.rect_element.centerx / TILE_SIZE, self.tank.rect_element.centery / TILE_SIZE)
        mundo.elementos_por_capa[2].append(nova_mina)
        mundo.elementos_actualizables.append(nova_mina)
        mundo.add_mine(nova_mina)

    def update_secundaria(self, tank, mundo):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio  # Milisegundos desde el inicio del Dash