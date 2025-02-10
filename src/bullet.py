import pygame

class Bala:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.direccion = direccion  # Dirección en la que la bala se mueve
        self.velocidad = 5  # Velocidad de la bala
        self.radio = 5  # Tamaño de la bala

        # Establecer la dirección de la bala
        if direccion == "arriba":
            self.vel_y = -self.velocidad
            self.vel_x = 0
        elif direccion == "abajo":
            self.vel_y = self.velocidad
            self.vel_x = 0
        elif direccion == "izquierda":
            self.vel_x = -self.velocidad
            self.vel_y = 0
        elif direccion == "derecha":
            self.vel_x = self.velocidad
            self.vel_y = 0
        elif direccion == "arriba_izquierda":
            self.vel_x = -self.velocidad * 0.707
            self.vel_y = -self.velocidad * 0.707
        elif direccion == "arriba_derecha":
            self.vel_x = self.velocidad * 0.707
            self.vel_y = -self.velocidad * 0.707
        elif direccion == "abajo_izquierda":
            self.vel_x = -self.velocidad * 0.707
            self.vel_y = self.velocidad * 0.707
        elif direccion == "abajo_derecha":
            self.vel_x = self.velocidad * 0.707
            self.vel_y = self.velocidad * 0.707

        self.rect = pygame.Rect(self.x, self.y, self.radio * 2, self.radio * 2)

    def update(self):
        # Mueve la bala en función de su dirección
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)  # Actualiza la posición del rectángulo de la bala

    def draw(self, pantalla):
        pygame.draw.circle(pantalla, (255, 0, 0), (self.rect.centerx, self.rect.centery), self.radio)

    def fuera_de_pantalla(self, pantalla):
        # Si la bala se ha salido de la pantalla, la eliminamos
        return not pantalla.get_rect().colliderect(self.rect)
