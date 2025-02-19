import settings
import numpy as np

from settings import CollisionLayer
from bullet import Bala
import weapon

import pygame

from tank import Tank


class Player(Tank):

    def __init__(self, x, y, tamaño_tile):

        self.velocidad_base = 3
        self.velocidad = self.velocidad_base

        # Llamamos al constructor de la clase base (Elemento)
        super().__init__(3, self.velocidad_base, x, y, tamaño_tile, CollisionLayer.PLAYER)

        # Equipamos armas
        self.armas_secundarias = [ None, weapon.Dash(), weapon.Escopeta()]  # Lista de las posibles armas
        self.arma_secundaria_pos = 0 #posicion en la lista de la arma secundaria actualmente equipada
        self.arma_secundaria = None # se inicia el juego sin ninguna arma secundaria equipada
        self.ultimo_uso_secundaria = pygame.time.get_ticks()
        self.sprite_arma_secundaria = None
        self.rect_secundaria = None

    def update(self, mundo):
        self.mover(mundo)
        self.gestionar_disparo()
        self.gestionar_arma_secundaria()
        if self.arma_secundaria != None:
            self.arma_secundaria.update(self)
        self.verificar_fuera_pantalla(mundo)

        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def mover(self, mundo):
        teclas = pygame.key.get_pressed()
        movimiento_x, movimiento_y = self.obtener_movimiento(teclas)
        self.actualizar_posicion(movimiento_x, movimiento_y, mundo)

    def obtener_movimiento(self, teclas):
        movimiento_x = (-self.velocidad if teclas[pygame.K_LEFT] or teclas[pygame.K_a] else 0) + \
                       (self.velocidad if teclas[pygame.K_RIGHT] or teclas[pygame.K_d] else 0)
        movimiento_y = (-self.velocidad if teclas[pygame.K_UP] or teclas[pygame.K_w] else 0) + \
                       (self.velocidad if teclas[pygame.K_DOWN] or teclas[pygame.K_s] else 0)
        if movimiento_x and movimiento_y:
            movimiento_x *= 0.707
            movimiento_y *= 0.707
        return movimiento_x, movimiento_y

    def verificar_fuera_pantalla(self, mundo):
        if self.rect_element.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif self.rect_element.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif self.rect_element.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif self.rect_element.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

    def gestionar_disparo(self):
        if pygame.mouse.get_pressed()[0]:
            if pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= 1000:
                self.disparar()
                self.tiempo_ultimo_disparo = pygame.time.get_ticks()

    def update_cannon_position(self, mundo):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        diff_x = cursorx - (self.rect_element.centerx - mundo.camara_x)
        diff_y = cursory - (self.rect_element.centery - mundo.camara_y)

        self.aim(diff_x, diff_y)

    def gestionar_arma_secundaria(self):
        if self.arma_secundaria != None:
            if pygame.mouse.get_pressed()[2]:
                self.use_special()

    def cambiar_arma_secundaria(self):
        if self.arma_secundaria_pos < (len(self.armas_secundarias) - 1):
            self.arma_secundaria_pos += 1
        else:
            self.arma_secundaria_pos = 0
        self.arma_secundaria = self.armas_secundarias[self.arma_secundaria_pos]
        if self.arma_secundaria != None:
            if self.arma_secundaria.tipo == "escopeta":
                self.sprite_cannon = pygame.transform.scale(self.arma_secundaria.imagen, (self.tamaño_tile * settings.RESIZE_PLAYER, self.tamaño_tile * settings.RESIZE_PLAYER))
                self.arma_secundaria.animacion = [pygame.transform.scale(self.arma_secundaria.animacion [i], (settings.RESIZE_PLAYER* self.tamaño_tile, settings.RESIZE_PLAYER * self.tamaño_tile))
                        for i in range(0, len(self.arma_secundaria.animacion ) - 1)]
                self.sprite_arma_secundaria = None
            else:
                self.sprite_arma_secundaria = self.escalar_y_cargar(self.arma_secundaria.imagen, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)
                self.sprite_cannon = self.sprites["canhon"]


    def dibujar_arma_secundaria(self, mundo):
        #aun hay que hacer con que el propulsor de dash estea correctamente alineado con el tanque
        if self.sprite_arma_secundaria != None: #dibujar arma secundaria si necesario
            self.rect_secundaria = self.sprite_arma_secundaria.get_rect(top=self.rect_element.bottom)
            mundo.pantalla.blit(self.sprite_arma_secundaria, (self.rect_element.centerx - self.rect_secundaria.width // 2 - mundo.camara_x, self.rect_element.centery - self.rect_secundaria.height // 2 - mundo.camara_y))
        

        

    def draw(self, mundo):
        for bala in self.balas:
            bala.draw(mundo.pantalla, mundo)
        self.dibujar(mundo.pantalla, mundo)
        self.update_cannon_position(mundo)
        if (self.arma_secundaria != None):
                self.dibujar_arma_secundaria(mundo)
        mundo.pantalla.blit(self.imagen_canon, (self.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))