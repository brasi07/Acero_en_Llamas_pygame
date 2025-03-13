from extras.resourcesmanager import ResourceManager
from weapons import Weapon
from weapons.bullets.Rocket import Rocket


class RocketLauncher(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.sprites = ResourceManager.load_animation(f"weapons{tank.tank_level}_128x128.png", 128, 128, 16)
        self.imagen_canon_base = self.sprites[11]
        self.rocket_counter = 5
        self.posRocket = -30

    def activar_secundaria(self, mundo):
        if self.rocket_counter == 0:
            self.cooldown = 12000
            self.rocket_counter = 5
        else:
            self.cooldown = 200
            self.rocket_counter -= 1

        rocket = Rocket(self, self.posRocket)
        mundo.add_bullet(rocket)

        # Alternar entre -30, -10, 10, y 30 para hacer que los misiles salgan de diferentes lados
        posiciones_ciclo = [-30, -20, -10, 10, 20, 30]
        indice_actual = posiciones_ciclo.index(self.posRocket)
        self.posRocket = posiciones_ciclo[(indice_actual + 1) % len(posiciones_ciclo)]



