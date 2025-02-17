import math
import pygame
import settings
import numpy
from elements import Elemento
from bullet import Bala

import pygame
import math
import numpy

class Player(Elemento):
    def __init__(self, x, y, tamaño_tile):
        self.tamaño_tile = tamaño_tile

        # Cargar una única imagen base
        self.sprite_base = self.escalar_y_cargar("../res/tanques/body_tracks.png", settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)
        self.sprite_base_45 = self.escalar_y_cargar("../res/tanques/body_tracks_45.png", settings.RESIZE_PLAYER, settings.RESIZE_PLAYER)



        # Crear un diccionario con todas las rotaciones necesarias
        self.sprites = self.generar_sprites()

        # Llamamos al constructor de la clase base (Elemento)
        super().__init__(x, y,True, self.sprites["abajo"])

        # Inicializamos los atributos específicos del jugador
        self.sprite_cannon = self.sprites["canhon"]
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -0)  # Cañón sin rotar inicialmente
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

        self.velocidad = 3
        self.direccion = "abajo"  # Dirección inicial del tanque
        self.balas = []  # Lista para almacenar las balas disparadas
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Tiempo del último disparo
        self.angulo_cannon = 0  # Ángulo del cañón

    def escalar_y_cargar(self, ruta, resizex, resizey):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (self.tamaño_tile * resizex, self.tamaño_tile * resizey))

    def rotar_y_centrar(imagen, angulo, rect_original):
        """Rota una imagen y mantiene su centro respecto al rect actual."""
        imagen_rotada = pygame.transform.rotate(imagen, angulo)
        rect_rotado = imagen_rotada.get_rect(center=rect_original.center)
        return imagen_rotada, rect_rotado

    def generar_sprites(self):
        """Genera todas las rotaciones a partir de la imagen base mirando a la derecha."""
        sprites = {
            "arriba": self.sprite_base,  # Imagen base
            "derecha": pygame.transform.rotate(self.sprite_base, -90),
            "izquierda": pygame.transform.rotate(self.sprite_base, 90),
            "abajo": pygame.transform.rotate(self.sprite_base, 180),
            "arriba_izquierda": self.sprite_base_45,
            "arriba_derecha": pygame.transform.rotate(self.sprite_base_45, -90),
            "abajo_izquierda": pygame.transform.rotate(self.sprite_base_45, 90),
            "abajo_derecha": pygame.transform.rotate(self.sprite_base_45, 180),
            "canhon": self.escalar_y_cargar("../res/tanques/tanque_canon.png", settings.RESIZE_PLAYER,settings.RESIZE_PLAYER)
        }
        return sprites

    def update(self, mundo):
        teclas = pygame.key.get_pressed()
        direccion = None

        # Movimiento en X e Y por separado
        movimiento_x = 0
        movimiento_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimiento_x = -self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimiento_x = self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            movimiento_y = -self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            movimiento_y = self.velocidad

        # Movimiento en diagonal (se reduce velocidad)
        if movimiento_x != 0 and movimiento_y != 0:
            movimiento_x *= 0.707  # √2/2 para mantener velocidad uniforme
            movimiento_y *= 0.707

        # --- Verificar colisiones usando check_collision ---
        colision_x = False
        colision_y = False

        # 1. Mover en X y verificar colisión
        self.rect_element.x += movimiento_x
        if any(self.check_collision(elemento) for elemento in mundo.elementos_por_capa[2]):
            self.rect_element.x -= movimiento_x  # Si hay colisión, deshacer movimiento en X
            colision_x = True

        # 2. Mover en Y y verificar colisión
        self.rect_element.y += movimiento_y
        if any(self.check_collision(elemento) for elemento in mundo.elementos_por_capa[2]):
            self.rect_element.y -= movimiento_y  # Si hay colisión, deshacer movimiento en Y
            colision_y = True

        # Verificar si el jugador sale de la pantalla y cambiar la cámara
        if self.rect_element.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif self.rect_element.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif self.rect_element.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif self.rect_element.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

        # --- Determinar la dirección final según los movimientos permitidos ---
        if movimiento_x < 0 > movimiento_y and not colision_x and not colision_y:
            direccion = "arriba_izquierda"
        elif movimiento_x > 0 > movimiento_y and not colision_x and not colision_y:
            direccion = "arriba_derecha"
        elif movimiento_x < 0 < movimiento_y and not colision_x and not colision_y:
            direccion = "abajo_izquierda"
        elif movimiento_x > 0 < movimiento_y and not colision_x and not colision_y:
            direccion = "abajo_derecha"
        elif movimiento_x < 0 and not colision_x:
            direccion = "izquierda"
        elif movimiento_x > 0 and not colision_x:
            direccion = "derecha"
        elif movimiento_y < 0 and not colision_y:
            direccion = "arriba"
        elif movimiento_y > 0 and not colision_y:
            direccion = "abajo"

        # Aplicar el movimiento final
        if direccion:
            self.direccion = direccion  # Actualizar la dirección del tanque
            self.imagen = self.sprites[direccion]

        # Disparo del tanque
        if pygame.mouse.get_pressed()[0]:  # 0 es el botón izquierdo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_disparo >= 1000:  # 1 segundo entre disparos
                self.disparar()
                self.tiempo_ultimo_disparo = tiempo_actual  # Actualiza el tiempo del último disparo

        # Actualizar las balas
        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def update_cannon_position(self, mundo):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        diff_x = cursorx - (self.rect_element.centerx - mundo.camara_x)
        diff_y = cursory - (self.rect_element.centery - mundo.camara_y)

        # Calcular el ángulo del cañón
        self.angulo_cannon = numpy.degrees(numpy.arctan2(diff_y, diff_x))  # Guardar el ángulo para disparos

        # Rotar la imagen del cañón
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -self.angulo_cannon - 90)

        # Mantener el cañón centrado en el tanque
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_element.center)

    def disparar(self):
        # Crear una nueva bala en la posición del cañón con el ángulo del cañón
        imagen = pygame.image.load("../res/tanques/bala.png")
        imagen = pygame.transform.scale(imagen,(self.tamaño_tile * 0.15, self.tamaño_tile * 0.15))
        nueva_bala = Bala(self.rect_canon.centerx, self.rect_canon.centery, self.angulo_cannon, imagen, "player")
        self.balas.append(nueva_bala)


    def draw(self, mundo):

        # Dibujar las balas
        for bala in self.balas:
            bala.draw(mundo.pantalla, mundo)

        # Dibujar tanque
        self.dibujar(mundo.pantalla, mundo)
        self.update_cannon_position(mundo)

        mundo.pantalla.blit(self.imagen_canon, (self.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))

        #Mostrar la Hitbox
        #pygame.draw.rect(pantalla, (255, 0, 0), (self.hitbox.x - mundo.camara_x, self.hitbox.y - mundo.camara_y, self.hitbox.width, self.hitbox.height), 2)
