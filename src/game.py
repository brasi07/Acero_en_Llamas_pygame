import math
import pygame
import settings
from elements import Boton
from world import World
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1
        self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.ejecutando = True

        self.jugador = Player(0, 0)
        self.mundo = World(self.pantalla, "1", self.jugador)

    def run(self):
        self.set_cursor()
        while self.ejecutando:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

        pygame.quit()

    def set_cursor(self):
        cursor_image = pygame.image.load("../res/UI/mirilla.png")
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
                    self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO))
                elif evento.key == pygame.K_e:  # Presionar "E" para activar botones
                    for capa in self.mundo.elementos_por_capa.values():
                        for elemento in capa:
                            if isinstance(elemento, Boton) and self.jugador.rect_element.colliderect(
                                    elemento.rect_element):
                                elemento.activar()
                if evento.key == pygame.K_g: #cambiar arma secundaria con la tecla G (temporario mientras no se pueden encontrar las armas en el juego)
                    self.jugador.cambiar_arma_secundaria()
                if evento.key == pygame.K_m:
                    self.mundo = World(self.pantalla, "2", self.jugador)


    def update(self):
        self.jugador.update(self.mundo)
        #self.mundo.update()

    def draw(self):
        self.mundo.draw(self.pantalla)
        self.jugador.draw(self.mundo)
        pygame.display.flip()

