import pygame

from enemy import Enemy

class Boss(Enemy):
    def __init__(self, vida, velocidad, x, y, resizex, resizey):
        super().__init__(vida, velocidad, x, y, resizex, resizey, "")