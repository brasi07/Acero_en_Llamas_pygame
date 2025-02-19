import pygame
import math
import time
from settings import CollisionLayer, COLLISION_RULES
from elements import Elemento



class Bala(Elemento):
    # Cargar sprites de colisión una sola vez (variable estática)
    sprites_colision = [pygame.transform.scale(pygame.image.load(f"../res/disparos/expl{i}.png"), (20, 20))
                        for i in range(1, 11)]

    def __init__(self, cannon_tip, angulo, tamaño_tile, tipoColision):
        self.tamaño_tile = tamaño_tile
        self.imagen = self.escalar_y_cargar("../res/entidades/balas/bala.png", 0.15, 0.15)
        self.x, self.y = cannon_tip

        super().__init__(self.x, self.y, self.imagen, tipoColision)

        # Convertir ángulo a radianes y calcular velocidad
        self.angulo = math.radians(angulo)
        self.velocidad = 7
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad

        # Estado de la bala
        self.colisionando = False
        self.tiempo_colision = 0
        self.frame_actual = 0

    def escalar_y_cargar(self, ruta, resizex, resizey):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (resizex * self.tamaño_tile, resizey * self.tamaño_tile))

    def check_collision(self, other_element):

        if other_element.collision_layer not in COLLISION_RULES.get(self.collision_layer, set()):
            return False

        # Comprobar si los rectángulos colisionan
        return self.rect_element.colliderect(other_element.rect_element)

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""
        if self.colisionando:
            return self.actualizar_colision()

        # Mover la bala
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect_element.topleft = (self.x, self.y)

        # Verificar colisiones con los elementos del mundo
        for elemento in mundo.elementos_por_capa.get(2, []):  # Evita KeyError si la capa no existe
            if self.check_collision(elemento):
                self.iniciar_colision()
                return False  # No eliminar aún, esperar animación

        # Verificar si la bala sale de la pantalla
        if self.fuera_de_pantalla(mundo, ancho_pantalla, alto_pantalla):
            return True  # Eliminar la bala

        return False

    def iniciar_colision(self):
        """Activa la animación de colisión y detiene el movimiento."""
        self.colisionando = True
        self.tiempo_colision = time.time()
        self.rect_element = self.sprites_colision[0].get_rect(center=self.rect_element.center)  # Centrar explosión

    def actualizar_colision(self):
        """Maneja la animación de colisión y decide si eliminar la bala."""
        tiempo_transcurrido = time.time() - self.tiempo_colision
        self.frame_actual = int((tiempo_transcurrido / 1.0) * len(self.sprites_colision))

        return self.frame_actual >= len(self.sprites_colision)  # Eliminar cuando la animación termine

    def fuera_de_pantalla(self, mundo, ancho_pantalla, alto_pantalla):
        """Verifica si la bala ha salido de la pantalla."""
        return (self.x < mundo.camara_x or self.x > mundo.camara_x + ancho_pantalla or
                self.y < mundo.camara_y or self.y > mundo.camara_y + alto_pantalla)

    def draw(self, pantalla, mundo):
        """Dibuja la bala o su animación de colisión."""
        if self.colisionando:
            if self.frame_actual < len(self.sprites_colision):
                pantalla.blit(self.sprites_colision[self.frame_actual],
                              (self.rect_element.x - mundo.camara_x, self.rect_element.y - mundo.camara_y))
        else:
            self.dibujar(pantalla, mundo)
