from pefile import fast_load

from ..extras import NEGRO_TRANSLUCIDO, ResourceManager, EVENTO_BOSS_MUERTO
from .world import World

class World3(World):
    def __init__(self, alto_pantalla, ancho_pantalla):
        super().__init__(alto_pantalla, ancho_pantalla, 3, "final_city.wav")
        world_number = 3
        self.hasSky = False
        self.traps = (-2, -2)
        self.lowWalls = (1410, 12, 13, 16, 679, 680)
        self.decorations = (1484, 2142)
        self.ice = ()

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
        from .world1 import World1
        if self.control.change_world(evento) or evento.type == EVENTO_BOSS_MUERTO:
            ResourceManager.stop_and_unload_wav(self.song_name)
            self.director.cambiar_escena(World1(self.alto_pantalla, self.ancho_pantalla))