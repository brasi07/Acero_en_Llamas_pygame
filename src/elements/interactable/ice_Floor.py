from .interactable import Interactable
from ...extras import Settings

class IceFloor(Interactable):
    def __init__(self, x, y, imagen=None):
        super().__init__(x, y, imagen, Settings.CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto):
        from ...tanks import Player
        if self.check_collision(objeto) and isinstance(objeto, Player):
            objeto.deslizar=True
            objeto.contador_desliz=0