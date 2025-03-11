import math

import pygame

from extras import settings
from extras.resourcesmanager import ResourceManager
from extras.settings import ROJO, ROJO_CLARO
from singleton import SingletonMeta


class Ui(metaclass=SingletonMeta):
    def __init__(self):
        """Inicializa la UI con la pantalla y el tanque del jugador."""
        self.font = pygame.font.Font(None, 36)  # Fuente para los textos
        self.cursor_image = ResourceManager.load_and_scale_image("mirilla.png", 0.75, 0.75)  # Cursor personalizado
        self.set_cursor()


    def set_cursor(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image.get_width() // 2, self.cursor_image.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image)
        pygame.mouse.set_cursor(cursor)

    def dibujar_minimapa(self, jugador, mundo, pantalla):
        """Dibuja el minimapa con habitaciones y conexiones."""
        minimapa = pygame.Surface((200, 100), pygame.SRCALPHA)  # Superficie del minimapa
        minimapa.fill((0, 0, 0, 0))  # Fondo completamente transparente

        # Posiciones de cada habitación en el minimapa
        posiciones = {}

        x_player = jugador.rect_element.centerx // settings.ANCHO
        y_player = jugador.rect_element.centery // settings.ALTO

        # Dibujar habitaciones
        for fila in range(4):
            for col in range(3):
                x = col * (settings.HABITACION_ANCHO + settings.ESPACIADO)
                y = fila * (settings.HABITACION_ALTO + settings.ESPACIADO)

                posiciones[(fila, col)] = (x + settings.HABITACION_ANCHO // 2, y + settings.HABITACION_ALTO // 2)
                if (fila, col) == (y_player, x_player):
                    color = settings.BLANCO_TRANSLUCIDO
                else:
                    color = settings.NEGRO_TRANSLUCIDO

                pygame.draw.rect(minimapa, color, (x, y, settings.HABITACION_ANCHO, settings.HABITACION_ALTO), border_radius=3)

        # Dibujar conexiones con colores variables
        for ((y1, x1), (y2, x2), color) in mundo.CONEXIONES:
            if (y1, x1) in posiciones and (y2, x2) in posiciones:
                # Obtener coordenadas de los centros de las habitaciones
                x1_px, y1_px = posiciones[(y1, x1)]
                x2_px, y2_px = posiciones[(y2, x2)]

                # Calcular la dirección de la línea
                dx, dy = x2_px - x1_px, y2_px - y1_px
                distancia = math.sqrt(dx ** 2 + dy ** 2)

                # Normalizar dirección y ajustar para que la línea comience desde el borde de la habitación
                if distancia > 0:
                    ajuste_x = (dx / distancia) * (settings.HABITACION_ANCHO // 2)
                    ajuste_y = (dy / distancia) * (settings.HABITACION_ALTO // 2)

                    x1_px += ajuste_x
                    y1_px += ajuste_y
                    x2_px -= ajuste_x
                    y2_px -= ajuste_y

                # Dibujar la línea ajustada
                pygame.draw.line(minimapa, color, (x1_px, y1_px), (x2_px, y2_px), 8)

        # Dibujar el minimapa en la pantalla
        pantalla.blit(minimapa, settings.MINIMAPA_POS)

    def draw_health_bar(self, tank, pantalla, cam_x, cam_y):
        """Dibuja una barra de vida debajo del tanque con fondo rojo."""

        # Posición de la barra de vida
        barra_ancho = tank.barra_vida.get_width()  # Ancho total de la barra de vida
        barra_alto = 6  # Altura de la barra de vida
        x = tank.rect_element.x + tank.rect_element.width // 2 - barra_ancho // 2 - cam_x
        y = tank.rect_element.y - cam_y

        # Calcular vida actual (porcentaje)
        vida_porcentaje = max(tank.vida / tank.vida_inicial, 0)  # Evitar valores negativos
        vida_ancho = int(barra_ancho * vida_porcentaje)  # Ajustar el ancho de la barra verde

        # Dibujar fondo rojo
        pygame.draw.rect(pantalla, ROJO, (x, y+2, barra_ancho, barra_alto))

        # Dibujar la vida en verde sobre el fondo rojo
        pygame.draw.rect(pantalla, ROJO_CLARO, (x, y+2, vida_ancho, barra_alto))

        pantalla.blit(tank.barra_vida, (x, y))


    def draw_health_bar_player(self, jugador, pantalla):
        x = 20
        y = 20

        # Asegurar que la vida no sea negativa
        vida_actual = max(jugador.vida, 0)
        pantalla.blit(jugador.barra_vida[vida_actual], (x, y))

