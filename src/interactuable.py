import abc
import pygame

from elements import Elemento
from settings import CollisionLayer


class Interactuable(Elemento):
    @abc.abstractmethod
    def __init__(self, x, y, imagen,layer):
        super().__init__(x, y, imagen, layer)
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")


class Boton(Interactuable):
    def __init__(self, x, y, sprite, objeto_a_activar):
        super().__init__(x,y,sprite,CollisionLayer.INTERACTUABLE)
        self.x = x
        self.y = y
        self.sprite = sprite
        self.objeto_a_activar = objeto_a_activar  # Elemento que activará el botón


    def update(self, jugador):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if self.check_collision(jugador):
            self.activar()

    def activar(self):
        print("Botón presionado. Activando elemento...")
        self.objeto_a_activar.activar()  # Llama al método activar de otro objeto


class Puerta(Interactuable):
    def __init__(self, x, y, sprite_abierto, sprite_cerrado):
        super().__init__(x,y,sprite_abierto,CollisionLayer.WALL)
        self.x = x
        self.y = y
        self.abierta = False  # Estado inicial: cerrada
        self.sprite_abierto = sprite_abierto
        self.sprite_cerrado = sprite_cerrado

    def activar(self):
        self.abierta = not self.abierta  # Cambia el estado
        if self.abierta:
            self.imagen=self.sprite_abierto
        else:
            self.imagen=self.sprite_cerrado
        print(f"Puerta {'abierta' if self.abierta else 'cerrada'}.")


