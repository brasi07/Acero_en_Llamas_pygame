import pygame

from extras.settings import CollisionLayer, TILE_SIZE
from elements.interactable.pickable import PickableWeapon
from tanks.enemies.astar import *
from tanks.tank import Tank
from weapons import Weapon
from weapons.weapon_pool import WeaponPool


class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):
    # TODO: Pasar el daño del enemigo para ajustar los distintos niveles
    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_level, modo_patrulla=0):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_level=tank_level)

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

        self.modo_patrulla = self.determinar_modo_patrulla(modo_patrulla)
        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.start_x = self.x
        self.start_y = self.y
        self.patrol_movement = 350  # Rango de patrulla

        self.patrol_phase = 0  # Fase de patrulla

        self.chase_range = 300  # Distancia para empezar a perseguir
        self.attack_range = 280 # Distancia para atacar

        self.arma = Weapon(self)
        self.arma_drop = None

        if self.modo_patrulla == "elite":
            self.arma_drop = WeaponPool().random_weapon()
            self.arma = WeaponPool().set_enemy_weapon(self)

        self.colision_layer_balas = CollisionLayer.BULLET_ENEMY

        self.indice_mundo_x = (self.rect_element.x // TILE_SIZE) // 32
        self.indice_mundo_y = (self.rect_element.y // TILE_SIZE) // 18

        self.path = []

    @staticmethod
    def determinar_modo_patrulla(modo_patrulla):
        modos = {
            0: "horizontal",
            1: "circular",
            2: "vertical",
            3: "torreta",
            4: "elite"
        }
        return modos.get(modo_patrulla, "circular")

    def update(self, jugador, mundo):
        """Actualiza el estado del enemigo dependiendo de la distancia y el estado actual."""
        if not self.en_la_misma_pantalla(jugador):
            return

        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]

        start = ((self.rect_element.centerx // TILE_SIZE) % 32, (self.rect_element.centery // TILE_SIZE) % 18)
        goal = ((jugador.rect_element.centerx // TILE_SIZE) % 32, (jugador.rect_element.centery // TILE_SIZE) % 18)

        if self.vida <= 0:
            self.eliminar = True
            self.drop_weapon(mundo)

        self.arma.update(mundo, tank=jugador)
        distancia = self.distancia_jugador(jugador)

        if (distancia < self.chase_range or self.vida != self.vida_inicial) and self.state == EnemyState.PATROLLING:
            self.state = EnemyState.CHASING

        if self.state == EnemyState.PATROLLING:
            self.manejar_patrullaje(mundo)
        elif self.state == EnemyState.CHASING:
            self.manejar_persecucion(mundo, pantalla_binaria, start, goal, TILE_SIZE)
        elif self.state == EnemyState.ATTACKING:
            self.manejar_ataque(mundo, pantalla_binaria, start, goal)


    def drop_weapon(self, mundo):
        if self.modo_patrulla == "elite":
            drop = PickableWeapon(self.x // TILE_SIZE, self.y // TILE_SIZE, self.arma_drop)
            mundo.elementos_por_capa[2].append(drop)
            mundo.elementos_actualizables.append(drop)

    def manejar_patrullaje(self, mundo):
        """Controla el movimiento en el estado de patrullaje."""
        if self.modo_patrulla == "circular":
            movimientos = [
                (self.velocidad, 0, self.rect_element.x >= self.start_x + self.patrol_movement, 1),
                (0, self.velocidad, self.rect_element.y >= self.start_y + self.patrol_movement, 2),
                (-self.velocidad, 0, self.rect_element.x <= self.start_x, 3),
                (0, -self.velocidad, self.rect_element.y <= self.start_y, 0)
            ]
            dx, dy, cambiar, nueva_fase = movimientos[self.patrol_phase]
            if cambiar:
                self.patrol_phase = nueva_fase

        elif self.modo_patrulla == "horizontal":
            dx, dy = self.velocidad * self.patrol_direction, 0
            if self.actualizar_posicion(dx, dy, mundo):
                self.patrol_direction *= -1
            if abs(self.rect_element.x - self.start_x) > self.patrol_movement:
                self.patrol_direction *= -1

        elif self.modo_patrulla == "vertical":
            dx, dy = 0, self.velocidad * self.patrol_direction
            if self.actualizar_posicion(dx, dy, mundo):
                self.patrol_direction *= -1
            if abs(self.rect_element.y - self.start_y) > self.patrol_movement:
                self.patrol_direction *= -1

    def manejar_persecucion(self, mundo, pantalla_binaria, start, goal, tile_size):
        """Gestiona el movimiento en el estado de persecución."""
        if raycasting(pantalla_binaria, start, goal):
            self.state = EnemyState.ATTACKING
            return

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

            if ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18) == (next_step[0], next_step[1]):
                self.path.pop(0)

    def manejar_ataque(self, mundo, pantalla_binaria, start, goal):
        """Gestiona la lógica de ataque."""
        if not raycasting(pantalla_binaria, start, goal):
            self.state = EnemyState.CHASING
            self.path = astar(pantalla_binaria, start, goal)
        elif pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= self.arma.cooldown:

            if self.modo_patrulla == "elite":
                self.arma.activar_secundaria(self, mundo)
            else:
                self.arma.activar()

            self.tiempo_ultimo_disparo = pygame.time.get_ticks()

    def calcular_direccion_canon(self, mundo, jugador):
        # Obtener la posición del ratón en relación con la cámara
        dirx = jugador.rect_element.x - self.rect_element.x
        diry = jugador.rect_element.y - self.rect_element.y

        return dirx, diry
    
    def patrullar(self):
        self.state = EnemyState.PATROLLING
        self.establecer_posicion(self.start_x, self.start_y)

    def en_la_misma_pantalla(self, jugador):
        return (jugador.rect_element.x // TILE_SIZE // 32 == self.indice_mundo_x) and (jugador.rect_element.y // TILE_SIZE // 18 == self.indice_mundo_y)

       
    def dibujar_enemigo(self, pantalla, x, y):
        self.dibujar(pantalla, x, y)
        self.arma.dibujar_arma(pantalla, x, y)

    def distancia_jugador(self, jugador):
        return math.hypot(jugador.rect_element.x - self.rect_element.x, jugador.rect_element.y - self.rect_element.y)
