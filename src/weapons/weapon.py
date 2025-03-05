import numpy as np
import pygame
from weapons.bullets.bullet import Bullet
from extras.resourcesmanager import ResourceManager

class Weapon:
    def __init__(self, tank):
        self.tank = tank
        self.imagen_canon_base = ResourceManager.cargar_canon(0, "weapons", tank.tank_level)
        self.imagenes_accesorio_base = None

        self.imagen_canon = self.imagen_canon_base
        self.imagen_accesorio = self.imagenes_accesorio_base

        self.rect_canon = self.imagen_canon.get_rect(center=tank.rect_element.center)
        self.rect_accesorio = None

        self.angulo_cannon = 0
        self.balas = []

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
        nueva_bala = Bullet(cannon_tip, self.angulo_cannon, self.tank.colision_layer_balas)
        self.balas.append(nueva_bala)

    def update(self, mundo, tank=None):
        # Calcular la dirección del cañón
        dirx, diry = self.tank.calcular_direccion_canon(mundo, tank)
        
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

    def dibujar_arma(self, mundo):
        if self.imagen_accesorio: #dibujar arma secundaria si necesario
            self.rect_accesorio = self.imagen_accesorio.get_rect(top=self.tank.rect_element.bottom)
            mundo.pantalla.blit(self.imagen_accesorio, (self.tank.rect_element.centerx - self.rect_accesorio.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.tank.rect_element.height // 2 - mundo.camara_y))

        mundo.pantalla.blit(self.imagen_canon, (self.tank.rect_element.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.tank.rect_element.centery - self.rect_canon.height // 2 - mundo.camara_y))

    def dibujar_minas(self,mundo):
        pass

    def activar_secundaria(self, tank, mundo):
        pass

    def update_secundaria(self, tank, mundo):
        pass










