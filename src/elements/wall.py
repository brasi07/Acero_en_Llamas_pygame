from .element import Element
from ..extras import Settings

class Wall(Element):
    def __init__(self, x, y, imagen):
        super().__init__(x * Settings.TILE_SIZE, y * Settings.TILE_SIZE, imagen, Settings.CollisionLayer.WALL)