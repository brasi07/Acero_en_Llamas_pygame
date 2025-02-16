import math
import pygame
import settings


class Elemento:
    def __init__(self, x, y, colisiona, imagen=None):
        self.x = x
        self.y = y
        self.colisiona = colisiona
        self.imagen = imagen

        # Si hay imagen, ajustamos el rectángulo y la máscara
        if self.imagen:
            self.rect_element = self.imagen.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.imagen)  # Crear la máscara para la imagen
        else:
            self.rect_element = pygame.Rect(x, y, 0, 0)
            self.mask = None  # No hay máscara si no hay imagen

    def dibujar(self, pantalla, mundo):
        if self.imagen:  # Si tiene imagen, dibujamos la imagen
            pantalla.blit(self.imagen, (self.rect_element.x - mundo.camara_x, self.rect_element.y - mundo.camara_y))
        else:
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect_element)

    def check_collision(self, other_element):
        if not other_element.colisiona or self is other_element: return False

        # Comprobar si el rectángulo de colisión se solapa
        if self.rect_element.colliderect(other_element.rect_element):
            offset_x = other_element.rect_element.x - self.rect_element.x
            offset_y = other_element.rect_element.y - self.rect_element.y

            # Verificar si la máscara de la imagen tiene un valor distinto de 0
            if self.mask and other_element.mask:
                if self.mask.overlap(other_element.mask, (offset_x, offset_y)):
                    return True
        return False


class Boton(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, False, imagen)

class Muro(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, True, imagen)

class Vacio(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, False, imagen)

class Trampa(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, False, imagen)

class Arbol(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, True, imagen)


class Arbusto(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, False, imagen)

