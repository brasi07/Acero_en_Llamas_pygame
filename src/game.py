import pygame
from src.world import World
from src.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
        #self.pantalla = pygame.display.set_mode((800, 600))  # Ventana de 800x600

        self.clock = pygame.time.Clock()
        self.ejecutando = True
        self.jugador = Player()
        self.mundo = World("mundo_1", self.pantalla)

    def run(self):
        while self.ejecutando:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Detecta cuando se presiona ESC
                    self.ejecutando = False  # Termina el juego

    def update(self):
        self.jugador.update(self.pantalla, self.mundo.elementos)
        self.mundo.update()

    def draw(self):
        self.pantalla.fill((0, 0, 0))
        self.mundo.draw(self.pantalla)
        self.jugador.draw(self.pantalla)
        pygame.display.flip()

