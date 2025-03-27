from ..elements import LowWall, Decoracion, Wall
from ..elements.interactable import Button, Trap, IceCube, IceFloor, PickableWeapon
from ..elements.activateable import Door
from ..extras import Settings
from ..tanks.enemies import EnemyRed, EnemyPurple, EnemyGreen, EnemyBrown
from ..tanks.enemies.bosses import WarTrain, MegaCannon, Mecha
from ..weapons import WeaponPool


class ElementFactory:
    @staticmethod
    def create_element(valor, x, y, sprites, puertas, game_instance, id_enemigo):
        """Crea una instancia del elemento correspondiente al valor."""
        if 5100 <= valor <= 5199:  # Puertas
            elemento = Door(x, y, sprites[1315], sprites[4000])
            pos = valor - 5100
            if pos not in puertas:
                puertas[pos] = []
            puertas[pos].append(elemento)
            return elemento

        elif valor == 0:  # Jugador
            game_instance.camara_x = x // (game_instance.ancho_pantalla / Settings.TILE_SIZE) * game_instance.ancho_pantalla
            game_instance.camara_y = y // (game_instance.alto_pantalla / Settings.TILE_SIZE) * game_instance.alto_pantalla
            game_instance.player.establecer_posicion(x * Settings.TILE_SIZE, y * Settings.TILE_SIZE)
            return game_instance.player

        elif 7000 <= valor <= 7399:
            return ElementFactory.crear_enemigo(valor, x, y, id_enemigo)
        elif valor == 7400:
            return Mecha(x, y)
        elif valor == 7401:
            return MegaCannon(x, y)
        elif valor == 7402:
            return WarTrain(x, y)
        elif  valor in game_instance.ice:
            return IceFloor(x,y,sprites[valor])

        elif 5200 <= valor <= 5299:
            return PickableWeapon(x, y, WeaponPool().get_weapon(valor % 100))

        elif 5000 <= valor <= 5099:  # Botones
            pos = valor - 5000
            puertas_a_activar = puertas.get(pos)
            return Button(x, y, sprites[2142], puertas_a_activar, game_instance)
        elif valor in game_instance.traps:
            from . import World1, World2
            if isinstance(game_instance, World1):
                return Trap(x, y, sprites[valor])
            elif isinstance(game_instance, World2):
                return IceCube(x, y, sprites[valor])
            else:
                return Trap(x, y, sprites[valor])
        elif valor in game_instance.lowWalls:
            return LowWall(x, y, sprites[valor])
        elif valor in game_instance.decorations:
            return Decoracion(x, y, sprites[valor])
        elif valor != -1 and valor in sprites:
            return Wall(x, y, sprites[valor])

        return None  # Si no hay un elemento válido

    @staticmethod
    def crear_enemigo(valor, x, y, id_enemigo):
        """Crea un enemigo basado en el valor dado, asignándole tipo, patrullaje y si es élite."""
        tipos_enemigos = {
            0: EnemyBrown,
            1: EnemyGreen,
            2: EnemyPurple,
            3: EnemyRed,
        }

        tipos_patrullas = {
            0: "horizontal",
            1: "vertical",
            3: "torreta",
        }

        base_tipo = (valor % 1000) // 100
        enemy_class = tipos_enemigos.get(base_tipo, EnemyBrown)

        base_patrulla = (valor % 100) // 10
        modo_patrulla = tipos_patrullas.get(base_patrulla, "horizontal")

        elite = False
        if valor % 10 != 0: elite = True

        enemigo = enemy_class(x, y, modo_patrulla, elite=elite, id_mapa=id_enemigo)
        return enemigo
