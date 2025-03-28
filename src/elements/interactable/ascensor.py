from .interactable import Interactable
from ...extras import Settings

class Ascensor(Interactable):
    def __init__(self, x, y, imagen=None):
        super().__init__(x, y, imagen, Settings.CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto,mundo):
        from ...tanks import Player

        if self.check_collision(objeto) and isinstance(objeto, Player):
            if objeto.y>10:
                objeto.x=0
                objeto.y=0
                mundo.destino_camara_x = 0
                mundo.destino_camara_y = 0

            else:
                objeto.x = 0
                objeto.y = 0
                mundo.destino_camara_x = 0
                mundo.destino_camara_y = 0