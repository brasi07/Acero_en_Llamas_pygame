import pygame
import abc
import math
from bullet import Bala
import spritesheet
import settings

class Weapon(abc.ABC):  # Clase base abstracta para armas
    def __init__(self, tipo):
        self.imagen_canon_especial = self.escalar_y_cargar_imagen(f"../res/entidades/jugador/armas/{tipo}.png")
        self.imagen_accesorio = self.escalar_y_cargar_imagen(f"../res/entidades/jugador/armas/{tipo}.png")

    def generar_sprites(self, ruta):
        sprite_base = self.escalar_y_cargar_imagen(ruta + "bodies/body_tracks.png")
        sprite_base_45 = self.escalar_y_cargar_imagen(ruta + "bodies/body_tracks_45.png")

        return {
            "arriba": sprite_base,
            "derecha": pygame.transform.rotate(sprite_base, -90),
            "izquierda": pygame.transform.rotate(sprite_base, 90),
            "abajo": pygame.transform.rotate(sprite_base, 180),
            "arriba_izquierda": sprite_base_45,
            "arriba_derecha": pygame.transform.rotate(sprite_base_45, -90),
            "abajo_izquierda": pygame.transform.rotate(sprite_base_45, 90),
            "abajo_derecha": pygame.transform.rotate(sprite_base_45, 180),
        }

    @staticmethod
    def escalar_y_cargar_imagen(ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (settings.TILE_SIZE * settings.RESIZE_PLAYER, settings.TILE_SIZE * settings.RESIZE_PLAYER))

    @staticmethod
    def escalar_y_cargar_animacion(ruta):
        sprite_sheet = spritesheet.SpriteSheet(ruta)
        animacion = sprite_sheet.load_strip((0, 0, 128, 128), 8, settings.ELIMINAR_FONDO)
        return [pygame.transform.scale(frame, (settings.RESIZE_PLAYER * settings.TILE_SIZE, settings.RESIZE_PLAYER * settings.TILE_SIZE)) for frame in animacion]

    @abc.abstractmethod
    def cambio_de_arma(self, tank):
        """Método abstracto que todas las armas deben implementar"""
        pass

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

    def cambio_de_arma(self, tank):
        tank.sprites["cannon"] = tank.cargar_canon_base("../res/entidades/jugador/")
        tank.sprite_arma_secundaria = self.imagen_accesorio

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
        super().__init__("turret_01_mk1")
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.animacion = self.escalar_y_cargar_animacion("../res/entidades/jugador/armas/turret_01_mk4.png")
        self.frame_actual = 0
        self.imagen_canon_especial = self.animacion[0]
        self.activo = False

    def cambio_de_arma(self, tank):
        tank.sprites["cannon"] = self.imagen_canon_especial
        tank.sprite_arma_secundaria = None  # No hay sprite separado para la escopeta
        
    def activar(self, tank):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bala(tank.get_cannon_tip(), tank.angulo_cannon, settings.CollisionLayer.BULLET_PLAYER)
        bala_izquierda = Bala(tank.get_cannon_tip(), tank.angulo_cannon - 15, settings.CollisionLayer.BULLET_PLAYER)
        bala_derecha = Bala(tank.get_cannon_tip(), tank.angulo_cannon + 15, settings.CollisionLayer.BULLET_PLAYER)
        tank.balas.append(bala_central)
        tank.balas.append(bala_izquierda)
        tank.balas.append(bala_derecha)
        self.activo = True
    
    def update(self, tank):
        if self.activo:
            if self.frame_actual < len(self.animacion):
                self.imagen_canon_especial = self.animacion[self.frame_actual]
                tank.sprites["cannon"] = self.imagen_canon_especial
                self.frame_actual += 1
            else:
                self.frame_actual = 0
                self.imagen_canon_especial = self.animacion[0]
                tank.sprites["cannon"] = self.imagen_canon_especial
                self.activo = False


        
        
        
      
    
