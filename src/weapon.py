import pygame
import abc

class Weapon(abc.ABC):  # Clase base abstracta para armas
    def __init__(self, tipo):
        self.tipo = tipo

    @abc.abstractmethod
    def activar(self, jugador):
        """Método abstracto que todas las armas deben implementar"""
        pass

    @abc.abstractmethod
    def update(self, jugador):
        """Método abstracto que todas las armas deben implementar"""
        pass

class Dash(Weapon):
    def __init__(self):
        super().__init__("dash")
        self.duracion_ms = 300  # Duración del Dash en milisegundos
        self.tiempo_inicio = None  # Guarda el tiempo de activación
        self.activo = False  # Indica si el Dash está activo

    def activar(self, jugador):
        """Activa el Dash si no está en uso."""
        if not self.activo:
            self.activo = True
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo de inicio
            jugador.velocidad = jugador.velocidad_base * 3  # Aumenta velocidad

    def update(self, jugador):
        """Verifica si el Dash debe desactivarse automáticamente."""
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio >= self.duracion_ms:
                self.activo = False  # Desactivar Dash
                jugador.velocidad = jugador.velocidad_base  # Restablecer velocidad


        
      
    
