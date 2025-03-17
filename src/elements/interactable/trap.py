from .interactable import Interactable
from ...extras import CollisionLayer

class Trap(Interactable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if self.check_collision(objeto) and not self.eliminar:
            self.deslizar(objeto)

    def deslizar(self, jugador):
        from ...tanks import Player
        #if isinstance(jugador, Player): #Si queremos solo jugador
        self.eliminar = True
        jugador.establecer_posicion(jugador.posx_change_screen, jugador.posy_change_screen)