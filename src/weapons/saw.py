import pygame
from ..extras import TIME_FRAME, ResourceManager
from .weapon import Weapon

class Saw(Weapon):
    DIRECCIONES_ROTACION = {
        "arriba": 0,
        "derecha": -90,
        "izquierda": 90,
        "abajo": 180,
        "arriba_izquierda": 45,
        "arriba_derecha": -45,
        "abajo_izquierda": 135,
        "abajo_derecha": -135
    }

    def __init__(self, tank):
        super().__init__(tank)
        self.animacion = ResourceManager.load_animation("weapons_boss1.png", 96, 96, 3)
        self.imagen_canon_base = self.animacion[0]
        self.imagen_canon = self.imagen_canon_base
        self.frame_actual = 0
        self.ultimo_cambio_frame = 0
        self.ultimo_golpe = 0  # Guarda el tiempo del último golpe
        self.tiempo_actual = 0

    def activar_secundaria(self, mundo, jugador):
        if self.tiempo_actual - self.ultimo_golpe > 1000:
            jugador.recibir_dano(1)
            self.ultimo_golpe = self.tiempo_actual

    def update_secundaria(self, tank, mundo):
        self.tiempo_actual = pygame.time.get_ticks()

        if self.tiempo_actual - self.ultimo_cambio_frame >= TIME_FRAME:
            self.ultimo_cambio_frame = self.tiempo_actual  # Actualizar el tiempo del último cambio
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion)

            # Actualizar la imagen del cañón
            self.imagen_canon_base = self.animacion[self.frame_actual]
            self.actualizar_rotacion(self.tank.direccion)  # Aplicar rotación según la dirección del tanque

    def actualizar_rotacion(self, direccion):
        """Rota la imagen de la sierra según la dirección del tanque."""
        if direccion in self.DIRECCIONES_ROTACION:
            angulo = self.DIRECCIONES_ROTACION[direccion]
            self.imagen_canon = pygame.transform.rotate(self.imagen_canon_base, angulo)
            self.rect_canon = self.imagen_canon.get_rect(center=self.tank.rect_element.center)



