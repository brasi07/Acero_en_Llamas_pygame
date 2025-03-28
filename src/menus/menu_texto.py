from ..extras import ResourceManager
from .elemento_gui import ElementoGUI
from ..extras.settings import Settings

class TextoMenu(ElementoGUI):
    def __init__(self, pantalla, texto, fonte, posicion):
        self.pantalla = pantalla
        self.font = fonte
        self.text = self.font.render(texto, True, Settings.NEGRO)
        self.rect = self.text.get_rect()
        self.establecerPosicion(posicion)

    def update(self):
        return
    
    def dibujar(self, pantalla):
        pantalla.blit(self.text,self.rect)
    
