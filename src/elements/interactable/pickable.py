from abc import ABC

from elements.interactable.interactable import Interactable
from extras.settings import CollisionLayer


class Pickable(ABC, Interactable):

    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, CollisionLayer.INTERACTUABLE)
        #poner los sprites del pickable

class PickableWeapon(Pickable):

    def __init__(self, x, y, weapon):
        self.weapon = weapon
        super().__init__(x, y, weapon.get_pickable_image())

    def interactuar(self, objeto):
        from tanks import Player
        if isinstance(objeto, Player) and self.check_collision(objeto):
            self.eliminar = True
            objeto.cambiar_secundaria(self.weapon)