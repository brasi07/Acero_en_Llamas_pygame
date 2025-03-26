from src.tanks import Player
from src.weapons import WeaponPool
import pickle


class Partida:

    def __init__(self, vida, objetos_clave, weapon, world, x=0, y=0, camx=0, camy=0):
        self.player = Player(vida, objetos_clave)
        self.x = x
        self.y = y
        self.camx = camx
        self.camy = camy
        WeaponPool().reset_pool(self.player)
        self.player.cambiar_secundaria(WeaponPool.get_weapon(weapon))
        self.player.armas_pos = weapon
        self.current_stage = world

    def save(self):
        print(WeaponPool.get_weapon_number(self.player))
        data = {
            "hp" : self.player.vida,
            "posx" : self.player.rect_element.x,
            "posy" : self.player.rect_element.y,
            "weapon" : WeaponPool.get_weapon_number(self.player),
            "key_obj" : self.player.key_objs,
            "world" : self.current_stage,
            "camx" : self.camx,
            "camy" : self.camy
        }
        with open("save.pkl", "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def load(archivo="save.pkl"):
        try:
            with open(archivo, "rb") as f:
                datos = pickle.load(f)
                return Partida(
                    datos["hp"],
                    datos["key_obj"],
                    datos["weapon"],
                    datos["world"],
                    x=datos["posx"],
                    y=datos["posy"],
                    camx=datos["camx"],
                    camy=datos["camy"]
                )
        except FileNotFoundError:
            print("No se encontró la partida guardada.")
            return None