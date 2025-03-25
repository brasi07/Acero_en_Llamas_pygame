import pygame
from ...extras import CollisionLayer, TILE_SIZE
from ...elements.interactable import PickableWeapon
from .astar import *
from ..tank import Tank
from ...weapons import Weapon, WeaponPool

class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):
    def __init__(self, vida, velocidad, x, y, resizex, resizey, modo_patrulla, elite, tank_level, id_mapa=None):
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_level=tank_level)

        self.state = EnemyState.PATROLLING if modo_patrulla != "torreta" else EnemyState.ATTACKING
        self.chase_range = 300
        self.attack_range = 280
        self.id_mapa_binario = id_mapa

        self.modo_patrulla = modo_patrulla
        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.start_x = self.x
        self.start_y = self.y
        self.patrol_movement = 350  # Rango de patrulla
        self.patrol_phase = 0  # Fase de patrulla

        self.elite = elite
        self.arma_drop = WeaponPool().random_weapon()
        self.arma = WeaponPool().set_enemy_weapon(self) if elite else Weapon(self)

        if elite:
            self.velocidad *= 1.2
            factor = 1 + (1.5 / math.log(self.vida_inicial + 1))  # Reduce el aumento con vida más alta
            self.vida_inicial = int(self.vida_inicial * factor)
            self.vida = self.vida_inicial
            self.chase_range *= 1.5

        self.colision_layer_balas = CollisionLayer.BULLET_ENEMY

        self.indice_mundo_x = (self.rect_element.x // TILE_SIZE) // 32
        self.indice_mundo_y = (self.rect_element.y // TILE_SIZE) // 18

        self.path = []
        self.tiempo_ultimo_disparo = 0  # Control del cooldown de ataque
        self.ultima_persecucion = 0  # Control del tiempo de la última persecución

    def update(self, jugador, mundo):

        """Actualiza el estado del enemigo dependiendo de la distancia y el estado actual."""
        if not self.en_la_misma_pantalla(jugador):
            return

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]
        start = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // TILE_SIZE) % 32, (jugador.rect_element.centery // TILE_SIZE) % 18)

        self.marcar_nodo_ocupado(pantalla_binaria, start, self.id_mapa_binario)    

        if self.vida <= 0:
            self.eliminar = True
            if self.elite:  self.drop_weapon(mundo)

        self.arma.update(mundo, tank=jugador)
        distancia = self.distancia_jugador(jugador)

        if (distancia < self.chase_range or self.vida != self.vida_inicial) and self.state == EnemyState.PATROLLING:
            self.state = EnemyState.CHASING

        if self.state == EnemyState.PATROLLING and self.modo_patrulla != "torreta":
            self.manejar_patrullaje(mundo, pantalla_binaria)
        elif self.state == EnemyState.CHASING and self.modo_patrulla != "torreta":
            self.manejar_persecucion(mundo, pantalla_binaria, start, goal, TILE_SIZE, distancia_jugador=distancia)
        elif self.state == EnemyState.ATTACKING:
            self.manejar_ataque(mundo, pantalla_binaria, start, goal)

    def marcar_nodo_ocupado(self, pantalla_binaria, pos, id):
        """Actualiza la posición del enemigo en el mapa."""
        x, y = pos
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(pantalla_binaria) and 0 <= nx < len(pantalla_binaria[0]) and pantalla_binaria[ny][nx] == 0:
                    pantalla_binaria[ny][nx] = id

    def desmarcar_nodo_ocupado(self, pantalla_binaria, pos, id):
        """Restaura la posición (x, y) y sus 8 vecinos a transitables en el mapa binario."""
        x, y = pos
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(pantalla_binaria) and 0 <= nx < len(pantalla_binaria[0]) and pantalla_binaria[ny][nx] == id:
                    pantalla_binaria[ny][nx] = 0  # Solo borrar el id, dejando los 1 intactos

    def drop_weapon(self, mundo):
        drop = PickableWeapon(self.rect_element.centerx / TILE_SIZE, self.rect_element.centery / TILE_SIZE,
                              self.arma_drop)
        mundo.elementos_por_capa_y_pantalla[2][self.fila_pantalla][self.col_pantalla].append(drop)
        mundo.elementos_actualizables.append(drop)

    def manejar_patrullaje(self, mundo, pantalla_binaria):
        if self.modo_patrulla == "horizontal":
            dx, dy = self.velocidad * self.patrol_direction, 0
            pos_anterior = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
            if self.actualizar_posicion(dx, dy, mundo):
                self.patrol_direction *= -1
                self.marcar_nodo_ocupado(pantalla_binaria, ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18), self.id_mapa_binario)
                self.desmarcar_nodo_ocupado(pantalla_binaria, pos_anterior, self.id_mapa_binario)
            if abs(self.rect_element.x - self.start_x) > self.patrol_movement:
                self.patrol_direction *= -1

        elif self.modo_patrulla == "vertical":
            dx, dy = 0, self.velocidad * self.patrol_direction
            pos_anterior = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
            if self.actualizar_posicion(dx, dy, mundo):
                self.patrol_direction *= -1
                self.marcar_nodo_ocupado(pantalla_binaria, ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18), self.id_mapa_binario)
                self.desmarcar_nodo_ocupado(pantalla_binaria, pos_anterior, self.id_mapa_binario)
            if abs(self.rect_element.y - self.start_y) > self.patrol_movement:
                self.patrol_direction *= -1

    def manejar_persecucion(self, mundo, pantalla_binaria, start, goal, tile_size, distancia_jugador=None):
        """Gestiona el movimiento en el estado de persecución."""

        # Inicializar la posición anterior si aún no existe
        if not hasattr(self, "pos_anterior"):
            self.pos_anterior = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)



        if distancia_jugador < self.attack_range and (raycasting(pantalla_binaria, start, goal) or pantalla_binaria[goal[1]][goal[0]] == 1):
            self.state = EnemyState.ATTACKING
            return

        # Recalcular ruta si no hay path o el objetivo ha cambiado
        if pygame.time.get_ticks() - self.ultima_persecucion > 2000:
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

                self.desmarcar_nodo_ocupado(pantalla_binaria, (self.pos_anterior[0], self.pos_anterior[1]), self.id_mapa_binario)  # Desmarca el anterior
                self.marcar_nodo_ocupado(pantalla_binaria,( pos_actual[0], pos_actual[1]), self.id_mapa_binario)  # Marca la nueva posición
                self.pos_anterior = pos_actual  # Actualiza la última posición registrada

            # Si ha alcanzado el siguiente paso del path, eliminarlo
            if pos_actual == (next_step[0], next_step[1]):
                self.path.pop(0)

    def manejar_ataque(self, mundo, pantalla_binaria, start, goal):
        """Gestiona la lógica de ataque."""
        if not raycasting(pantalla_binaria, start, goal) and self.modo_patrulla != "torreta":
            self.state = EnemyState.CHASING
        elif self.arma.cooldown and pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= self.arma.cooldown:
            if self.elite:
                self.arma.activar_secundaria(mundo)
            else:
                self.arma.activar(mundo)
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()

    def calcular_direccion_canon(self, mundo, jugador, arma=None):
        # Obtener la posición del ratón en relación con la cámara
        dirx = jugador.rect_element.centerx - self.arma.x
        diry = jugador.rect_element.centery - self.arma.y

        return dirx, diry
    
    def patrullar(self):
        if self.modo_patrulla != "torreta":
            self.state = EnemyState.PATROLLING
            self.establecer_posicion(self.start_x, self.start_y)

    def en_la_misma_pantalla(self, jugador):
        return (jugador.rect_element.x // TILE_SIZE // 32 == self.indice_mundo_x) and (jugador.rect_element.y // TILE_SIZE // 18 == self.indice_mundo_y)

    def dibujar_enemigo(self, pantalla, x, y):
        self.dibujar(pantalla, x, y)
        self.arma.dibujar_arma(pantalla, x, y)

    def distancia_jugador(self, jugador):
        return math.hypot(jugador.rect_element.x - self.rect_element.x, jugador.rect_element.y - self.rect_element.y)

