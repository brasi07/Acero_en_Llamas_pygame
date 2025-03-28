from .interactable import Interactable
from ...extras import Settings

class Ascensor(Interactable):
    def __init__(self, x, y, imagen=None):
        super().__init__(x, y, imagen, Settings.CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto,mundo):
        from ...tanks import Player
        if self.check_collision(objeto):
            if self.check_collision(objeto) and isinstance(objeto, Player):
                if objeto.fila_pantalla==2:
                    objeto.rect_element.x=Settings.ANCHO*2.77
                    objeto.rect_element.y=objeto.rect_element.y-Settings.ALTO
                    mundo.destino_camara_y = mundo.destino_camara_y - Settings.ALTO

                else:
                    objeto.rect_element.x=Settings.ANCHO*2.77
                    objeto.rect_element.y = objeto.rect_element.y + Settings.ALTO
                    mundo.destino_camara_y = mundo.destino_camara_y + Settings.ALTO
