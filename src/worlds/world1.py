from extras.resourcesmanager import ResourceManager
from extras.settings import ROJO_TRANSLUCIDO, NEGRO_TRANSLUCIDO, EVENTO_BOSS_MUERTO
from worlds.world import World

class World1(World):
    def __init__(self, alto_pantalla, ancho_pantalla, director):
        super().__init__(alto_pantalla, ancho_pantalla, director)
        world_number = 1
        self.hasSky = True
        self.traps = (836, -2)
        self.lowWalls = (1168, 1155, 1283, 1220, 1282, 1157, 1346, 1092, 1347)
        self.decorations = (514, 515, 516, 517, 578, 579, 580, 581, 876, 878, 768, 2436, 2437, 2438, 2500, 2502, 2564, 2565, 2566)

        self.CONEXIONES = [
            ((1, 1), (2, 1), ROJO_TRANSLUCIDO),
            ((0, 0), (0, 1), NEGRO_TRANSLUCIDO),  # Habitación (0,0) conecta con (0,1)
            ((0, 1), (0, 2), NEGRO_TRANSLUCIDO),
            ((0, 0), (1, 0), NEGRO_TRANSLUCIDO),
            ((1, 0), (2, 0), NEGRO_TRANSLUCIDO),
            ((2, 0), (3, 0), NEGRO_TRANSLUCIDO),
            ((0, 1), (0, 2), NEGRO_TRANSLUCIDO),
            ((0, 1), (1, 1), NEGRO_TRANSLUCIDO),
            ((1, 1), (1, 2), NEGRO_TRANSLUCIDO),
            ((1, 2), (2, 2), NEGRO_TRANSLUCIDO),
            ((2, 2), (3, 2), NEGRO_TRANSLUCIDO),
            ((3, 2), (3, 1), NEGRO_TRANSLUCIDO),
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
        from worlds.world2 import World2
        if self.control.change_world(evento) or evento.type == EVENTO_BOSS_MUERTO:
            self.director.cambiar_escena(World2(self.alto_pantalla, self.ancho_pantalla, self.director))
