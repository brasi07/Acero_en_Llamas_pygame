import pygame
import math

class Bala:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = math.radians(angulo)  # Convertir grados a radianes
        self.velocidad = 7  # Ajusta la velocidad de la bala
        self.radio = 5  # Tamaño de la bala

        # Calcular velocidad en X e Y usando seno y coseno
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad

        # Definir el rectángulo de la bala
        self.rect = pygame.Rect(self.x, self.y, self.radio * 2, self.radio * 2)

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        # Mueve la bala en la dirección del ángulo calculado
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)


        # Verificar colisión con elementos
        for elemento in mundo.elementos:
            if self.rect.colliderect(elemento.rect_element):
                return True  # Indica que la bala debe ser eliminada

        # Verificar si la bala está fuera de la pantalla
        if (self.x < 0 or self.x > ancho_pantalla + mundo.camara_x or
                self.y < 0 or self.y > alto_pantalla + mundo.camara_y):
            return True  # Eliminar la bala

        return False

    def draw(self, pantalla, mundo):
        pygame.draw.circle(pantalla, (255, 0, 0),
            (self.rect.centerx - mundo.camara_x, self.rect.centery - mundo.camara_y), self.radio)


