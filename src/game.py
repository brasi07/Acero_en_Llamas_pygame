import math
import pygame
import settings
from interactuable import Boton
from ui import Ui
from world import World
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1
        self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.ejecutando = True
        self.en_juego = True
        self.selected_item = 0
        self.mundo_actual = "1"

        #opciones menu pausa
        self.menu_items = ["Back to Game", "Options", "Quit"]

        # Fuente
        self.font = pygame.font.Font(None, 74)

        self.jugador = Player(0, 0)
        self.mundo = World(self.pantalla, self.mundo_actual, self.jugador)
        self.ui = Ui()

    def run(self):
        while self.ejecutando:
            self.handle_events()
            if self.en_juego:
                self.update()
                self.draw()
                self.clock.tick(settings.FPS)

        pygame.quit()

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Detecta cuando se presiona ESC
                    self.toggle_pause()
                elif evento.key == pygame.K_F11:
                    self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO))
                else:
                    if self.en_juego == True:
                        if evento.key == pygame.K_g: #cambiar arma secundaria con la tecla G (temporario mientras no se pueden encontrar las armas en el juego)
                            self.jugador.cambiar_arma_secundaria()
                        elif evento.key == pygame.K_m:
                            if self.mundo.mundo_number == "1":
                                self.mundo = World(self.pantalla, "2", self.jugador, True)
                            elif self.mundo.mundo_number == "2":
                                self.mundo = World(self.pantalla, "1", self.jugador)
                            elif self.mundo.mundo_number == "3":
                                self.mundo = World(self.pantalla, "1", self.jugador)
                    else:
                        if evento.key == pygame.K_w:
                            self.selected_item -= 1
                            if self.selected_item < 0: self.selected_item = 2
                            self.update_selected_option()
                            pygame.display.flip()
                        elif evento.key == pygame.K_s:
                            self.selected_item += 1
                            if self.selected_item > 2: self.selected_item = 0
                            self.update_selected_option()
                            pygame.display.flip()
                        elif evento.key == pygame.K_RETURN:
                            self.do_the_thing()

    def toggle_pause(self):
        self.en_juego = not self.en_juego
        if not self.en_juego:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.pause_menu()
        else:
            self.ui.set_cursor()
        pygame.display.flip()

    def pause_menu(self):

        self.selected_item = 0

        self.update_selected_option()

    def update_selected_option(self):
        for index, item in enumerate(self.menu_items):
            color = settings.VERDE if index == self.selected_item else (150, 150, 150)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(settings.ANCHO/2, (settings.ALTO/2 - 100 + index * 100)))
            self.mundo.pantalla.blit(text, rect)

    def do_the_thing(self):
        if self.selected_item == 0:
            self.toggle_pause()
        if self.selected_item == 2:
            self.ejecutando = False  # Termina el juego

    def update(self):
        self.jugador.update(self.mundo)
        if self.jugador.muerto:
            self.jugador.muerto = False
            self.mundo = World(self.pantalla, self.mundo_actual, self.jugador)
        self.mundo.update()

    def draw(self):
        self.mundo.draw()
        
        for enemigo in self.mundo.enemigos:
            enemigo.dibujar_enemigo(self.mundo)

        self.jugador.draw(self.mundo)

        for enemigo in self.mundo.enemigos:
            enemigo.arma.dibujar_balas(self.mundo)

        self.jugador.arma.dibujar_balas(self.mundo)

        if self.mundo.hasSky:
            self.mundo.draw_sky()

        for enemigo in self.mundo.enemigos:
            self.ui.draw_health_bar(enemigo, self.mundo)

        self.ui.draw_health_bar_player(self.jugador, self.pantalla)
        self.ui.dibujar_minimapa(self.jugador, self.mundo)

        pygame.display.flip()


