import pygame
from .interactable import Interactable
from ...extras import Settings, ResourceManager


class Button(Interactable):
    def __init__(self, x, y, sprite, objetos_a_activar, mundo):
        super().__init__(x, y, sprite, Settings.CollisionLayer.INTERACTUABLE)
        self.camara_temporal_activa = False
        self.tiempo_activacion = 0
        self.tiempo_objetos = 0
        self.objetos_activados = False
        self.sprite = sprite
        self.objetos_a_activar = objetos_a_activar
        self.mundo = mundo

        self.camara_x_original = self.mundo.camara_x
        self.camara_y_original = self.mundo.camara_y

        self.objeto_colisionando = False

    def interactuar(self, objeto,mundo):
        """Solo activa el botón si el jugador NO estaba colisionando en el frame anterior."""
        if not self.camara_temporal_activa and self.check_collision(objeto) and not self.objeto_colisionando:
            self.presionar_boton()
            ResourceManager.play_sound("button_pressed.wav")
            self.objeto_colisionando = True

    def update(self, jugador):
        """Controla el tiempo de activación de la cámara y los objetos y gestiona la colisión."""
        if self.camara_temporal_activa:
            tiempo_actual = pygame.time.get_ticks()

            if not self.objetos_activados and tiempo_actual - self.tiempo_objetos >= 1000:
                for objeto in self.objetos_a_activar:
                    objeto.activar()
                self.objetos_activados = True

            if tiempo_actual - self.tiempo_activacion >= 2000:
                self.mundo.camara_x = self.camara_x_original
                self.mundo.camara_y = self.camara_y_original
                self.mundo.enfocando_objeto = False
                self.camara_temporal_activa = False

        if not self.check_collision(jugador):
            self.objeto_colisionando = False

    def presionar_boton(self):
        """Mueve la cámara y programa la activación de objetos después de 1 segundo."""
        self.mundo.enfocando_objeto = True

        self.camara_x_original = self.mundo.camara_x
        self.camara_y_original = self.mundo.camara_y

        # Tamaño total del mundo en píxeles
        ancho_total = self.mundo.num_columnas * Settings.TILE_SIZE
        alto_total = self.mundo.num_filas * Settings.TILE_SIZE

        # Calcular la nueva posición centrada en el objeto
        nueva_x = self.objetos_a_activar[0].x + Settings.TILE_SIZE - self.mundo.ancho_pantalla // 2
        nueva_y = self.objetos_a_activar[0].y - self.mundo.alto_pantalla // 2

        # Limitar dentro de los márgenes del mundo
        self.mundo.camara_x = max(0, min(nueva_x, ancho_total - self.mundo.ancho_pantalla))
        self.mundo.camara_y = max(0, min(nueva_y, alto_total - self.mundo.alto_pantalla))

        self.tiempo_activacion = pygame.time.get_ticks()
        self.tiempo_objetos = self.tiempo_activacion
        self.objetos_activados = False

        self.camara_temporal_activa = True