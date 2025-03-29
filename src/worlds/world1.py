from ..elements import Wall
from ..extras import Settings, ResourceManager
from .world import World
from ..menus.menu import DialogoMenu

class World1(World):
    def __init__(self, alto_pantalla, ancho_pantalla):
        super().__init__(alto_pantalla, ancho_pantalla, 1, "jungle.wav")
        self.hasSky = True
        self.traps = (836, -2)
        self.lowWalls = (1168, 1155, 1283, 1220, 1282, 1157, 1346, 1092, 1347)
        self.decorations = (514, 515, 516, 517, 578, 579, 580, 581, 876, 878, 768, 2436, 2437, 2438, 2500, 2502, 2564, 2565, 2566)
        self.ice = ()
        self.world_number = 1
        self.CONEXIONES = [
            ((1, 1), (2, 1), Settings.ROJO_TRANSLUCIDO),
            ((0, 0), (0, 1), Settings.NEGRO_TRANSLUCIDO),  # Habitación (0,0) conecta con (0,1)
            ((0, 1), (0, 2), Settings.NEGRO_TRANSLUCIDO),
            ((0, 0), (1, 0), Settings.NEGRO_TRANSLUCIDO),
            ((1, 0), (2, 0), Settings.NEGRO_TRANSLUCIDO),
            ((2, 0), (3, 0), Settings.NEGRO_TRANSLUCIDO),
            ((0, 1), (0, 2), Settings.NEGRO_TRANSLUCIDO),
            ((0, 1), (1, 1), Settings.NEGRO_TRANSLUCIDO),
            ((1, 1), (1, 2), Settings.NEGRO_TRANSLUCIDO),
            ((1, 2), (2, 2), Settings.NEGRO_TRANSLUCIDO),
            ((2, 2), (3, 2), Settings.NEGRO_TRANSLUCIDO),
            ((3, 2), (3, 1), Settings.NEGRO_TRANSLUCIDO),
        ]

        for capa, tiles in self.capas.items():
            self.generar_elementos(tiles, self.elementos_por_capa[capa], self.sprites_por_capa[capa], self.enemigos,
                                   self.elementos_actualizables, capa)

        self.mapas_binarios = self.generar_mapas_binarios()

    def manejar_evento_especifico(self, evento):
        from .world2 import World2
        if  evento.type == Settings.EVENTO_BOSS_MUERTO: #or self.control.change_world(evento)  <-- Opcion de desarrollador
            self.player.improve()
            self.stop_music()
            self.director.cambiar_escena(DialogoMenu(self.director, "nieve", World2(self.alto_pantalla, self.ancho_pantalla), "intersection.wav"))