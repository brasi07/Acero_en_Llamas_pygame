import pygame

class Elemento:
    def __init__(self, x, y, ancho, alto, color=None, imagen=None):
        self.rect = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo
        self.color = color  # Color del elemento
        self.imagen = imagen  # Imagen (puede ser None si no se usa imagen)

    def dibujar(self, pantalla):
        if self.imagen:  # Si tiene imagen, dibujamos la imagen
            pantalla.blit(self.imagen, (self.rect.x, self.rect.y))
        else:  # Si no tiene imagen, dibujamos el rectángulo
            pygame.draw.rect(pantalla, self.color, self.rect)


class Muro(Elemento):
    def __init__(self, x, y, ancho, alto, color, imagen):
        super().__init__(x, y, ancho, alto, color, imagen)  # Llama al constructor de la clase padre


class Palmera(Elemento):
    def __init__(self, x, y, ancho, alto, color, imagen=None):
        super().__init__(x, y, ancho, alto, color, imagen)  # Llama al constructor de la clase padre


