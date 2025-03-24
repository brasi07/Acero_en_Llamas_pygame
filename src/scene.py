from abc import ABC, abstractmethod


class Scene(ABC):

    def __init__(self, director):
        self.director = director

    @abstractmethod
    def update(self, *args):
        raise NotImplemented("no esta implementada la funcion")

    @abstractmethod
    def eventos(self, *args):
        raise NotImplemented("no esta implementada la funcion")

    @abstractmethod
    def dibujar(self, *args):
        raise NotImplemented("no esta implementada la funcion")

    def get_parametros(self):
        pass
