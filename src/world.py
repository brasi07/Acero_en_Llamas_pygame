import pygame
import maps
from settings import Color
from elements import Muro, Palmera
import math

import pygame

class World:
    def __init__(self, nombre, pantalla):
        self.nombre = nombre
        self.pantalla = pantalla
        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()

        # Cargar el mapa y redimensionarlo
        self.mapa_original = pygame.image.load(f"../res/mapas/{nombre}.png")
        self.mapa = pygame.transform.scale(self.mapa_original, (self.ancho_pantalla, self.alto_pantalla))

        # Obtener dimensiones del mapa en tiles
        self.num_filas = len(maps.mapa_tiles)
        self.num_columnas = len(maps.mapa_tiles[0])

        # Calcular tamaño de cada tile dinámicamente
        self.tamaño_tile = math.gcd(self.ancho_pantalla, self.alto_pantalla)

        # Cargar imágenes de los sprites
        self.muro_imagen = pygame.image.load("../res/muros/wall1.png")

        # Ajustar tamaño de los sprites a los tamaños de los tiles
        self.muro_imagen = pygame.transform.scale(self.muro_imagen, (self.tamaño_tile, self.tamaño_tile))

        # Lista de elementos
        self.elementos = []
        self.generar_elementos()

    def generar_elementos(self):
        """Crea los elementos del mapa ajustándolos al tamaño de la pantalla."""
        for y, fila in enumerate(maps.mapa_tiles):
            for x, valor in enumerate(fila):
                if valor == "1":  # Muro
                    self.elementos.append(Muro(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile, self.tamaño_tile, (255, 255, 255), self.muro_imagen))
                elif valor == "2":  # Palmera
                    self.elementos.append(Palmera(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile, self.tamaño_tile, (0, 255, 0)))

    def update(self):
        pass

    def draw(self, pantalla):
        pantalla.blit(self.mapa, (0, 0))

        for elemento in self.elementos:
            elemento.dibujar(pantalla)  # Dibuja cada elemento en su nueva escala
