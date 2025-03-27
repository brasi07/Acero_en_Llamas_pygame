from src.extras import Settings
from src.tanks import Player
from src.weapons import WeaponPool
import pickle


class Partida:

    def __init__(self, vida, objetos_clave, weapon, world, x=0, y=0, camx=0, camy=0, world_rows = 1, world_columns = 1):
        self.player = Player(vida, objetos_clave)
        self.filas = world_rows
        self.columnas = world_columns
        self.x = x
        self.y = y
        self.camx = camx
        self.camy = camy
        WeaponPool().reset_pool(self.player)
        self.player.cambiar_secundaria(WeaponPool.get_weapon(weapon))
        self.player.armas_pos = weapon
        self.current_stage = world

    def update_save_data(self, camx, camy, rows, col, numb):
        self.camx = camx // Settings.TILE_SIZE
        self.camy = camy // Settings.TILE_SIZE
        self.filas = rows
        self.columnas = col
        self.current_stage = numb
        self.x = self.player.rect_element.x / (self.columnas * Settings.TILE_SIZE)
        self.y = self.player.rect_element.y / (self.filas * Settings.TILE_SIZE)

    def set_save_coords(self, fase):
        fase.player.rect_element.x = int(self.x * (fase.num_columnas * Settings.TILE_SIZE))
        fase.player.rect_element.y = int(self.y * (fase.num_filas * Settings.TILE_SIZE))
        fase.camara_x = self.camx * Settings.TILE_SIZE
        fase.camara_y = self.camy * Settings.TILE_SIZE

    def save(self):
        data = {
            "hp" : self.player.vida,
            "posx" : self.x,
            "posy" : self.y,
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