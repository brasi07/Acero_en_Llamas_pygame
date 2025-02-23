import math
import pygame
import settings
from settings import CollisionLayer, COLLISION_RULES
from tank import Tank

class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):

    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_type):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, tank_type=tank_type, collision_layer=CollisionLayer.ENEMY, ruta="../res/entidades/enemigos/")

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

   
    def update(self):
        if self.state == EnemyState.PATROLLING:
            # Movimiento en una ruta fija
            pass
        elif self.state == EnemyState.CHASING:
            # Movimiento hacia el jugador
            pass
        elif self.state == EnemyState.ATTACKING:
            # Animación de ataque o colisión
            pass
        pass  # Aquí iría la IA de movimiento

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

    # def distancia_player(self, player):


class Enemy_Brown(Enemy):

    def __init__(self, x, y):
        super().__init__(3, 3, x, y, settings.RESIZE_ENEMY_BROWN, settings.RESIZE_ENEMY_BROWN, "_brown")

