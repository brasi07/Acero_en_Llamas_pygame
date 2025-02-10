import pygame

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("res/enemigos/tanque_enemigo.png")
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass  # Aquí iría la IA de movimiento

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
