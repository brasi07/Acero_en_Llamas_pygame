import pygame

class Weapon:
    def __init__(self, tipo):
        self.tipo = tipo
        self.imagen = pygame.image.load(f"res/armas/{tipo}.png")

    def use(self):
        print(f"Usando arma: {self.tipo}")
