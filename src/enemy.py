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

    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_level):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_level=tank_level)

        self.barra_vida = settings.escalar_y_cargar_animacion(f"../res/UI/vida_enemigos.png", 48, 7, 5, resizey=0.3)

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.start_x = x  # Posición de inicio
        self.patrol_movement = 300  # Rango de patrulla

        self.chase_range = 250  # Distancia para empezar a perseguir
        self.attack_range = 150 # Distancia para atacar

        self.arma = Weapon(self)
        self.colision_layer_balas = CollisionLayer.BULLET_ENEMY

        self.path = []
   
    def update(self, jugador):

        if self.vida == 0:
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
            # Movimiento hacia el jugador
            self.arma.update(jugador=jugador)

            if self.rect_element.x < jugador.rect_element.x:
                self.rect_element.x += jugador.velocidad
            elif self.rect_element.x > jugador.rect_element.x:
                self.rect_element.x -= self.velocidad

            if self.rect_element.y < jugador.rect_element.y:
                self.rect_element.y += self.velocidad
            elif self.rect_element.y > jugador.rect_element.y:
                self.rect_element.y -= self.velocidad

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

