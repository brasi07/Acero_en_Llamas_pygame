import abc
import pygame

from elements import Elemento
from settings import CollisionLayer


class Interactuable(Elemento):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x, y, imagen, layer)

    @abc.abstractmethod
    def activar(self, objeto):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")


class Boton(Interactuable):
    def __init__(self, x, y, sprite, objetos_a_activar, mundo):
        super().__init__(x, y, sprite, CollisionLayer.INTERACTUABLE)
        self.camara_temporal_activa = False
        self.tiempo_activacion = 0
        self.tiempo_objetos = 0
        self.objetos_activados = False
        self.x = x
        self.y = y
        self.sprite = sprite
        self.objetos_a_activar = objetos_a_activar
        self.mundo = mundo

        self.camara_x_original = self.mundo.camara_x
        self.camara_y_original = self.mundo.camara_y

        self.objeto_colisionando = False  # 🚀 Nueva bandera para controlar la colisión previa

    def activar(self, objeto):
        """Solo activa el botón si el jugador NO estaba colisionando en el frame anterior."""
        if not self.camara_temporal_activa and self.check_collision(objeto) and not self.objeto_colisionando:
            self.presionar_boton()
            self.objeto_colisionando = True  # 🚀 Marca que el jugador está colisionando

    def update(self, jugador):
        """Controla el tiempo de activación de la cámara y los objetos y gestiona la colisión."""
        if self.camara_temporal_activa:
            tiempo_actual = pygame.time.get_ticks()

            # ⚡ Activar los objetos después de 1 segundo
            if not self.objetos_activados and tiempo_actual - self.tiempo_objetos >= 1000:
                for objeto in self.objetos_a_activar:
                    objeto.activar()
                self.objetos_activados = True

            # ⏳ Restaurar la cámara después de 2 segundos
            if tiempo_actual - self.tiempo_activacion >= 2000:
                self.mundo.camara_x = self.camara_x_original
                self.mundo.camara_y = self.camara_y_original
                self.mundo.enfocando_objeto = False
                self.camara_temporal_activa = False

        # 🚀 Si el jugador deja de colisionar, permite volver a presionar el botón
        if not self.check_collision(jugador):
            self.objeto_colisionando = False

    def presionar_boton(self):
        """Mueve la cámara y programa la activación de objetos después de 1 segundo."""
        self.mundo.enfocando_objeto = True

        self.camara_x_original = self.mundo.camara_x
        self.camara_y_original = self.mundo.camara_y

        self.mundo.camara_x = self.objetos_a_activar[0].x - self.mundo.ancho_pantalla // 2
        self.mundo.camara_y = self.objetos_a_activar[0].y - self.mundo.alto_pantalla // 2

        self.tiempo_activacion = pygame.time.get_ticks()
        self.tiempo_objetos = self.tiempo_activacion
        self.objetos_activados = False

        self.camara_temporal_activa = True

class Trampa(Interactuable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)
        self.explotada=False

    def activar(self, objeto):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if not self.explotada and self.check_collision(objeto):
            self.explotar()

    def explotar(self):
        self.explotada = True
        print("¡Explosión!")
        # Aquí puedes agregar la logica de la explosion



