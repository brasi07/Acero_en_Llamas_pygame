import numpy as np
import pygame
from bullet import Bala
from bullet import BalaRebote
import spritesheet
import settings
from mina import Mina

class Weapon:
    def __init__(self, tank):
        self.tank = tank
        self.imagen_canon_base = self.cargar_canon(0, tank.tank_type, "armas/weapons", tank.tank_color)
        self.imagenes_accesorio_base = None

        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.rect_accesorio = None

        self.angulo_cannon = 0
        self.balas = []

    @staticmethod
    def cargar_canon(numberweapon, tank_type, sprite_type, tank_color):
        weapon_sprite_sheet = spritesheet.SpriteSheet(f"../res/entidades/{tank_type}/{sprite_type}{tank_color}.png")
        weapon_strip = weapon_sprite_sheet.load_strip((0, 0, 96, 96), 16, settings.ELIMINAR_FONDO)
        weapon_sprites = [pygame.transform.scale(frame, (settings.RESIZE_CANNON * settings.TILE_SIZE, settings.RESIZE_CANNON * settings.TILE_SIZE)) for frame in weapon_strip]
        sprite_weapon = weapon_sprites[numberweapon]
        return sprite_weapon

    @staticmethod
    def escalar_y_cargar_imagen(ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (settings.TILE_SIZE * settings.RESIZE_PLAYER, settings.TILE_SIZE * settings.RESIZE_PLAYER))

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
        nueva_bala = Bala(cannon_tip, self.angulo_cannon, self.tank.colision_layer_balas)
        self.balas.append(nueva_bala)

    def update(self, mundo=None, jugador=None):
        # Calcular la dirección del cañón
        dirx, diry = self.tank.calcular_direccion_canon(mundo, jugador)
        
        # Calcular el ángulo del cañón
        self.angulo_cannon = np.degrees(np.arctan2(diry, dirx))  # Guardar el ángulo para disparos

        self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, -self.angulo_cannon - 90)
        self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)

        for bala in self.balas[:]:
            if bala.update(mundo, mundo.ancho_pantalla, mundo.alto_pantalla):
                self.balas.remove(bala)

    def cambio_de_arma(self):
        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

    def dibujar_balas(self, mundo):
        for bala in self.balas:
            bala.draw(mundo)

    def dibujar_minas(self,mundo):
        pass

    def dibujar_arma(self, mundo):
        if self.imagen_accesorio: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            mundo.pantalla.blit(self.imagen_accesorio, (self.tank.rect_element.centerx - self.rect_accesorio.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.tank.rect_element.height // 2 - mundo.camara_y))

        mundo.pantalla.blit(self.imagen_canon, (self.tank.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))

    def activar_secundaria(self, tank, mundo):
        pass

    def update_secundaria(self, tank, mundo):
        pass

class Dash(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "dash"
        self.imagenes_accesorio_base = self.tank.generar_sprites(settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, "jugador", "armas/dash")

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


class Escopeta(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.nombre_sprite = "turret_01_mk4"
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.animacion = settings.escalar_y_cargar_animacion(f"../res/entidades/jugador/armas/{self.nombre_sprite}.png", 128, 128, 8)
        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, tank, mundo):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_central = Bala(self.get_cannon_tip(), self.angulo_cannon, self.tank.colision_layer_balas)
        bala_izquierda = Bala(self.get_cannon_tip(), self.angulo_cannon - 15, self.tank.colision_layer_balas)
        bala_derecha = Bala(self.get_cannon_tip(), self.angulo_cannon + 15, self.tank.colision_layer_balas)
        self.balas.append(bala_central)
        self.balas.append(bala_izquierda)
        self.balas.append(bala_derecha)
        self.activo = True
    
    def update_secundaria(self, tank, mundo):
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
        self.animacion = settings.escalar_y_cargar_animacion("../res/entidades/jugador/armas/turret_02_mk1.png", 128, 128, 8)
        self.imagen_canon_base = self.animacion[0]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, tank, mundo):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_rebote = BalaRebote(self.get_cannon_tip(), self.angulo_cannon, self.tank.colision_layer_balas)
        self.balas.append(bala_rebote)
        self.activo = True

    def update_secundaria(self, tank, mundo):
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

class Arma_Minas(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = pygame.time.get_ticks()
        #self.imagenes_accesorio_base = self.tank.generar_sprites(settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, "jugador", "armas/mina") 
        self.activo = False
        self.minas = []

    def activar_secundaria(self, tank, mundo):
        self.actvio = True
        self.tiempo_inicio = pygame.time.get_ticks()
        nova_mina = Mina(self.tank.rect_element.x, self.tank.rect_element.y)
        mundo.elementos_por_capa[2].append(nova_mina)
        self.minas.append(nova_mina)
    
    def update_secundaria(self, tank, mundo):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio  # Milisegundos desde el inicio del Dash

        for mina in self.minas:
            if (tiempo_actual - mina.tiempo_creacion) > mina.duracion:
                mina.activar(mundo)
                self.minas.remove(mina)
    

    def dibujar_minas(self, mundo):
        for mina in self.minas:
            mina.dibujar(mundo)

