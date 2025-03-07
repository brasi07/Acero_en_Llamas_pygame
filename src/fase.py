from abc import ABC, abstractmethod


class Escenario(ABC):

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("no esta implementada la funcion")

    def eventos(self, *args):
        raise NotImplemented("no esta implementada la funcion")

    def dibujar(self, *args):
        raise NotImplemented("no esta implementada la funcion")