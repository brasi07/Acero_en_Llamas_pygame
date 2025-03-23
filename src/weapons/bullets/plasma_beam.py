import pygame

from src.extras import ResourceManager
from src.weapons.bullets import Bullet
from src.extras import COLLISION_RULES

class PlasmaBeam(Bullet):
    def __init__(self, arma):
        super().__init__(arma, desplazamiento_frontal=351)
        self.animacion = ResourceManager.load_animation("rayo_plasma.png", 64, 1024, 8, resizex=1.5, resizey=20)
        self.frame_index = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.tiempo_por_frame = 200  # 200ms
        self.arma = arma

        self.imagen = pygame.transform.rotate(self.animacion[self.frame_index], -arma.angulo_cannon - 90)
        self.rect_element = self.imagen.get_rect(center=self.rect_element.center)
        self.mask = pygame.mask.from_surface(self.imagen)

        
    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""

        # Verificar colisiones con elementos del mundo
        for elemento in mundo.elementos_por_capa_y_pantalla[2][self.fila_pantalla][self.col_pantalla]:
            if self.check_collision(elemento) and self.frame_index != 0:
                self.realizar_dano(elemento)
                return False  # No eliminar aún, esperar animación

        # Actualizar animación cada 200ms
        tiempo_actual = pygame.time.get_ticks()
        if self.frame_index == 0 and tiempo_actual -  self.tiempo_ultimo_frame > 500:
            self.tiempo_ultimo_frame = tiempo_actual
            self.frame_index += 1
            
        elif tiempo_actual - self.tiempo_ultimo_frame > self.tiempo_por_frame and self.frame_index != 0:
            self.tiempo_ultimo_frame = tiempo_actual
            self.frame_index += 1
            if self.frame_index >= len(self.animacion):
                return True  # La animación terminó, eliminar bala

        self.imagen = pygame.transform.rotate(self.animacion[self.frame_index], -self.arma.angulo_cannon - 90)
        self.rect_element = self.imagen.get_rect(center=self.rect_element.center)
        self.mask = pygame.mask.from_surface(self.imagen)

        return False


