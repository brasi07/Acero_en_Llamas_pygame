import pygame
from src.settings import Color
from src.wall import Muro

class World:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mapa = pygame.image.load("../res/img.png")
        #self.mapa = pygame.image.load(f"res/mapas/{nombre}.png")
        self.muro = Muro(300, 200, 100, 25, Color.BLANCO)  # Crear un muro en las coordenadas (300, 200) con tamaño (100x50)

    def update(self):
        pass

    def draw(self, pantalla):
        pantalla.blit(self.mapa, (0, 0))
        self.muro.dibujar(pantalla)  # Dibuja el muro en la pantalla
