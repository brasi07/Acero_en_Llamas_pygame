import pygame

class Weapon:
    def __init__(self, tipo):
        self.tipo = tipo
        #self.imagen = pygame.image.load(f"res/armas/{tipo}.png")


class dash(Weapon):

    def __init__(self):
        self.tipo = "dash"
        Weapon.__init__(self, self.tipo)

    def use(self, velocidad, duracion, inicial):
        if duracion > 0:
            velocidad = inicial * 3
            return velocidad
        else:
            velocidad = inicial
            return velocidad
        
      
    
