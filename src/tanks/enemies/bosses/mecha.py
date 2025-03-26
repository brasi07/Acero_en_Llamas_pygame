import pygame

from ....extras import RESIZE_PLAYER, TILE_SIZE, EVENTO_BOSS_MUERTO, ResourceManager
from ..astar import astar
from ..enemy import Enemy, EnemyState
from ....weapons import Saw


class Mecha(Enemy):
    def __init__(self, x, y):
        super().__init__(20, 2.5, x, y, RESIZE_PLAYER, RESIZE_PLAYER, "horizontal", tank_level="_boss1", elite=False)
        self.in_screen = False
        self.arma = Saw(self)
        self.id_mapa_binario = 2


    def update(self, jugador, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(EVENTO_BOSS_MUERTO))
            jugador.vida = jugador.vida_inicial
            self.eliminar = True

        if not self.en_la_misma_pantalla(jugador):
            if self.in_screen:
                ResourceManager.stop_and_unload_wav("boss_battle_loop.wav")
                self.in_screen = False
            return

        if not self.in_screen:
            ResourceManager.load_and_play_wav("boss_battle_loop.wav", -1)
            self.in_screen =  True

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]

        start = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // TILE_SIZE) % 32, (jugador.rect_element.centery // TILE_SIZE) % 18)

        self.arma.update_secundaria(jugador, mundo)
        distancia = self.distancia_jugador(jugador)


        if (distancia < self.chase_range or self.vida != self.vida_inicial) and self.state == EnemyState.PATROLLING:
            self.state = EnemyState.CHASING

        if self.state == EnemyState.PATROLLING:
            self.manejar_patrullaje(mundo, pantalla_binaria)
        elif self.state == EnemyState.CHASING:
            if distancia > TILE_SIZE*1.5:
                self.manejar_persecucion(mundo, pantalla_binaria, start, goal, TILE_SIZE)
            else:
                self.arma.activar_secundaria(mundo, jugador)

    def manejar_persecucion(self, mundo, pantalla_binaria, start, goal, tile_size, distancia_jugador=None):
        """Gestiona el movimiento en el estado de persecución."""

        # Inicializar la posición anterior si aún no existe
        if not hasattr(self, "pos_anterior"):
            self.pos_anterior = (
            (self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)

        # Recalcular ruta si no hay path o el objetivo ha cambiado
        if pygame.time.get_ticks() - self.ultima_persecucion > 500:
            self.ultima_persecucion = pygame.time.get_ticks()
            if not self.path or self.path[-1] != goal:
                self.path = astar(pantalla_binaria, start, goal, id_mapa=self.id_mapa_binario)

        if self.path:
            next_step = self.path[0]
            target_x = (self.indice_mundo_x * 32 + next_step[0]) * tile_size
            target_y = (self.indice_mundo_y * 18 + next_step[1]) * tile_size

            diff_x, diff_y = target_x - self.rect_element.centerx, target_y - self.rect_element.centery
            factor = 0.707 if diff_x and diff_y else 1

            dx = self.velocidad * factor if diff_x > 0 else -self.velocidad * factor if diff_x < 0 else 0
            dy = self.velocidad * factor if diff_y > 0 else -self.velocidad * factor if diff_y < 0 else 0

            self.actualizar_posicion(dx, dy, mundo)

            # Nueva posición del enemigo en coordenadas de tile
            pos_actual = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)

            # Si ha cambiado de tile, actualizar la matriz binaria
            if pos_actual != self.pos_anterior:
                self.desmarcar_nodo_ocupado(pantalla_binaria, (self.pos_anterior[0], self.pos_anterior[1]),
                                            self.id_mapa_binario)  # Desmarca el anterior
                self.marcar_nodo_ocupado(pantalla_binaria, (pos_actual[0], pos_actual[1]),
                                         self.id_mapa_binario)  # Marca la nueva posición
                self.pos_anterior = pos_actual  # Actualiza la última posición registrada

            # Si ha alcanzado el siguiente paso del path, eliminarlo
            if pos_actual == (next_step[0], next_step[1]):
                self.path.pop(0)
