import pygame

import settings


class Ui:
    def __init__(self, mundo):
        """Inicializa la UI con la pantalla y el tanque del jugador."""
        self.mundo = mundo
        self.font = pygame.font.Font(None, 36)  # Fuente para los textos
        self.cursor_image = pygame.image.load("../res/UI/mirilla.png")  # Cursor personalizado
        self.set_cursor()


    def set_cursor(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image.get_width() // 2, self.cursor_image.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image)
        pygame.mouse.set_cursor(cursor)

    def draw_health_bar(self, tank):
        """Dibuja la barra de vida justo debajo del tanque."""

        # Posición del tanque
        x = tank.rect_element.x + tank.rect_element.width // 2 - tank.barra_vida[0].get_width() // 2 - self.mundo.camara_x
        y = tank.rect_element.y - self.mundo.camara_y

        # Asegurar que la vida no sea negativa
        vida_actual = max(tank.vida, 0)
        self.mundo.pantalla.blit(tank.barra_vida[vida_actual], (x, y))


