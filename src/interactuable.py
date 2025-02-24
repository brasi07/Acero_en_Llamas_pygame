import abc
import pygame

from elements import Elemento
from settings import CollisionLayer


class Interactuable(Elemento):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x, y, imagen, layer)

    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")


class Boton(Interactuable):
    def __init__(self, x, y, sprite, objetos_a_activar, mundo):
        super().__init__(x,y,sprite,CollisionLayer.INTERACTUABLE)
        self.x = x
        self.y = y
        self.sprite = sprite
        self.objetos_a_activar = objetos_a_activar  # Elemento que activará el botón
        self.mundo = mundo

    def update(self, jugador):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador

        if self.check_collision(jugador):
            self.activar()

    def activar(self):
        camara_x_original = self.mundo.camara_x
        self.mundo.camara_x = self.objetos_a_activar[0].x

        for objeto in self.objetos_a_activar:
            objeto.activar()  # Llama al método activar de otro objeto


class Puerta(Interactuable):
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


