import pygame

from extras.resourcesmanager import ResourceManager
from extras.settings import CollisionLayer, TILE_SIZE
from tanks.enemies.astar import *
from tanks.tank import Tank
from weapons import Weapon


class EnemyState:
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"

class Enemy(Tank):
    # TODO: Pasar el daño del enemigo para ajustar los distintos niveles
    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_level, modo_patrulla=0):
        
        super().__init__(vida, velocidad, x, y, resizex, resizey, collision_layer=CollisionLayer.ENEMY, tank_level=tank_level)

        self.barra_vida = ResourceManager.load_animation(f"vida_enemigos.png", 48, 7, 5, resizey=0.3)

        # Inicializamos en patrulla
        self.state = EnemyState.PATROLLING

        self.modo_patrulla = self.determinar_modo_patrulla(modo_patrulla)
        self.patrol_direction = 1  # 1 derecha, -1 izquierda
        self.start_x = self.x
        self.start_y = self.y
        self.patrol_movement = 350  # Rango de patrulla

        self.patrol_phase = 0  # Fase de patrulla

        self.chase_range = 300  # Distancia para empezar a perseguir
        self.jugador_visto = False
        self.attack_range = 280 # Distancia para atacar

        self.arma = Weapon(self)
        self.colision_layer_balas = CollisionLayer.BULLET_ENEMY

        self.indice_mundo_x = (self.rect_element.x // TILE_SIZE) // 32
        self.indice_mundo_y = (self.rect_element.y // TILE_SIZE) // 18

        self.ultimo_cambio_estado = pygame.time.get_ticks()

        self.path = []

    def determinar_modo_patrulla(self, modo_patrulla):
        if modo_patrulla == 0:
            return "horizontal"
        elif modo_patrulla == 1:
            return "circular"
        elif modo_patrulla == 2:
            return "vertical"
        else:
            return "circular"
   
    def update(self, jugador, mundo):
        tile_size = TILE_SIZE

        # Activar la lógica solo si el jugador está en la misma pantalla
        if self.en_la_misma_pantalla(jugador):

            # Obtenemos el mapa binario (grid) actual
            pantalla_binaria = mundo.mapas_binarios[self.indice_mundo_x][self.indice_mundo_y]
            start = ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18)
            goal = ((jugador.rect_element.centerx // tile_size) % 32, (jugador.rect_element.centery // tile_size) % 18)

            # Si ya no tiene vida, se marca para eliminar
            if self.vida <= 0:
                self.eliminar = True

            self.arma.update(mundo, tank=jugador)

            distancia = self.distancia_jugador(jugador)

            # Si el jugador está dentro del rango de persecución, entramos en CHASING;
            # si se aleja demasiado, volvemos a patrullar (con un pequeño retardo para evitar bugs)
            if distancia < self.attack_range and raycasting(pantalla_binaria, start, goal):
                self.state = EnemyState.ATTACKING
            elif distancia < self.chase_range or self.jugador_visto:
                self.state = EnemyState.CHASING
                self.ultimo_cambio_estado = pygame.time.get_ticks()
                self.jugador_visto = True

            if self.state == EnemyState.PATROLLING:
                # Patrulla según el modo de patrulla definido
                if self.modo_patrulla == "circular":
                    if self.patrol_phase == 0:  # Derecha
                        dx, dy = self.velocidad, 0
                        if self.rect_element.x >= self.start_x + self.patrol_movement:
                            self.patrol_phase = 1
                    elif self.patrol_phase == 1:  # Abajo
                        dx, dy = 0, self.velocidad
                        if self.rect_element.y >= self.start_y + self.patrol_movement:
                            self.patrol_phase = 2
                    elif self.patrol_phase == 2:  # Izquierda
                        dx, dy = -self.velocidad, 0
                        if self.rect_element.x <= self.start_x:
                            self.patrol_phase = 3
                    elif self.patrol_phase == 3:  # Arriba
                        dx, dy = 0, -self.velocidad
                        if self.rect_element.y <= self.start_y:
                            self.patrol_phase = 0

                elif self.modo_patrulla == "horizontal":
                    dx, dy = self.velocidad * self.patrol_direction, 0
                    # Si choca o se sale del rango de patrulla, invierte la dirección
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

            elif self.state == EnemyState.CHASING:
                
                # Verifica primero la línea de visión: si la tiene, pasa a ATTACKING inmediatamente.
                if raycasting(pantalla_binaria, start, goal) and distancia < self.attack_range:
                    self.state = EnemyState.ATTACKING
                else:
                    # Si no hay visión, se calcula el camino y se mueve hacia el jugador.
                    if not self.path or self.path[-1] != goal:  # Recalcular si el jugador cambió de celda
                        self.path = astar(pantalla_binaria, start, goal)

                    if self.path:
                        next_step = self.path[0]
                        target_x = (self.indice_mundo_x * 32 + next_step[0]) * tile_size
                        target_y = (self.indice_mundo_y * 18 + next_step[1]) * tile_size

                        diff_x = target_x - self.rect_element.centerx
                        diff_y = target_y - self.rect_element.centery

                        factor = 0.707 if abs(diff_x) > 0 and abs(diff_y) > 0 else 1

                        dx = self.velocidad * factor if diff_x > 0 else -self.velocidad * factor if diff_x < 0 else 0
                        dy = self.velocidad * factor if diff_y > 0 else -self.velocidad * factor if diff_y < 0 else 0

                        self.actualizar_posicion(dx, dy, mundo)

                        # Cuando se alcanza la celda del path, se elimina ese paso.
                        if ((self.rect_element.centerx // tile_size) % 32, (self.rect_element.centery // tile_size) % 18) == (next_step[0], next_step[1]):
                            self.path.pop(0)

            elif self.state == EnemyState.ATTACKING:
                # En ATTACKING, si se pierde la visión, volver a CHASING y recalcular el camino
                if not raycasting(pantalla_binaria, start, goal):
                    self.state = EnemyState.CHASING
                    self.path = astar(pantalla_binaria, start, goal)
                else:
                    # print("Atacando")
                    if pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= 3000:
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
        self.jugador_visto = False

    def en_la_misma_pantalla(self, jugador):
        return (jugador.rect_element.x // TILE_SIZE // 32 == self.indice_mundo_x) and (jugador.rect_element.y // TILE_SIZE // 18 == self.indice_mundo_y)

       
    def dibujar_enemigo(self, mundo):
        self.dibujar(mundo)
        self.arma.dibujar_arma(mundo)

    def distancia_jugador(self, jugador):
        return math.hypot(jugador.rect_element.x - self.rect_element.x, jugador.rect_element.y - self.rect_element.y)
