from ..extras import NEGRO_TRANSLUCIDO, ResourceManager, EVENTO_BOSS_MUERTO
from .world import World

class World2(World):
    def __init__(self, alto_pantalla, ancho_pantalla):
        super().__init__(alto_pantalla, ancho_pantalla, 2)
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

        for capa, tiles in self.capas.items():
            self.generar_elementos(tiles, self.elementos_por_capa[capa], self.sprites_por_capa[capa], self.enemigos,
                                   self.elementos_actualizables, capa)

        self.mapas_binarios = self.generar_mapas_binarios()

    def manejar_evento_especifico(self, evento):
        from .world3 import World3
        if self.control.change_world(evento) or evento.type == EVENTO_BOSS_MUERTO:
            self.director.cambiar_escena(World3(self.alto_pantalla, self.ancho_pantalla))