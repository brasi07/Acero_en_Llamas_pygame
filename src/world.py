import pygame

class World:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mapa = pygame.image.load("../res/img.png")
        #self.mapa = pygame.image.load(f"res/mapas/{nombre}.png")
        self.muro = pygame.Rect(100, 100, 100, 25)

    def update(self):
        pass

    def draw(self, pantalla):
        pantalla.blit(self.mapa, (0, 0))
