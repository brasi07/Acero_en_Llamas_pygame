from abc import ABC, abstractmethod

from elements.interactable.interactable import Interactable
from extras.settings import TILE_SIZE
from tanks import Player


class Pickable(ABC, Interactable):

    def __init__(self, x, y, sprite, layer):
        self.receiver = Player()
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, sprite, layer)
        #poner los sprites del pickable

    @abstractmethod
    def pick(self):
        del self

class PickableWeapon(Pickable):

    def __init__(self, x, y, layer, weapon):
        self.weapon = weapon
        super().__init__(x, y, weapon.imagen_accesorio, layer)

    def interactuar(self, objeto):
        if self.check_collision(objeto):
            self.pick()

    def pick(self):
        self.receiver.cambiar_secundaria(self.weapon)
        super().pick()