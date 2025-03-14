import pygame

from ....extras.settings import RESIZE_PLAYER, TILE_SIZE, EVENTO_BOSS_MUERTO
from ..astar import astar
from ..enemy import Enemy, EnemyState
from ....weapons.saw import Saw


class Mecha(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 2.5, x, y, RESIZE_PLAYER, RESIZE_PLAYER, "horizontal", tank_level="_boss1", elite=False)
        self.arma = Saw(self)

    def update(self, jugador, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(EVENTO_BOSS_MUERTO))
            jugador.vida = jugador.vida_inicial
            self.eliminar = True


        if not self.en_la_misma_pantalla(jugador):
            return

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]

        start = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // TILE_SIZE) % 32, (jugador.rect_element.centery // TILE_SIZE) % 18)

        self.arma.update_secundaria(jugador, mundo)
        distancia = self.distancia_jugador(jugador)


        if (distancia < self.chase_range or self.vida != self.vida_inicial) and self.state == EnemyState.PATROLLING:
            self.state = EnemyState.CHASING

        if self.state == EnemyState.PATROLLING:
            self.manejar_patrullaje(mundo)
        elif self.state == EnemyState.CHASING:
            if distancia > TILE_SIZE*1.5:
                self.manejar_persecucion(mundo, pantalla_binaria, start, goal, TILE_SIZE)
            else:
                self.arma.activar_secundaria(mundo, jugador)

    def manejar_persecucion(self, mundo, pantalla_binaria, start, goal, tile_size):

        """Gestiona el movimiento en el estado de persecución."""
        if not self.path or self.path[-1] != goal:
            self.path = astar(pantalla_binaria, start, goal)

        if self.path:
            next_step = self.path[0]
            target_x = (self.indice_mundo_x * 32 + next_step[0]) * tile_size
            target_y = (self.indice_mundo_y * 18 + next_step[1]) * tile_size

            diff_x, diff_y = target_x - self.rect_element.centerx, target_y - self.rect_element.centery
            factor = 0.707 if diff_x and diff_y else 1

            dx = self.velocidad * factor if diff_x > 0 else -self.velocidad * factor if diff_x < 0 else 0
            dy = self.velocidad * factor if diff_y > 0 else -self.velocidad * factor if diff_y < 0 else 0

            self.actualizar_posicion(dx, dy, mundo)

            if ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18) == (
            next_step[0], next_step[1]):
                self.path.pop(0)
