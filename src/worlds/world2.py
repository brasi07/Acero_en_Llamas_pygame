import pygame

from extras.resourcesmanager import ResourceManager
from extras.settings import NEGRO_TRANSLUCIDO
from menu import PauseMenu
from worlds.world import World

class World2(World):
    def __init__(self, alto_pantalla, ancho_pantalla, director, ui, controller, player):
        super().__init__(alto_pantalla, ancho_pantalla, director, ui, controller, player)
        world_number = 2
        self.hasSky = True
        self.traps = (1425, -2)
        self.lowWalls = (16, 18, 20, 85, 86, 336, 338, 340, 466, 405, 406, 469, 470)
        self.decorations = (512, 513, 576, 577, 1360, 1361, 1362, 1424, 1426, 1488, 1489, 1490, 1486, 1550, 1614, 1678)

        self.CONEXIONES = [
            ((3, 0), (3, 1), NEGRO_TRANSLUCIDO),  # Habitación (0,0) conecta con (0,1)
            ((3, 1), (3, 2), NEGRO_TRANSLUCIDO),
            ((3, 2), (2, 2), NEGRO_TRANSLUCIDO),
            ((2, 2), (1, 2), NEGRO_TRANSLUCIDO),
            ((1, 2), (0, 2), NEGRO_TRANSLUCIDO),
            ((0, 2), (0, 1), NEGRO_TRANSLUCIDO),
            ((0, 1), (0, 0), NEGRO_TRANSLUCIDO),
            ((0, 0), (1, 0), NEGRO_TRANSLUCIDO),
            ((1, 0), (2, 0), NEGRO_TRANSLUCIDO),
            ((2, 0), (2, 1), NEGRO_TRANSLUCIDO),
            ((2, 1), (1, 1), NEGRO_TRANSLUCIDO),
        ]

        # Cargar los mapas desde los archivos CSV
        archivos_mapa = ResourceManager.buscar_archivos_mapa(world_number)
        for archivo in archivos_mapa:
            capa_numero = self.extraer_numero_capa(archivo)  # Obtener número de capa desde el nombre
            self.capas[capa_numero] = ResourceManager.load_map_from_csv(archivo)

        # Cargar dinámicamente los sprites según la capa
        for capa in self.capas.keys():
            carpeta_elementos = ResourceManager.locate_resource(f"elementos_{world_number}_{capa}")
            self.sprites_por_capa[capa] = ResourceManager.load_files_from_folder(carpeta_elementos)

        self.num_filas = len(self.capas[1]) if 1 in self.capas else 0
        self.num_columnas = len(self.capas[1][0]) if self.num_filas > 0 else 0
        self.elementos_por_capa = {capa: [] for capa in self.capas.keys()}

        for capa, tiles in self.capas.items():
            self.generar_elementos(tiles, self.elementos_por_capa[capa], self.sprites_por_capa[capa], self.enemigos,
                                   self.elementos_actualizables)

        self.mapas_binarios = self.generar_mapas_binarios()


    def manejar_evento_especifico(self, evento):
        from worlds.world1 import World1
        if self.control.change_world(evento):
            self.director.cambiar_escena(World1(self.alto_pantalla, self.ancho_pantalla, self.director, self.ui, self.control, self.player))