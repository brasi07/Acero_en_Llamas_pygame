import pygame
import settings
from src.bullet import Bala

class Player:
    def __init__(self, pantalla):
        # Cargar imágenes del tanque y escalarlas
        self.sprites = {
            "izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_izquierda.png", settings.RESIZE_PLAYER),
            "derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_derecha.png", settings.RESIZE_PLAYER),
            "arriba": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba.png", settings.RESIZE_PLAYER),
            "abajo": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo.png", settings.RESIZE_PLAYER),
            "arriba_izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba_izquierda.png", settings.RESIZE_PLAYER),
            "arriba_derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba_derecha.png", settings.RESIZE_PLAYER),
            "abajo_izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo_izquierda.png", settings.RESIZE_PLAYER),
            "abajo_derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo_derecha.png", settings.RESIZE_PLAYER),
        }
        self.pantalla = pantalla
        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()
        self.image = self.sprites["abajo"]
        self.rect = self.image.get_rect(center=(self.ancho_pantalla//2, self.alto_pantalla//2))
        self.velocidad = 2
        self.direccion = "abajo"  # Dirección inicial del tanque
        self.balas = []  # Lista para almacenar las balas disparadas
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Tiempo del último disparo

    def cargar_y_escalar_imagen(self, ruta, escala):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (int(imagen.get_width() * escala), int(imagen.get_height() * escala)))

    def update(self, pantalla, elementos):
        teclas = pygame.key.get_pressed()
        direccion = None
        nuevo_rect = self.rect.copy()

        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_derecha"
        elif (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_derecha"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            nuevo_rect.x -= self.velocidad
            direccion = "izquierda"
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            nuevo_rect.x += self.velocidad
            direccion = "derecha"
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            nuevo_rect.y -= self.velocidad
            direccion = "arriba"
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            nuevo_rect.y += self.velocidad
            direccion = "abajo"

        # Verificar colisión con todos los elementos
        if not any(nuevo_rect.colliderect(elemento.rect) for elemento in elementos):
            self.rect = nuevo_rect  # Mover el jugador solo si no hay colisión

        if direccion:
            self.image = self.sprites[direccion]
            self.direccion = direccion  # Actualizar la dirección del tanque

        # Verificar el clic izquierdo del ratón para disparar
        if pygame.mouse.get_pressed()[0]:  # 0 es el botón izquierdo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_disparo >= 1000:  # Verifica si han pasado 2 segundos
                self.disparar()
                self.tiempo_ultimo_disparo = tiempo_actual  # Actualiza el tiempo del último disparo

        # Actualizar las balas
        for bala in self.balas[:]:
            if bala.update(elementos) or bala.fuera_de_pantalla(pantalla):
                self.balas.remove(bala)  # Eliminar la bala si choca o sale de la pantalla

    def disparar(self):
        # Crear una nueva bala en la posición del tanque según la dirección
        nueva_bala = Bala(self.rect.centerx-5, self.rect.centery-5, self.direccion)
        self.balas.append(nueva_bala)

    def draw(self, pantalla):
        # Dibujar las balas
        for bala in self.balas:
            bala.draw(pantalla)

        # Dibujar tanque
        pantalla.blit(self.image, self.rect)

