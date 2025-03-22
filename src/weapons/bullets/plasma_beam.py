import pygame

from src.extras import ResourceManager
from src.weapons.bullets import Bullet

class PlasmaBeam(Bullet):
    def __init__(self, arma):
        super().__init__(arma)
        self.animacion = ResourceManager.load_animation("rayo_plasma.png", 64, 1024, 8, resizey=20)
        self.frame_index = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.tiempo_por_frame = 200  # 200ms
        self.arma = arma

        # Obtener imagen inicial y rect
        self.imagen = self.rotar_imagen(self.animacion[self.frame_index])

        # Colocar la imagen en la punta del cañón
        self.rect = self.imagen.get_rect(midtop=self.get_cannon_tip())

    def rotar_imagen(self, imagen):
        """Rota la imagen y ajusta el rect para que la rotación sea sobre la parte superior centrada."""
        imagen_rotada = pygame.transform.rotate(imagen, -self.arma.angulo_cannon - 90)
        self.rect = imagen_rotada.get_rect(midtop=self.get_cannon_tip())  # Usar la punta del cañón como midtop
        return imagen_rotada

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""

        # Verificar colisiones con elementos del mundo
        for elemento in mundo.elementos_por_capa_y_pantalla[2][self.fila_pantalla][self.col_pantalla]:
            if self.check_collision(elemento):
                self.realizar_dano(elemento)
                return False  # No eliminar aún, esperar animación

        # Actualizar animación cada 200ms
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame > self.tiempo_por_frame:
            self.tiempo_ultimo_frame = tiempo_actual
            self.frame_index += 1
            if self.frame_index >= len(self.animacion):
                return True  # La animación terminó, eliminar bala
            self.imagen = self.rotar_imagen(self.animacion[self.frame_index])

        # Actualizar la posición de la bala en cada frame, alineada con la punta del cañón
        self.rect = self.imagen.get_rect(midtop=self.get_cannon_tip())

        return False

