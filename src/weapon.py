import pygame
import abc
import math
from bullet import Bala
import spritesheet
import settings

class Weapon(abc.ABC):  # Clase base abstracta para armas
    def __init__(self, tipo):
        self.tipo = tipo
        self.imagen = f"../res/entidades/jugador/armas/{tipo}.png"

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


class Escopeta(Weapon):
    def __init__(self):
        super().__init__("escopeta")
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.sprite_sheet = spritesheet.SpriteSheet("../res/entidades/jugador/armas/escopeta.png")
        self.imagen = self.sprite_sheet.image_at((0,0,128,128))
        self.imagen.set_colorkey((0,0,0))
        self.animacion = self.sprite_sheet.load_strip((0,0,128,128), 8, (0,0,0))
        self.frame_actual = 0
        self.activo = False
        
    def activar(self, jugador):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bala(jugador.get_cannon_tip(), jugador.angulo_cannon, jugador.tamaño_tile, settings.CollisionLayer.BULLET_PLAYER)
        bala_izquierda = Bala(jugador.get_cannon_tip(), jugador.angulo_cannon - 15, jugador.tamaño_tile, settings.CollisionLayer.BULLET_PLAYER)
        bala_derecha = Bala(jugador.get_cannon_tip(), jugador.angulo_cannon + 15, jugador.tamaño_tile, settings.CollisionLayer.BULLET_PLAYER)
        jugador.balas.append(bala_central)
        jugador.balas.append(bala_izquierda)
        jugador.balas.append(bala_derecha)
        self.activo = True
    
    def update(self, jugador):
        if self.activo:
            if self.frame_actual < len(self.animacion):
                self.imagen = self.animacion[self.frame_actual]
                jugador.sprite_cannon = self.imagen
                self.frame_actual += 1
            else:
                self.frame_actual = 0
                self.imagen = self.animacion[0]
                jugador.sprite_cannon = self.imagen
                self.activo = False
        
        
        
      
    
