import math
from settings import CollisionLayer, COLLISION_RULES
from tank import Tank
from weapon import *
from astar import *

class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):

    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_level):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_level=tank_level)

        self.barra_vida = ResourceManager.load_animation(f"vida_enemigos.png", 48, 7, 5, resizey=0.3)

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.start_x = x  # Posición de inicio
        self.patrol_movement = 300  # Rango de patrulla

        self.chase_range = 250  # Distancia para empezar a perseguir
        self.attack_range = 150 # Distancia para atacar

        self.arma = Weapon(self)
        self.colision_layer_balas = CollisionLayer.BULLET_ENEMY

        self.indice_mundo_x = (self.rect_element.x // settings.TILE_SIZE) // 32
        self.indice_mundo_y = (self.rect_element.y // settings.TILE_SIZE) // 18

        self.path = []
   
    def update(self, jugador, mundo):
        tile_size = settings.TILE_SIZE

        # Obtenemos el mapa binario en el que estamos
        pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]

        if self.vida <= 0:
            self.eliminar = True

        distancia = self.distancia_jugador(jugador)

        if distancia < self.attack_range:
            self.state = EnemyState.ATTACKING
        elif distancia < self.chase_range:
            self.state = EnemyState.CHASING
        else:
            self.state = EnemyState.PATROLLING

        
        if self.state == EnemyState.PATROLLING:
            # Movimiento en una ruta fija
            self.rect_element.x += self.velocidad * self.patrol_direction
            # Cambiar dirección si se alcanza el rango de patrulla
            if abs(self.rect_element.x - self.start_x) > self.patrol_movement:
                self.patrol_direction *= -1

        elif self.state == EnemyState.CHASING:
            self.arma.update(jugador=jugador)
            # Movimiento hacia el jugador
            start = ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18)
            goal = ((jugador.rect_element.centerx // tile_size) % 32, (jugador.rect_element.centery // tile_size) % 18)

            if not self.path or self.path[-1] != goal:  # Solo recalcular si el jugador cambió de celda
                self.path = astar(pantalla_binaria, start, goal)

            if self.path:
                next_step = self.path[0]
                target_x = (self.indice_mundo_x * 32 + next_step[0]) * tile_size
                target_y = (self.indice_mundo_y * 18 + next_step[1]) * tile_size

                diff_x = target_x - self.rect_element.centerx
                diff_y = target_y - self.rect_element.centery

                if abs(diff_x) > 0 and abs(diff_y) > 0:
                    factor = 0.707  # Ajuste para diagonales (1/√2)
                else:
                    factor = 1

                self.rect_element.x += self.velocidad * factor if diff_x > 0 else -self.velocidad * factor if diff_x < 0 else 0
                self.rect_element.y += self.velocidad * factor if diff_y > 0 else -self.velocidad * factor if diff_y < 0 else 0

                if ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18) == (next_step[0], next_step[1]):
                    self.path.pop(0)

        elif self.state == EnemyState.ATTACKING:
            # Animación de ataque o colisión
            self.arma.update(jugador=jugador)
            pass

    # def movimiento(self,):

    def calcular_direccion_canon(self, mundo, jugador):
        # Obtener la posición del ratón en relación con la cámara
        dirx = jugador.rect_element.x - self.rect_element.x
        diry = jugador.rect_element.y - self.rect_element.y

        return dirx, diry

       
    def dibujar_enemigo(self, mundo, jugador):
        self.dibujar(mundo)
        self.arma.dibujar_arma(mundo)

    def distancia_jugador(self, jugador):
        return math.hypot(jugador.rect_element.x - self.rect_element.x, jugador.rect_element.y - self.rect_element.y)


class Enemy_Brown(Enemy):

    def __init__(self, x, y):
        super().__init__(3, 2, x, y, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, tank_level="_brown")

