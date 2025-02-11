import pygame

class Elemento:
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo
        self.color = color  # Color del elemento

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)  # Dibuja el rectángulo


class Muro(Elemento):
    def __init__(self, x, y, ancho, alto, color):
        super().__init__(x, y, ancho, alto, color)  # Llama al constructor de la clase padre


class Palmera(Elemento):
    def __init__(self, x, y, ancho, alto, color):
        super().__init__(x, y, ancho, alto, color)  # Llama al constructor de la clase padre


