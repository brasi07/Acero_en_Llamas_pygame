import numpy as np
import pygame
from bullet import Bala
from bullet import BalaRebote
import spritesheet
import settings

class Weapon:
    def __init__(self, tank):
        self.tank = tank
        self.imagen_canon_base = self.cargar_canon(0, tank.ruta, tank.tank_type)
        self.imagen_accesorio_base = None

        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagen_accesorio_base

        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.rect_accesorio = None

        self.angulo_cannon = 0
        self.balas = []

    @staticmethod
    def cargar_canon(numberweapon, ruta, tank_type=""):
        weapon_sprite_sheet = spritesheet.SpriteSheet(ruta + "armas/weapons" + tank_type + ".png")
        weapon_strip = weapon_sprite_sheet.load_strip((0, 0, 96, 96), 16, settings.ELIMINAR_FONDO)
        weapon_sprites = [pygame.transform.scale(frame, (settings.RESIZE_CANNON * settings.TILE_SIZE, settings.RESIZE_CANNON * settings.TILE_SIZE)) for frame in weapon_strip]
        sprite_weapon = weapon_sprites[numberweapon]
        return sprite_weapon

    @staticmethod
    def escalar_y_cargar_imagen(ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (settings.TILE_SIZE * settings.RESIZE_PLAYER, settings.TILE_SIZE * settings.RESIZE_PLAYER))

    @staticmethod
    def escalar_y_cargar_animacion(ruta, numberSprites):
        sprite_sheet = spritesheet.SpriteSheet(ruta)
        animacion = sprite_sheet.load_strip((0, 0, 128, 128), numberSprites, settings.ELIMINAR_FONDO)
        return [pygame.transform.scale(frame, (settings.RESIZE_PLAYER * settings.TILE_SIZE, settings.RESIZE_PLAYER * settings.TILE_SIZE)) for frame in animacion]

    def get_cannon_tip(self):
        """Calcula la punta del cañón después de la rotación"""
        angle_rad = np.radians(self.angulo_cannon)  # Convertir ángulo a radianes
        cannon_length = self.rect_canon.height // 4  # Largo del cañon

        # Calcular desplazamiento desde el centro del cañón
        x_offset = cannon_length * np.cos(angle_rad)
        y_offset = cannon_length * np.sin(angle_rad)

        # Devolver la nueva posición del midtop corregido
        return self.rect_canon.centerx + x_offset, self.rect_canon.centery + y_offset

    def activar(self):
        cannon_tip = self.get_cannon_tip()  # Obtener la punta del cañón
        nueva_bala = Bala(cannon_tip, self.angulo_cannon, settings.CollisionLayer.BULLET_PLAYER)
        self.balas.append(nueva_bala)

    def update(self, mundo):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        dirx = cursorx - (self.tank.rect_element.centerx - mundo.camara_x)
        diry = cursory - (self.tank.rect_element.centery - mundo.camara_y)

        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diry, dirx))  # Guardar el ángulo para disparos

        self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, -self.angulo_cannon - 90)
        self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)

        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def cambio_de_arma(self):
        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagen_accesorio_base

    def draw(self, mundo):
        for bala in self.balas:
            bala.draw(mundo)

        if self.imagen_accesorio: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            mundo.pantalla.blit(self.imagen_accesorio, (self.tank.rect_element.centerx - self.rect_accesorio.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.tank.rect_element.height // 2 - mundo.camara_y))

        mundo.pantalla.blit(self.imagen_canon, (self.tank.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))

    def activar_secundaria(self, tank):
        pass

    def update_secundaria(self, mundo):
        pass

class Dash(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "dash"
        self.duracion_ms = 300  # Duración del Dash en milisegundos
        self.tiempo_inicio = None  # Guarda el tiempo de activación
        self.activo = False  # Indica si el Dash está activo
        self.imagen_accesorio_base = self.escalar_y_cargar_imagen(f"../res/entidades/jugador/armas/{self.nombre_sprite}.png")

    def activar_secundaria(self, tank):
        """Activa el Dash si no está en uso."""
        if not self.activo:
            self.activo = True
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo de inicio
            tank.velocidad = tank.velocidad_base * 3  # Aumenta velocidad

    def update_secundaria(self, tank):
        """Verifica si el Dash debe desactivarse automáticamente."""
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio >= self.duracion_ms:
                self.activo = False  # Desactivar Dash
                tank.velocidad = tank.velocidad_base  # Restablecer velocidad


class Escopeta(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "turret_01_mk4"
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.animacion = self.escalar_y_cargar_animacion(f"../res/entidades/jugador/armas/{self.nombre_sprite}.png", 8)
        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, tank):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bala(self.get_cannon_tip(), self.angulo_cannon, settings.CollisionLayer.BULLET_PLAYER)
        bala_izquierda = Bala(self.get_cannon_tip(), self.angulo_cannon - 15, settings.CollisionLayer.BULLET_PLAYER)
        bala_derecha = Bala(self.get_cannon_tip(), self.angulo_cannon + 15, settings.CollisionLayer.BULLET_PLAYER)
        self.balas.append(bala_central)
        self.balas.append(bala_izquierda)
        self.balas.append(bala_derecha)
        self.activo = True
    
    def update_secundaria(self, tank):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= settings.TIME_FRAME:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina

                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                self.imagen_canon = self.imagen_canon_base


class Rebote(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.animacion = self.escalar_y_cargar_animacion("../res/entidades/jugador/armas/turret_02_mk1.png", 8)
        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, tank):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_rebote = BalaRebote(self.get_cannon_tip(), self.angulo_cannon, settings.CollisionLayer.BULLET_PLAYER)
        self.balas.append(bala_rebote)
        self.activo = True

    def update_secundaria(self, tank):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= settings.TIME_FRAME:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina

                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                self.imagen_canon = self.imagen_canon_base


        
        
        
      
    
