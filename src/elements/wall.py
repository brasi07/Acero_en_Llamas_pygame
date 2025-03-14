from .element import Element
from ..extras.settings import TILE_SIZE, CollisionLayer

class Wall(Element):
    def __init__(self, x, y, imagen):
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, imagen, CollisionLayer.WALL)