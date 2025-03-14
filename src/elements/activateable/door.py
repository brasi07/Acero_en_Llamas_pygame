from .activateable import Activateable
from ...extras import CollisionLayer

class Door(Activateable):
    def __init__(self, x, y, sprite_cerrado, sprite_abierto):
        super().__init__(x,y,sprite_cerrado,CollisionLayer.WALL)
        self.abierta = False  # Estado inicial: cerrada
        self.sprite_abierto = sprite_abierto
        self.sprite_cerrado = sprite_cerrado

    def activar(self):
        self.abierta = not self.abierta  # Cambia el estado
        if self.abierta:
            self.collision_layer = CollisionLayer.NONE
            self.imagen=self.sprite_abierto
        else:
            self.collision_layer = CollisionLayer.WALL
            self.imagen=self.sprite_cerrado