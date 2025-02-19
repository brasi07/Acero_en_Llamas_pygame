from enum import Enum

FPS = 60
ANCHO, ALTO = 1280, 720

TILE_SIZE = 32
RESIZE_PLAYER = 2

COOLDOWN = 2000

class CollisionLayer(Enum):
    PLAYER = 1
    ENEMY = 2
    BULLET_PLAYER = 3
    BULLET_ENEMY = 4
    WALL = 5
    LOW_WALL = 6
    NONE = 7  # Para elementos sin colisión

COLLISION_RULES = {
    CollisionLayer.PLAYER: {CollisionLayer.ENEMY, CollisionLayer.BULLET_ENEMY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.ENEMY: {CollisionLayer.PLAYER, CollisionLayer.BULLET_PLAYER, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.BULLET_PLAYER: {CollisionLayer.ENEMY, CollisionLayer.WALL},
    CollisionLayer.BULLET_ENEMY: {CollisionLayer.PLAYER, CollisionLayer.WALL},
    CollisionLayer.WALL: set(),
    CollisionLayer.LOW_WALL: set(),
    CollisionLayer.NONE: set()  # No colisiona con nada
}


class Color(Enum):
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    GRIS_OSCURO = (30, 30, 30)