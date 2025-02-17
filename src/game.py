import math
import pygame
import settings
from world import World
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1
        self.pantalla = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.ejecutando = True

        self.mundo = World("1", self.pantalla)
        self.jugador = self.mundo.player

    def run(self):
        self.set_cursor()
        while self.ejecutando:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def set_cursor(self):
        cursor_image = pygame.image.load("../res/tanques/mirilla.png")
        cursor = pygame.cursors.Cursor((cursor_image.get_width() // 2, cursor_image.get_height() // 2), cursor_image)
        pygame.mouse.set_cursor(cursor)

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Detecta cuando se presiona ESC
                    self.ejecutando = False  # Termina el juego
                elif evento.key == pygame.K_F11:
                    self.pantalla = pygame.display.set_mode((1280, 720))


    def update(self):
        self.jugador.update(self.mundo)
        #self.mundo.update()

    def draw(self):
        self.pantalla.fill((0, 0, 0))
        self.mundo.draw(self.pantalla)
        self.jugador.draw(self.mundo)
        pygame.display.flip()

