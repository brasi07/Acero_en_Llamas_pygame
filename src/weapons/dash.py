import pygame
from extras import settings
from extras.resourcesmanager import ResourceManager
from weapons.weapon import Weapon

class Dash(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "dash"
        self.imagenes_accesorio_base = ResourceManager.load_sprites(settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, "dash")

        self.duracion_ms = 200  # Duración total del Dash en milisegundos
        self.tiempo_inicio = None
        self.activo = False

        self.velocidad_dash = 0.1  # Velocidad del Dash (píxeles por milisegundo)
        self.dx = 0
        self.dy = 0

    def activar_secundaria(self, tank, mundo):
        """Activa el Dash con desplazamiento en función del tiempo."""
        if not self.activo:
            self.activo = True
            self.tiempo_inicio = pygame.time.get_ticks()

            # Direcciones normalizadas para mantener velocidad constante en diagonales
            direcciones = {
                "arriba": (0, -1),
                "abajo": (0, 1),
                "izquierda": (-1, 0),
                "derecha": (1, 0),
                "arriba_izquierda": (-0.707, -0.707),
                "arriba_derecha": (0.707, -0.707),
                "abajo_izquierda": (-0.707, 0.707),
                "abajo_derecha": (0.707, 0.707),
            }

            # Obtener dirección normalizada del tanque
            direccion_normalizada = direcciones.get(tank.direccion, (0, 0))
            self.dx = direccion_normalizada[0] * self.velocidad_dash
            self.dy = direccion_normalizada[1] * self.velocidad_dash

    def update_secundaria(self, tank, mundo):
        """Mueve el tanque progresivamente basado en el tiempo transcurrido."""
        self.imagen_accesorio = self.imagenes_accesorio_base[tank.direccion]

        if self.activo:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio  # Milisegundos desde el inicio del Dash

            if tiempo_transcurrido < self.duracion_ms:
                movimiento_x = self.dx * tiempo_transcurrido
                movimiento_y = self.dy * tiempo_transcurrido
                tank.actualizar_posicion(movimiento_x, movimiento_y, mundo)
            else:
                self.activo = False  # Finaliza el Dash