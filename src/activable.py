from elements import Elemento
from settings import CollisionLayer
import abc


class Activable(Elemento):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x, y, imagen, layer)

    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")

class Puerta(Activable):
    def __init__(self, x, y, sprite_cerrado, sprite_abierto):
        super().__init__(x,y,sprite_cerrado,CollisionLayer.WALL)
        self.x = x
        self.y = y
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