import pygame

class Muro:
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)  # Crea un rectángulo en las coordenadas (x, y) con el tamaño (ancho, alto)
        self.color = color

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)  # Dibuja el rectángulo (muro) en la pantalla
