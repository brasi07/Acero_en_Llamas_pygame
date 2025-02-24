
from settings import CollisionLayer
from tank import Tank
from weapon import *


class Player(Tank):

    def __init__(self, x, y):

        # Llamamos primero al constructor de la clase base (Tank)
        super().__init__(4, 3, x, y, settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, collision_layer=CollisionLayer.PLAYER, tank_type="jugador")

        # Equipamos armas
        self.armas = [Weapon(self), Dash(self), Escopeta(self), Rebote(self), Arma_Minas(self)]  # Lista de armas
        self.armas_pos = 0  # Índice de arma secundaria equipada
        self.colision_layer_balas = CollisionLayer.BULLET_PLAYER
        self.barra_vida = settings.escalar_y_cargar_animacion(f"../res/UI/vida_jugador.png", 48, 7, 5, resizex=5,resizey=0.5)


    def update(self, mundo):
        self.mover(mundo)
        self.arma.update_secundaria(self, mundo)
        self.arma.update(mundo=mundo)
        self.gestionar_armas(mundo)
        self.verificar_fuera_pantalla(mundo)

    def mover(self, mundo):
        teclas = pygame.key.get_pressed()
        movimiento_x, movimiento_y = self.obtener_movimiento(teclas)
        self.actualizar_posicion(movimiento_x, movimiento_y, mundo)

    def obtener_movimiento(self, teclas):
        movimiento_x = (-self.velocidad if teclas[pygame.K_LEFT] or teclas[pygame.K_a] else 0) + \
                       (self.velocidad if teclas[pygame.K_RIGHT] or teclas[pygame.K_d] else 0)
        movimiento_y = (-self.velocidad if teclas[pygame.K_UP] or teclas[pygame.K_w] else 0) + \
                       (self.velocidad if teclas[pygame.K_DOWN] or teclas[pygame.K_s] else 0)
        if movimiento_x and movimiento_y:
            movimiento_x *= 0.707
            movimiento_y *= 0.707
        return movimiento_x, movimiento_y

    def verificar_fuera_pantalla(self, mundo):
        if self.rect_element.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif self.rect_element.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif self.rect_element.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif self.rect_element.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

    def gestionar_armas(self, mundo):
        if pygame.mouse.get_pressed()[0]:
            if pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= 1000:
                self.arma.activar()
                self.tiempo_ultimo_disparo = pygame.time.get_ticks()

        if pygame.mouse.get_pressed()[2]:
            self.usar_arma_especial(mundo)

    def cambiar_arma_secundaria(self):
        # Cambia a la siguiente arma en la lista (ciclo circular)
        self.armas_pos = (self.armas_pos + 1) % len(self.armas)
        self.arma = self.armas[self.armas_pos]
        self.arma.cambio_de_arma()

    def draw(self, mundo):
        self.dibujar(mundo)
        self.arma.dibujar_arma(mundo)

    def calcular_direccion_canon(self, mundo, jugador):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        dirx = cursorx - (self.rect_element.centerx - mundo.camara_x)
        diry = cursory - (self.rect_element.centery - mundo.camara_y)

        return dirx, diry
