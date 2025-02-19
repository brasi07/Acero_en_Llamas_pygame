import abc
import pygame

from elements import Elemento


class Interactuable:
    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")


class Boton(Interactuable, Elemento):
    def __init__(self, x, y, tamaño, sprite, objeto_a_activar):
        super().__init__()
        self.x = x
        self.y = y
        self.tamaño = tamaño
        self.sprite = sprite
        self.objeto_a_activar = objeto_a_activar  # Elemento que activará el botón
        self.rect_element = pygame.Rect(x, y, tamaño, tamaño)

    def activar(self):
        print("Botón presionado. Activando elemento...")
        self.objeto_a_activar.activar()  # Llama al método activar de otro objeto

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))


class Puerta(Interactuable, Elemento):
    def __init__(self, x, y, tamaño, sprite_abierto, sprite_cerrado):
        super().__init__()
        self.x = x
        self.y = y
        self.tamaño = tamaño
        self.abierta = False  # Estado inicial: cerrada
        self.sprite_abierto = sprite_abierto
        self.sprite_cerrado = sprite_cerrado
        self.rect_element = pygame.Rect(x, y, tamaño, tamaño)

    def activar(self):
        self.abierta = not self.abierta  # Cambia el estado
        print(f"Puerta {'abierta' if self.abierta else 'cerrada'}.")

    def dibujar(self, pantalla):
        sprite = self.sprite_abierto if self.abierta else self.sprite_cerrado
        pantalla.blit(sprite, (self.x, self.y))
