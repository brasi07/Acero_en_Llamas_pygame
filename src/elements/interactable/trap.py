from .interactable import Interactable
from ...extras.settings import CollisionLayer
from ...tanks import Player


class Trap(Interactable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)
        self.explotada=False

    def interactuar(self, objeto):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if not self.explotada and self.check_collision(objeto):
            self.explotar(objeto)

    def explotar(self, jugador):
        if isinstance(jugador, Player):
            self.explotada = True
            jugador.recibir_dano(1)