import math

import pygame

from .extras.resourcesmanager import ResourceManager
from .extras.settings import Settings
from .singleton import SingletonMeta


class Ui(metaclass=SingletonMeta):

    def __init__(self):
        """Inicializa la UI con la pantalla y el tanque del jugador."""
        self.font = pygame.font.Font(None, 36)  # Fuente para los textos
        self.cursor_image1 = ResourceManager.load_and_scale_image("mirilla.png", 0.75, 0.75)  # Cursor personalizado
        self.cursor_image2 = ResourceManager.load_and_scale_image("mirilla2.png", 0.75, 0.75)
        self.set_cursor1()
        self.barras = ResourceManager.load_animation("barras_UI.png", 4, 6, 12, 0.2, 0.3)

    def set_cursor1(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image1.get_width() // 2, self.cursor_image1.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image1)
        pygame.mouse.set_cursor(cursor)

    def set_cursor2(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image2.get_width() // 2, self.cursor_image2.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image2)
        pygame.mouse.set_cursor(cursor)

    def dibujar_minimapa(self, jugador, mundo, pantalla):
        """Dibuja el minimapa con habitaciones y conexiones."""
        minimapa = pygame.Surface((200, 100), pygame.SRCALPHA)  # Superficie del minimapa
        minimapa.fill((0, 0, 0, 0))  # Fondo completamente transparente

        # Posiciones de cada habitación en el minimapa
        posiciones = {}

        x_player = jugador.rect_element.centerx // Settings.ANCHO
        y_player = jugador.rect_element.centery // Settings.ALTO

        # Dibujar habitaciones
        for fila in range(4):
            for col in range(3):
                x = col * (Settings.HABITACION_ANCHO + Settings.ESPACIADO)
                y = fila * (Settings.HABITACION_ALTO + Settings.ESPACIADO)

                posiciones[(fila, col)] = (x + Settings.HABITACION_ANCHO // 2, y + Settings.HABITACION_ALTO // 2)
                if (fila, col) == (y_player, x_player):
                    color = Settings.BLANCO_TRANSLUCIDO
                else:
                    color = Settings.NEGRO_TRANSLUCIDO

                pygame.draw.rect(minimapa, color, (x, y, Settings.HABITACION_ANCHO, Settings.HABITACION_ALTO), border_radius=3)

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
                    ajuste_x = (dx / distancia) * (Settings.HABITACION_ANCHO // 2)
                    ajuste_y = (dy / distancia) * (Settings.HABITACION_ALTO // 2)

                    x1_px += ajuste_x
                    y1_px += ajuste_y
                    x2_px -= ajuste_x
                    y2_px -= ajuste_y

                # Dibujar la línea ajustada
                pygame.draw.line(minimapa, color, (x1_px, y1_px), (x2_px, y2_px), 8)

        # Dibujar el minimapa en la pantalla
        pantalla.blit(minimapa, Settings.MINIMAPA_POS)

    def draw_health_bar(self, tank, pantalla, cam_x, cam_y):
        """Dibuja la barra de vida del tanque en una única superficie y la centra."""
        self.barras = ResourceManager.load_animation("barras_UI.png", 4, 6, 12, 0.2, 0.3)

        # Datos de la barra de vida
        vida_maxima = tank.vida_inicial
        vida_actual = max(tank.vida, 0)  # Evitar negativos
        sprite_width = self.barras[0].get_width()
        sprite_height = self.barras[0].get_height()

        num_segmentos = max(vida_maxima, 0)  # Segmentos intermedios
        total_width = num_segmentos * sprite_width  # Ancho total de la barra

        # **Calcular cuántos segmentos están dañados**
        segmentos_danados = num_segmentos - vida_actual  # Cuántos usarán self.barras[1]
        segmentos_danados = max(0, min(segmentos_danados, num_segmentos))  # Limitar entre 0 y num_segmentos

        # Crear una superficie vacía para toda la barra de vida
        surface_bar = pygame.Surface((total_width, sprite_height), pygame.SRCALPHA)

        primer_sprite = self.barras[0] if segmentos_danados == num_segmentos else self.barras[9]
        ultimo_sprite = self.barras[2] if segmentos_danados > 0 else self.barras[11]

        surface_bar.blit(primer_sprite, (0, 0))  # Primer segmento

        for i in range(num_segmentos-2):
            sprite = self.barras[1] if i+1 >= num_segmentos - segmentos_danados else self.barras[10]
            surface_bar.blit(sprite, ((i + 1) * sprite_width, 0))

        surface_bar.blit(ultimo_sprite, ((num_segmentos-1) * sprite_width, 0))  # Último segmento

        # **Centrar la barra sobre el tanque**
        x = tank.rect_element.centerx - cam_x - total_width // 2  # Centrar horizontalmente
        y = tank.rect_element.y - cam_y  # Un poco arriba del tanque

        # **Dibujar la barra ya centrada**
        pantalla.blit(surface_bar, (x, y))

    def draw_health_bar_player(self, jugador, pantalla):
        x = 20
        y = 20

        # Asegurar que la vida no sea negativa
        vida_actual = max(jugador.vida, 0)
        pantalla.blit(jugador.barra_vida[vida_actual], (x, y))

