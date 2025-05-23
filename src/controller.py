from abc import ABC, abstractmethod

import pygame


class Control(ABC):

    @abstractmethod
    def arriba(self, teclas):
        pass

    @abstractmethod
    def abajo(self, teclas):
        pass

    @abstractmethod
    def izquierda(self, teclas):
        pass

    @abstractmethod
    def derecha(self, teclas):
        pass

    @abstractmethod
    def arriba_tap(self, evento):
        pass

    @abstractmethod
    def abajo_tap(self, evento):
        pass

    @abstractmethod
    def izquierda_tap(self, evento):
        pass

    @abstractmethod
    def derecha_tap(self, evento):
        pass

    @abstractmethod
    def principal(self, teclas):
        pass

    @abstractmethod
    def secundaria(self, teclas):
        pass

    @abstractmethod
    def aceptar(self, evento):
        pass

    @abstractmethod
    def rechazar(self, evento):
        pass

    @abstractmethod
    def pausar(self, evento):
        pass


class KeyboardControl(Control):

    def arriba(self, teclas):
        return teclas[pygame.K_w] or teclas[pygame.K_UP]

    def abajo(self, teclas):
        return teclas[pygame.K_s] or teclas[pygame.K_DOWN]

    def izquierda(self, teclas):
        return teclas[pygame.K_a] or teclas[pygame.K_LEFT]

    def derecha(self, teclas):
        return teclas[pygame.K_d] or teclas[pygame.K_RIGHT]

    def arriba_tap(self, evento):
        return evento.type == pygame.KEYDOWN and (evento.key == pygame.K_w or evento.key == pygame.K_UP)

    def abajo_tap(self, evento):
        return evento.type == pygame.KEYDOWN and (evento.key == pygame.K_s or evento.key == pygame.K_DOWN)

    def izquierda_tap(self, evento):
        return evento.type == pygame.KEYDOWN and (evento.key == pygame.K_a or evento.key == pygame.K_LEFT)

    def derecha_tap(self, evento):
        return evento.type == pygame.KEYDOWN and (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT)

    def principal(self, teclas):
        return pygame.mouse.get_pressed()[0]

    def secundaria(self, teclas):
        return pygame.mouse.get_pressed()[2]

    def aceptar(self, evento):
        return pygame.mouse.get_pressed()[0] or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN)

    def rechazar(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE

    def pausar(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE

    def change_world(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key == pygame.K_m

    def open_minimap(self, evento):
        return (evento.type == pygame.KEYDOWN or evento.type == pygame.KEYUP)and evento.key == pygame.K_SPACE

    def change_weapon(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key == pygame.K_g
