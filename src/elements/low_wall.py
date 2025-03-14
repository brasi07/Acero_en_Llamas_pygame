from .element import Element
from ..extras.settings import TILE_SIZE, CollisionLayer

class LowWall(Element):
    def __init__(self, x, y, imagen):
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, imagen, CollisionLayer.LOW_WALL)