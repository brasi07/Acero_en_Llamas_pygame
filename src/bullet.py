import pygame
import math
import time

import settings
from interactuable import Interactuable
from settings import CollisionLayer, COLLISION_RULES
from elements import Elemento


class Bala(Elemento):
    # Cargar sprites de colisión una sola vez (variable estática)
    sprites_colision = [pygame.transform.scale(pygame.image.load(f"../res/disparos/expl{i}.png"), (20, 20))
                        for i in range(1, 11)]

    def __init__(self, cannon_tip, angulo, tipoColision):
        self.imagen = self.escalar_y_cargar("../res/entidades/balas/bala.png", settings.RESIZE_PLAYER * 0.07, settings.RESIZE_PLAYER * 0.07)
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
                self.realizar_dano(elemento)
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

    def realizar_dano(self, elemento, dano=1):
        if hasattr(elemento, "vida"):
            elemento.recibir_dano(dano)
            return True
        return False

    def actualizar_colision(self):
        """Maneja la animación de colisión y decide si eliminar la bala."""
        tiempo_transcurrido = time.time() - self.tiempo_colision
        self.frame_actual = int((tiempo_transcurrido / 1.0) * len(self.sprites_colision))

        return self.frame_actual >= len(self.sprites_colision)  # Eliminar cuando la animación termine

    def fuera_de_pantalla(self, mundo, ancho_pantalla, alto_pantalla):
        """Verifica si la bala ha salido de la pantalla."""
        return (self.x < mundo.camara_x or self.x > mundo.camara_x + ancho_pantalla or
                self.y < mundo.camara_y or self.y > mundo.camara_y + alto_pantalla)

    def draw(self, mundo):
        """Dibuja la bala o su animación de colisión."""
        if self.colisionando:
            if self.frame_actual < len(self.sprites_colision):
                mundo.pantalla.blit(self.sprites_colision[self.frame_actual],
                              (self.rect_element.x - mundo.camara_x, self.rect_element.y - mundo.camara_y))
        else:
            self.dibujar(mundo)

class BalaRebote(Bala):

    def __init__(self, cannon_tip, angulo, tipoColision):
        super().__init__(cannon_tip, angulo, tipoColision)
        self.rebote_count = 0
        self.rebote_max = 2

    def iniciar_colision(self, elemento):
        if isinstance(elemento, Interactuable):
            elemento.activar(self)
        if self.rebote_count >= self.rebote_max:
            """Activa la animación de colisión y detiene el movimiento."""
            self.colisionando = True
            self.tiempo_colision = time.time()
            self.rect_element = self.sprites_colision[0].get_rect(center=self.rect_element.center)  # Centrar explosión
        else:
            if self.rebote_count == 0:
                self.collision_layer = CollisionLayer.BULLET_ANY

            self.rebote_count += 1

            overlap_x = min(self.rect_element.right - elemento.rect_element.left, 
                elemento.rect_element.right - self.rect_element.left) #calcula cuanto colisionan los rectangulos por la lateral

            overlap_y = min(self.rect_element.bottom - elemento.rect_element.top, 
                elemento.rect_element.bottom - self.rect_element.top) #calcula cuanto colisionan los rectangulos por arriba y abajo

            #decide cual velocidad cambiar basado en si la colisión es mayor por la lateral o por arriba/abajo
            if overlap_x < overlap_y:
                self.vel_x = -self.vel_x 
            else:
                self.vel_y = -self.vel_y 


    def check_collision(self, other_element):
        if not other_element.habilitado or other_element.collision_layer not in COLLISION_RULES.get(self.collision_layer, set()):
            return False

        # Comprobar si los rectángulos colisionan y devuelve el element colisionado
        return self.rect_element.colliderect(other_element.rect_element), other_element
    
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
            if self.check_collision(elemento) == (True, elemento):

                if self.realizar_dano(elemento):
                    self.rebote_count = self.rebote_max

                self.iniciar_colision(elemento)
                return False  # No eliminar aún, esperar animación

        # Verificar si la bala sale de la pantalla
        if self.fuera_de_pantalla(mundo, ancho_pantalla, alto_pantalla):
            return True  # Eliminar la bala

        return False
