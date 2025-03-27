import time
from .bullet import Bullet
from ...elements.interactable import Interactable
from ...extras import Settings, ResourceManager


class BouncingBullet(Bullet):

    def __init__(self, arma):
        super().__init__(arma)
        self.rebote_count = 0
        self.rebote_max = 2
        self.sprites = ResourceManager.load_animation("balas_botadoras.png", 32, 32, 3, Settings.RESIZE_PLAYER * 0.13, Settings.RESIZE_PLAYER * 0.13)
        self.imagen = self.sprites[0]

    def iniciar_colision(self, elemento=None):
        if isinstance(elemento, Interactable):
            elemento.interactuar(self)
        if self.rebote_count >= self.rebote_max:
            """Activa la animación de colisión y detiene el movimiento."""
            self.colisionando = True
            self.tiempo_colision = time.time()
            self.rect_element = self.sprites_colision[0].get_rect(center=self.rect_element.center)  # Centrar explosión
        else:
            if self.rebote_count == 0:
                self.collision_layer = Settings.CollisionLayer.BULLET_ANY

            self.rebote_count += 1
            self.imagen = self.sprites[self.rebote_count]

            self.dano += 1 #se incrementa el daño por rebote

            overlap_x = min(self.rect_element.right - elemento.rect_element.left,
                            elemento.rect_element.right - self.rect_element.left)  # calcula cuanto colisionan los rectangulos por la lateral

            overlap_y = min(self.rect_element.bottom - elemento.rect_element.top,
                            elemento.rect_element.bottom - self.rect_element.top)  # calcula cuanto colisionan los rectangulos por arriba y abajo

            # decide cual velocidad cambiar basado en si la colisión es mayor por la lateral o por arriba/abajo
            if overlap_x < overlap_y:
                self.vel_x = -self.vel_x
            else:
                self.vel_y = -self.vel_y

    def check_collision(self, other_element):
        if other_element.collision_layer not in Settings.COLLISION_RULES.get(self.collision_layer, set()):
            return False

        # Comprobar si los rectángulos colisionan y devuelve el element colisionado
        return self.rect_element.colliderect(other_element.rect_element)

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""
        if self.colisionando:
            return self.actualizar_colision()

        # Mover la bala
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect_element.topleft = (self.x, self.y)

        # Verificar colisiones con los elementos del mundo
        for elemento in mundo.elementos_por_capa_y_pantalla[2][self.fila_pantalla][self.col_pantalla]:  # Evita KeyError si la capa no existe
            if self.check_collision(elemento):
                if self.realizar_dano(elemento):
                    self.rebote_count = self.rebote_max
                self.iniciar_colision(elemento)
                return False  # No eliminar aún, esperar animación

        # Verificar si la bala sale de la pantalla
        if self.fuera_de_pantalla(mundo, ancho_pantalla, alto_pantalla):
            return True  # Eliminar la bala

        return False