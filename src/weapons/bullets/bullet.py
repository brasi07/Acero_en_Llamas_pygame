import math
import time
from extras import settings
from extras.resourcesmanager import ResourceManager
from extras.settings import TILE_SIZE
from elements.element import Element

class Bullet(Element):
    # Cargar sprites de colisión una sola vez (variable estática)
    sprites_colision = [ResourceManager.load_and_scale_image(f"expl{i}.png", 20 / TILE_SIZE, 20 / TILE_SIZE)
                        for i in range(1, 11)]

    def __init__(self, cannon_tip, angulo, tipoColision):
        self.imagen = ResourceManager.load_and_scale_image("bala_base.png", settings.RESIZE_PLAYER * 0.07, settings.RESIZE_PLAYER * 0.07)
        self.x, self.y = cannon_tip

        super().__init__(self.x, self.y, self.imagen, tipoColision)

        # Convertir ángulo a radianes y calcular velocidad
        self.angulo = math.radians(angulo)
        self.velocidad = 7
        self.vel_x = math.cos(self.angulo) * self.velocidad
        self.vel_y = math.sin(self.angulo) * self.velocidad
        self.dano = 1

        # Estado de la bala
        self.colisionando = False
        self.tiempo_colision = 0
        self.frame_actual = 0

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""
        if self.colisionando:
            return self.actualizar_colision()

        # Mover la bala
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect_element.topleft = (self.x, self.y)

        # Verificar si la bala sale de la pantalla
        if self.fuera_de_pantalla(mundo, ancho_pantalla, alto_pantalla):
            return True  # Eliminar la bala

        # Verificar colisiones con los elementos del mundo
        for elemento in mundo.elementos_por_capa.get(2, []):  # Evita KeyError si la capa no existe
            if self.check_collision(elemento):
                self.realizar_dano(elemento)
                self.iniciar_colision()
                return False  # No eliminar aún, esperar animación



        return False

    def iniciar_colision(self):
        """Activa la animación de colisión y detiene el movimiento."""
        self.colisionando = True
        self.tiempo_colision = time.time()
        self.rect_element = self.sprites_colision[0].get_rect(center=self.rect_element.center)  # Centrar explosión

    def realizar_dano(self, elemento):
        if hasattr(elemento, "vida"):
            elemento.recibir_dano(self.dano)
            return True
        return False

    def actualizar_colision(self):
        """Maneja la animación de colisión y decide si eliminar la bala."""
        tiempo_transcurrido = time.time() - self.tiempo_colision
        self.frame_actual = int((tiempo_transcurrido / 1.0) * len(self.sprites_colision))

        return self.frame_actual >= len(self.sprites_colision)  # Eliminar cuando la animación termine

    def fuera_de_pantalla(self, mundo, ancho_pantalla, alto_pantalla):
        """Verifica si la bala ha salido de la pantalla."""
        return (self.x < mundo.camara_x or self.x > mundo.camara_x + ancho_pantalla or
                self.y < mundo.camara_y or self.y > mundo.camara_y + alto_pantalla)

    def draw(self, pantalla, x, y):
        """Dibuja la bala o su animación de colisión."""
        if self.colisionando:
            if self.frame_actual < len(self.sprites_colision):
                pantalla.blit(self.sprites_colision[self.frame_actual],
                              (self.rect_element.x - x, self.rect_element.y - y))
        else:
            self.dibujar(pantalla, x, y)


