import pygame

from enemy import Enemy

class Boss(Enemy):
    def __init__(self, vida, velocidad, x, y, resizex, resizey):
        super().__init__(vida, velocidad, x, y, resizex, resizey, "")

class Mecha(Boss):
    def __init__(self, x, y, resizex, resizey):
        super().__init__(20, 2.5, x, y, resizex, resizey)