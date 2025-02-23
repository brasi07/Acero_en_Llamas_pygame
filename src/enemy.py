import math
import pygame
import settings
from settings import CollisionLayer, COLLISION_RULES
from tank import Tank
from weapon import *

class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):

    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_color):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_color=tank_color)

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.patrol_movement = 100  # Rango de patrulla

        self.chase_range = 150  # Distancia para empezar a perseguir
        self.attack_range = 40 # Distancia para atacar

        self.arma = Weapon(self)

   
    def update(self, jugador):

        self.arma.update(jugador=jugador)
        # if self.state == EnemyState.PATROLLING:
        #     # Movimiento en una ruta fija
        #     pass
        # elif self.state == EnemyState.CHASING:
        #     # Movimiento hacia el jugador
        #     pass
        # elif self.state == EnemyState.ATTACKING:
        #     # Animación de ataque o colisión
        #     pass
        # pass  

    def calcular_direccion_canon(self, mundo, jugador):
        # Obtener la posición del ratón en relación con la cámara
        dirx = jugador.rect_element.x - self.rect_element.x
        diry = jugador.rect_element.y - self.rect_element.y

        return dirx, diry

       
    def draw(self, mundo, jugador):
        self.dibujar(mundo)
        self.arma.dibujar_arma(mundo)

    def distancia_player(self, player):
        return math.hypot(player.rect_element.x - self.rect_element.x, player.rect_element.y - self.rect_element.y)


class Enemy_Brown(Enemy):

    def __init__(self, x, y):
        super().__init__(3, 3, x, y, settings.RESIZE_ENEMY_BROWN, settings.RESIZE_ENEMY_BROWN, tank_color="_brown")

