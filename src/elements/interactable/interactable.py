import abc
from ..element import Element
from ...extras import TILE_SIZE

class Interactable(Element):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, imagen, layer)

    @abc.abstractmethod
    def interactuar(self, objeto):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")







