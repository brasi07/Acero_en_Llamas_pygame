import math
import pygame
from player import Player
from elements import Muro, Decoracion, Boton, Trampa, MuroBajo, Puerta
from enemy import Enemy
import settings
import csv
import os
import re  # Para extraer números del nombre del archivo

class World:
    def __init__(self, pantalla, mundo_number="1", player=None, hasSky=False):
        self.pantalla = pantalla
        self.player = player
        self.mundo_number = mundo_number  # Número del mundo actual
        self.hasSky = hasSky

        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()

        # Buscar archivos de mapa según el nuevo formato "Mapa_{mundo}_{capa}.csv"
        archivos_mapa = self.buscar_archivos_mapa(f"../res/mapas/Mapa_{self.mundo_number}_")

        # Diccionario para almacenar las capas
        self.capas = {}

        # Cargar los mapas desde los archivos CSV
        for archivo in archivos_mapa:
            capa_numero = self.extraer_numero_capa(archivo)  # Obtener número de capa desde el nombre
            self.capas[capa_numero] = self.cargar_mapa_desde_csv(archivo)

        # Obtener dimensiones del mapa en tiles
        self.num_filas = len(self.capas[1]) if 1 in self.capas else 0
        self.num_columnas = len(self.capas[1][0]) if self.num_filas > 0 else 0

        # Diccionario de sprites para cada capa
        self.sprites_por_capa = {}

        # Cargar dinámicamente los sprites según la capa
        for capa in self.capas.keys():
            carpeta_elementos = f"../res/elementos/elementos_{self.mundo_number}_{capa}"
            self.sprites_por_capa[capa] = self.cargar_sprites(carpeta_elementos)

        # Crear la cámara
        self.camara_x, self.camara_y = self.ancho_pantalla, self.alto_pantalla

        # Diccionario de elementos_1_2 para cada capa
        self.elementos_por_capa = {capa: [] for capa in self.capas.keys()}

        # Variables de transición
        self.en_transicion = False
        self.tiempo_inicio = 0
        self.destino_camara_x, self.destino_camara_y = 0,0

        self.puertas = {}

        # Generar los elementos_1_2 de cada capa
        for capa, tiles in self.capas.items():
            self.generar_elementos(tiles, self.elementos_por_capa[capa], self.sprites_por_capa[capa])

    def buscar_archivos_mapa(self, prefijo):
        """Busca archivos que coincidan con el patrón 'Mapa_{mundo}_{capa}.csv'."""
        carpeta = "../res/mapas"
        archivos = []
        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                if archivo.startswith(f"Mapa_{self.mundo_number}_") and archivo.endswith(".csv"):
                    archivos.append(os.path.join(carpeta, archivo))
        return archivos

    def extraer_numero_capa(self, archivo):
        """Extrae el número de capa desde el nombre del archivo 'Mapa_X_Y.csv'."""
        match = re.search(r'Mapa_\d+_(\d+)\.csv', archivo)
        return int(match.group(1)) if match else 1  # Si no encuentra número, asume capa 1

    def cargar_mapa_desde_csv(self, archivo):
        """Carga el mapa desde un archivo CSV y lo convierte en una lista de listas."""
        mapa = []
        try:
            with open(archivo, newline='') as csvfile:
                lector = csv.reader(csvfile)
                for fila in lector:
                    mapa.append([int(valor) for valor in fila])
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo}")
        return mapa

    def cargar_sprites(self, carpeta):
        """Carga todas las imágenes de la carpeta y las asocia por su ID."""
        sprites = {}
        if not os.path.exists(carpeta):
            print(f"Advertencia: La carpeta {carpeta} no existe.")
            return sprites  # Retorna un diccionario vacío si la carpeta no existe

        for archivo in os.listdir(carpeta):
            if archivo.endswith(".png"):
                id_sprite = archivo.split(".")[0]  # Obtiene el nombre sin la extensión
                sprites[int(id_sprite)] = pygame.image.load(os.path.join(carpeta, archivo))
        return sprites

    def generar_elementos(self, mapa_tiles, lista_elementos, sprites):
        """Crea los elementos del mapa ajustándolos al tamaño de la pantalla."""

        # Primer pase: Almacenar puertas
        for y, fila in enumerate(mapa_tiles):
            for x, valor in enumerate(fila):
                valor = int(valor)  # Asegurarse de que el valor es un número

                if 5100 <= valor <= 5199:  # Rango de valores reservados para puertas
                    puerta = Puerta(x * settings.TILE_SIZE, y * settings.TILE_SIZE, settings.TILE_SIZE, sprites.get(5100))
                    self.puertas[valor].append(puerta)  # Guardar la puerta con su ID único
                    lista_elementos.append(puerta)

        for y, fila in enumerate(mapa_tiles):
            for x, valor in enumerate(fila):

                valor = int(valor)  # Asegurarse de que el valor es un número
                if valor == 0:
                    self.camara_x = x // (self.ancho_pantalla / settings.TILE_SIZE) * self.ancho_pantalla
                    self.camara_y = y // (self.alto_pantalla / settings.TILE_SIZE) * self.alto_pantalla
                    self.player.establecer_posicion(x * settings.TILE_SIZE, y * settings.TILE_SIZE)
                    lista_elementos.append(self.player)
                elif 5000 <= valor <= 5099 and self.mundo_number == "1":  # Rango de valores reservados para botones
                    puerta_id = valor + 100  # Ejemplo: Botón 5000 activa puerta 5100
                    puertas_a_activar = self.puertas.get(puerta_id)
                    lista_elementos.append(Boton(x * settings.TILE_SIZE, y * settings.TILE_SIZE, sprites[valor], puertas_a_activar))
                elif valor == 836 and self.mundo_number == "1" \
                        or valor == 1425 and self.mundo_number == "2":
                    lista_elementos.append(Trampa(x * settings.TILE_SIZE, y * settings.TILE_SIZE, sprites[valor]))
                elif valor == 1168 and self.mundo_number == "1":
                    lista_elementos.append(MuroBajo(x * settings.TILE_SIZE, y * settings.TILE_SIZE, sprites[valor]))
                elif valor in (514, 515, 516, 517, 578, 579, 580, 581, 876, 878, 768, 2436, 2437, 2438, 2500, 2502, 2564, 2565, 2566) and self.mundo_number == "1" \
                        or valor in (1, 512, 513, 576, 577, 1360, 1361, 1362, 1424, 1426, 1488, 1489, 1490, 1486, 1550, 1614, 1678) and self.mundo_number == "2":
                    lista_elementos.append(Decoracion(x * settings.TILE_SIZE, y * settings.TILE_SIZE, sprites[valor]))
                elif valor != -1 and valor in sprites:
                    lista_elementos.append(Muro(x * settings.TILE_SIZE, y * settings.TILE_SIZE, sprites[valor]))

    def cambiar_pantalla(self, direccion):

        if not self.en_transicion:
            # Si no hay transición en curso, iniciar una
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo actual
            if direccion == "derecha" and self.camara_x + self.ancho_pantalla < self.num_columnas * self.ancho_pantalla:
                self.destino_camara_x = self.camara_x + self.ancho_pantalla
                self.destino_camara_y = self.camara_y
                self.en_transicion = True
            elif direccion == "izquierda" and self.camara_x > 0:
                self.destino_camara_x = self.camara_x - self.ancho_pantalla
                self.destino_camara_y = self.camara_y
                self.en_transicion = True
            elif direccion == "abajo" and self.camara_y + self.alto_pantalla < self.num_filas * self.alto_pantalla:
                self.destino_camara_x = self.camara_x
                self.destino_camara_y = self.camara_y + self.alto_pantalla
                self.en_transicion = True
            elif direccion == "arriba" and self.camara_y > 0:
                self.destino_camara_x = self.camara_x
                self.destino_camara_y = self.camara_y - self.alto_pantalla
                self.en_transicion = True

    def actualizar_transicion(self):
        """Actualiza la transición de la cámara."""
        if self.en_transicion:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
            duracion_transicion = 1000

            if tiempo_transcurrido < duracion_transicion:
                # Interpolación lineal
                t = tiempo_transcurrido / duracion_transicion
                self.camara_x = self.camara_x + (self.destino_camara_x - self.camara_x) * t
                self.camara_y = self.camara_y + (self.destino_camara_y - self.camara_y) * t
            else:
                # Una vez que se ha completado la transición
                self.camara_x = self.destino_camara_x
                self.camara_y = self.destino_camara_y
                self.en_transicion = False

    def elemento_en_pantalla(self, elemento):
        """Verifica si el elemento está dentro del área visible."""
        return (
                self.camara_x - 80 <= elemento.rect_element.x < self.camara_x + self.ancho_pantalla + 80
                and self.camara_y - 80 <= elemento.rect_element.y < self.camara_y + self.alto_pantalla + 80
        )

    def draw(self):
        """Dibuja todas las capas en orden, desde la más baja hasta la más alta."""
        for capa in sorted(self.capas.keys()):  # Dibuja en orden numérico
            if self.hasSky and max(self.capas.keys()) == capa:
                break

            for elemento in self.elementos_por_capa[capa]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(self)

        self.actualizar_transicion()

    def draw_sky(self):
        """Dibuja solo la última capa (capa más alta)."""
        capa_mas_alta = max(self.capas.keys())  # Encuentra la última capa
        for elemento in self.elementos_por_capa[capa_mas_alta]:
            if self.elemento_en_pantalla(elemento):
                elemento.dibujar(self)

