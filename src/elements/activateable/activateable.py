import abc
from elements.element import Element
from extras.settings import TILE_SIZE

class Activateable(Element):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, imagen, layer)

    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")