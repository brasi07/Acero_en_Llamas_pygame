import re  # Para extraer números del nombre del archivo
from abc import ABC, abstractmethod

import pygame
from extras import settings
from elements import Wall, LowWall, Decoracion, Button, Door, Trap
from extras.settings import EVENTO_JUGADOR_MUERTO
from menu import PauseMenu
from scene import Scene
from tanks.enemies import EnemyBrown, EnemyGreen, EnemyPurple, EnemyRed, Enemy
from tanks.enemies.bosses import Mecha, MegaCannon, WarTrain
from tanks.player import Player


class World(Scene, ABC):
    def __init__(self, alto_pantalla, ancho_pantalla, director, ui, controller, player):

        super().__init__(director)

        self.ui = ui
        self.control = controller
        self.ui.set_cursor()
        self.player = player

        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

        self.capas = {}
        self.sprites_por_capa = {}
        self.hasSky = False
        self.CONEXIONES = []
        self.num_filas = 0
        self.num_columnas = 0

        self.elementos_por_capa = {}
        self.elementos_actualizables = []
        self.enemigos = []

        # Variables de transición
        self.en_transicion = False
        self.enfocando_objeto = False
        self.tiempo_inicio = 0
        self.camara_x, self.camara_y = 0, 0
        self.destino_camara_x, self.destino_camara_y = 0,0

        self.minimap_active = False

        self.traps = ()
        self.lowWalls = ()
        self.decorations = ()

    @staticmethod
    def extraer_numero_capa(archivo):
        """Extrae el número de capa desde el nombre del archivo 'Mapa_X_Y.csv'."""
        match = re.search(r'Mapa_\d+_(\d+)\.csv', archivo)
        return int(match.group(1)) if match else 1  # Si no encuentra número, asume capa 1

    def get_parametros(self):
        return self.alto_pantalla, self.ancho_pantalla, self.director, self.ui, self.control, self.player

    def eventos(self, eventos):
        pass

    def generar_elementos(self, mapa_tiles, lista_elementos, sprites, lista_enemigos, lista_actualizables):
        """Crea los elementos del mapa ajustándolos al tamaño de la pantalla."""
        puertas = {}

        for y, fila in enumerate(mapa_tiles):
            for x, valor in enumerate(fila):

                valor = int(valor)  # Asegurarse de que el valor es un número
                elemento = None

                # Primer pase: Almacenar puertas
                if 5100 <= valor <= 5199:  # Rango de valores reservados para puertas
                    elemento = Door(x, y, sprites[1315], sprites[580])
                    pos = valor - 5100
                    if pos not in puertas:
                        puertas[pos] = []
                    puertas[pos].append(elemento)
                elif valor == 0:
                    self.camara_x = x // (self.ancho_pantalla / settings.TILE_SIZE) * self.ancho_pantalla
                    self.camara_y = y // (self.alto_pantalla / settings.TILE_SIZE) * self.alto_pantalla
                    self.player.establecer_posicion(x * settings.TILE_SIZE, y * settings.TILE_SIZE)
                    elemento = self.player
                elif 7000 <= valor <= 7009:
                    elemento = EnemyBrown(x, y, valor % 10)
                elif 7010 <= valor <= 7019:
                    elemento = EnemyGreen(x, y, valor % 10)
                elif 7020 <= valor <= 7029:
                    elemento = EnemyPurple(x, y, valor % 10)
                elif 7030 <= valor <= 7039:
                    elemento = EnemyRed(x, y, valor % 10)
                elif 7040 <= valor <= 7049:
                    elemento = Mecha(x, y, valor % 10)
                elif 7050 <= valor <= 7059:
                    elemento = MegaCannon(x, y, valor % 10)
                elif 7060 <= valor <= 7069:
                    elemento = WarTrain(x, y, valor % 10)
                elif 5000 <= valor <= 5099:  # Rango de valores reservados para botones
                    pos = valor - 5000
                    puertas_a_activar = puertas.get(pos)
                    elemento = Button(x, y, sprites[2142], puertas_a_activar, self)
                elif valor in self.traps:
                    elemento = Trap(x, y, sprites[valor])
                elif valor in self.lowWalls:
                    elemento = LowWall(x, y, sprites[valor])
                elif valor in self.decorations:
                    elemento = Decoracion(x, y, sprites[valor])
                elif valor != -1 and valor in sprites:
                    elemento = Wall(x, y, sprites[valor])

                if elemento:
                    lista_elementos.append(elemento)

                    if isinstance(elemento, Enemy):
                        lista_enemigos.append(elemento)
                    elif hasattr(elemento, "update") and not isinstance(elemento, Player):
                        lista_actualizables.append(elemento)

    def generar_mapas_binarios(self):
        """Genera mapas binarios donde haya 1s donde haya Muro/MuroBajo/Puerta y 0s en el resto, inflando obstáculos."""
        mapa_binario = [[0 for _ in range(self.num_columnas)] for _ in range(self.num_filas)]

        # Marcar obstáculos en la matriz
        for elemento in self.elementos_por_capa[2]:
            if isinstance(elemento, (Wall, LowWall, Door)):
                tile_x = elemento.x // settings.TILE_SIZE
                tile_y = elemento.y // settings.TILE_SIZE
                mapa_binario[tile_y][tile_x] = 1

        # Inflar obstáculos (doblando el grosor)
        inflado = [[valor for valor in fila] for fila in mapa_binario]  # Copia para modificar sin afectar la original
        for y in range(self.num_filas):
            for x in range(self.num_columnas):
                if mapa_binario[y][x] == 1:
                    # Inflar en un radio de 1 celda
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.num_filas and 0 <= nx < self.num_columnas:
                                inflado[ny][nx] = 1

        # Crear submatrices para cada grid de pantalla
        tiles_por_pantalla_x = self.ancho_pantalla // settings.TILE_SIZE
        tiles_por_pantalla_y = self.alto_pantalla // settings.TILE_SIZE
        matriz_mapas = [[None for _ in range(4)] for _ in range(3)]

        for i in range(3):
            for j in range(4):
                submatriz = []
                for y in range(tiles_por_pantalla_y):
                    fila = inflado[j * tiles_por_pantalla_y + y][i * tiles_por_pantalla_x:(i + 1) * tiles_por_pantalla_x]
                    submatriz.append(fila)
                matriz_mapas[i][j] = submatriz

        return matriz_mapas

    def cambiar_pantalla(self, direccion):

        dir_cam = {
            "derecha": (1, 0),
            "izquierda": (-1, 0),
            "abajo": (0, 1),
            "arriba": (0, -1)
        }

        for enemigo in self.enemigos:
            if enemigo.en_la_misma_pantalla(self.player):
                enemigo.patrullar()

        if not self.en_transicion and not self.enfocando_objeto:
            # Si no hay transición en curso, iniciar una
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo actual

            trans_x, trans_y = dir_cam[direccion]

            self.destino_camara_x = self.camara_x + trans_x*self.ancho_pantalla
            self.destino_camara_y = self.camara_y + trans_y*self.alto_pantalla

            self.en_transicion = True

    def actualizar_transicion(self):
        """Actualiza la transición de la cámara."""
        if not self.en_transicion:
            return

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
                self.camara_x - settings.TILE_SIZE <= elemento.rect_element.x < self.camara_x + self.ancho_pantalla + settings.TILE_SIZE
                and self.camara_y - settings.TILE_SIZE <= elemento.rect_element.y < self.camara_y + self.alto_pantalla + settings.TILE_SIZE
        )

    def eventos(self, eventos):
        """ Lógica común para todos los mundos """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
            elif evento.type == EVENTO_JUGADOR_MUERTO:
                self.director.reiniciar_escena()

            if self.control.pausar(evento):
                self.director.apilar_escena(PauseMenu(self.control, self.director))

            if self.control.change_weapon(evento):
                self.player.cambiar_arma_secundaria()

            if self.control.open_minimap(evento):
                self.minimap_active = not self.minimap_active

            self.manejar_evento_especifico(evento)

        self.player.eventos(self)

    def manejar_evento_especifico(self, evento):
        pass

    def update(self, time):

        self.player.update(self)

        """Actualiza el mundo y los elementos."""
        for elemento in self.enemigos:
            elemento.update(self.player, self)

        for elemento in self.elementos_actualizables:
            elemento.update(self.player)

        for lista in [self.enemigos, self.elementos_actualizables, self.elementos_por_capa[2]]:
            for elemento in lista.copy():
                if elemento.eliminar:
                    elemento.animacion_elimninar()
                    lista.remove(elemento)

    def dibujar(self, pantalla):
        self.draw(pantalla)

        for enemigo in self.enemigos:
            enemigo.dibujar_enemigo(pantalla, self.camara_x, self.camara_y)

        self.player.draw(pantalla, self.camara_x, self.camara_y)

        for enemigo in self.enemigos:
            enemigo.arma.dibujar_balas(pantalla, self.camara_x, self.camara_y)

        self.player.arma.dibujar_balas(pantalla, self.camara_x, self.camara_y)

        if self.hasSky:
            self.draw_sky(pantalla)

        for enemigo in self.enemigos:
            self.ui.draw_health_bar(enemigo, pantalla, self.camara_x, self.camara_y)

        self.ui.draw_health_bar_player(self.player, pantalla)
        if self.minimap_active:
            self.ui.dibujar_minimapa(self.player, self, pantalla)

    def draw(self, pantalla):
        """Dibuja todas las capas en orden, desde la más baja hasta la más alta."""
        for capa in sorted(self.capas.keys()):  # Dibuja en orden numérico
            if self.hasSky and max(self.capas.keys()) == capa:
                break

            for elemento in self.elementos_por_capa[capa]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        self.actualizar_transicion()

    def draw_sky(self, pantalla):
        """Dibuja solo la última capa (capa más alta)."""
        capa_mas_alta = max(self.capas.keys())  # Encuentra la última capa
        for elemento in self.elementos_por_capa[capa_mas_alta]:
            if self.elemento_en_pantalla(elemento):
                elemento.dibujar(pantalla, self.camara_x, self.camara_y)



