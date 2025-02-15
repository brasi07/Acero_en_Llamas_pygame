import pygame
import math
import time

class Bala:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = math.radians(angulo)  # Convertir grados a radianes
        self.velocidad = 7  # Velocidad de la bala
        self.radio = 5  # Tamaño de la bala

        # Estado de la bala
        self.colisionando = False
        self.tiempo_colision = 0
        self.frame_actual = 0

        sprites_colision = [
            "../res/disparos/expl1.png",
            "../res/disparos/expl2.png",
            "../res/disparos/expl3.png",
            "../res/disparos/expl4.png",
            "../res/disparos/expl5.png",
            "../res/disparos/expl6.png",
            "../res/disparos/expl7.png",
            "../res/disparos/expl8.png",
            "../res/disparos/expl9.png",
            "../res/disparos/expl10.png"
        ]

        # Cargar sprites de la animación de colisión
        self.sprites_colision = [pygame.image.load(img) for img in sprites_colision]
        self.sprites_colision = [pygame.transform.scale(img, (20, 20)) for img in self.sprites_colision]

        # Rectángulo de la bala
        self.rect = pygame.Rect(self.x, self.y, self.radio * 2, self.radio * 2)

        # Velocidad en X e Y usando trigonometría
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        if self.colisionando:
            tiempo_transcurrido = time.time() - self.tiempo_colision
            self.frame_actual = int((tiempo_transcurrido / 1.0) * len(self.sprites_colision))  # Ajustar el frame

            if self.frame_actual >= len(self.sprites_colision):  # Si la animación terminó
                return True  # Eliminar la bala
            return False  # Mantener la animación

        # Mover la bala si no ha colisionado
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)

        # Verificar colisión con elementos
        for elemento in mundo.elementos:
            if self.rect.colliderect(elemento.rect_element) and elemento.colisiona:
                self.colisionando = True
                self.tiempo_colision = time.time()  # Guardar tiempo de colisión
                self.rect = self.sprites_colision[0].get_rect(center=self.rect.center)  # Ajustar el sprite
                return False  # No eliminar aún

        # Verificar si la bala sale de la pantalla
        if (self.x < mundo.camara_x or self.x > mundo.camara_x + ancho_pantalla or
                self.y < mundo.camara_y or self.y > mundo.camara_y + alto_pantalla):
            return True  # Eliminar la bala

        return False

    def draw(self, pantalla, mundo):
        if self.colisionando:
            pantalla.blit(self.sprites_colision[self.frame_actual],
                          (self.rect.x - mundo.camara_x, self.rect.y - mundo.camara_y))  # Dibujar animación
        else:
            pygame.draw.circle(pantalla, (30, 30, 30),
                               (self.rect.centerx - mundo.camara_x, self.rect.centery - mundo.camara_y), self.radio)  # Dibujar bala normal
