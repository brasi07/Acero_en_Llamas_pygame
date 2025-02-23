import pygame

import settings


class Ui:
    def __init__(self, screen, tank):
        """Inicializa la UI con la pantalla y el tanque del jugador."""
        self.screen = screen
        self.tank = tank
        self.font = pygame.font.Font(None, 36)  # Fuente para los textos
        self.cursor_image = pygame.image.load("../res/UI/mirilla.png")  # Cursor personalizado
        self.set_cursor()

    def set_cursor(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image.get_width() // 2, self.cursor_image.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image)
        pygame.mouse.set_cursor(cursor)

    def draw_health_bar(self):
        """Dibuja la barra de vida del tanque."""
        vida_maxima = 10  # Valor máximo de vida
        barra_ancho = 200
        barra_altura = 20
        x, y = 20, 20  # Posición en la pantalla
        vida_actual = max(self.tank.vida, 0)  # Asegurar que la vida no sea negativa
        vida_actual = 5
        grosor_marco = 3

        if vida_actual <= 3:
            color = settings.ROJO
        elif vida_actual <= 6:
            color = settings.AMARILLO
        else:
            color = settings.VERDE

        # Fondo de la barra
        pygame.draw.rect(self.screen, settings.NEGRO, (x, y, barra_ancho, barra_altura))
        # Barra de vida
        ancho_vida = (vida_actual / vida_maxima) * (barra_ancho - grosor_marco*2)
        pygame.draw.rect(self.screen, color, (x + grosor_marco, y + grosor_marco, ancho_vida, barra_altura - grosor_marco*2))


    def draw_ui(self):
        """Dibuja todos los elementos de la UI en la pantalla."""
        self.draw_health_bar()
