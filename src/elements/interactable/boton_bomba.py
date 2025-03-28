import pygame
from .interactable import Interactable
from ...extras import Settings, ResourceManager


class Button_Bomb(Interactable):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, Settings.CollisionLayer.INTERACTUABLE)
        self.camara_temporal_activa = False
        self.tiempo_activacion = 0
        self.tiempo_objetos = 0
        self.objetos_activados = False
        self.sprite = sprite
        self.objeto_colisionando = False

    def interactuar(self, objeto,mundo):
        """Solo activa el botón si el jugador NO estaba colisionando en el frame anterior."""
        if not self.camara_temporal_activa and self.check_collision(objeto) and not self.objeto_colisionando:
            self.presionar_boton(mundo)
            ResourceManager.play_sound("button_pressed.wav")
            self.objeto_colisionando = True

    def update(self, jugador):
        """Controla el tiempo de activación de la cámara y los objetos y gestiona la colisión."""

        if not self.check_collision(jugador):
            self.objeto_colisionando = False

    def presionar_boton(self,mundo):
        """Mueve la cámara y programa la activación de objetos después de 1 segundo."""
        mundo.bomba.fin=True
