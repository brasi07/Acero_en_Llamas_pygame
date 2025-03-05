from elements.interactable.interactable import Interactable
from extras.settings import CollisionLayer

class Trap(Interactable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)
        self.explotada=False

    def interactuar(self, objeto):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if not self.explotada and self.check_collision(objeto):
            self.explotar()

    def explotar(self):
        self.explotada = True
        print("¡Explosión!")
        # Aquí puedes agregar la logica de la explosion