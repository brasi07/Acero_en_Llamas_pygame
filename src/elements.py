import pygame

class Elemento:
    def __init__(self, x, y, ancho, alto, color=None, imagen=None):
        self.rect = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo
        self.color = color  # Color del elemento
        self.imagen = imagen  # Imagen (puede ser None si no se usa imagen)

    def dibujar(self, pantalla, camera_x, camera_y):
        if self.imagen:  # Si tiene imagen, dibujamos la imagen
            pantalla.blit(self.imagen, (self.rect.x - camera_x, self.rect.y - camera_y))
        else:  # Si no tiene imagen, dibujamos el rectángulo
            pygame.draw.rect(pantalla, self.color,(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))


class Muro(Elemento):
    def __init__(self, x, y, ancho, alto, color, imagen):
        super().__init__(x, y, ancho, alto, color, imagen)  # Llama al constructor de la clase padre


class Palmera(Elemento):
    def __init__(self, x, y, ancho, alto, color, imagen=None):
        super().__init__(x, y, ancho, alto, color, imagen)  # Llama al constructor de la clase padre


