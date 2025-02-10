import pygame
from src.world import World
from src.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.ejecutando = True
        self.jugador = Player()
        self.mundo = World("mundo_1")

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

    def update(self):
        self.jugador.update(self.pantalla, self.mundo.muro)
        self.mundo.update()

    def draw(self):
        self.pantalla.fill((0, 0, 0))
        self.mundo.draw(self.pantalla)
        self.jugador.draw(self.pantalla)
        pygame.display.flip()

