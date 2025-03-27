import pygame
from ..extras import Settings

class Element:
    def __init__(self, x, y, imagen=None, collision_layer=Settings.CollisionLayer.NONE):
        self.x = x
        self.y = y
        self.collision_layer = collision_layer  # Asigna la capa de colisión
        self.imagen = imagen
        self.eliminar = False

        # Si hay imagen, ajustamos el rectángulo y la máscara
        if self.imagen:
            self.rect_element = self.imagen.get_rect(topleft=(self.x, self.y))
            self.mask = pygame.mask.from_surface(self.imagen)
        else:
            self.rect_element = pygame.Rect(self.x, self.y, 0, 0)
            self.mask = None

        self.fila_pantalla, self.col_pantalla = self.obtener_pantalla_actual()
        self.fila_pantalla = max(0, min(self.fila_pantalla, 3))
        self.col_pantalla = max(0, min(self.col_pantalla, 2))


    def dibujar(self, pantalla, x, y):
        """Dibuja el elemento en la pantalla."""
        if self.imagen:
            pantalla.blit(self.imagen, (self.rect_element.x - x, self.rect_element.y - y))
        else:
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect_element)

    def animacion_elimninar(self):
        pass

    def obtener_pantalla_actual(self):
        """Calcula en qué pantalla está el jugador basado en su posición."""
        col_pantalla = int(self.rect_element.centerx // Settings.ANCHO)
        fila_pantalla = int(self.rect_element.centery // Settings.ALTO)

        return fila_pantalla, col_pantalla

    def check_collision(self, other_element):
        """Verifica colisión con otro elemento basado en la tabla de colisiones."""
        # Si las capas no pueden colisionar, retorna False
        if other_element.collision_layer not in Settings.COLLISION_RULES.get(self.collision_layer, set()) or other_element is self:
            return False

        # Verificar colisión por máscara si ambos tienen imagen
        if self.rect_element.colliderect(other_element.rect_element):
            offset_x = other_element.rect_element.x - self.rect_element.x
            offset_y = other_element.rect_element.y - self.rect_element.y

            if self.mask and other_element.mask:
                return bool(self.mask.overlap(other_element.mask, (offset_x, offset_y)))
            return True  # Si no hay máscaras, pero hay colisión de rectángulos
        return False