from elements import Button, Trap, LowWall, Decoracion, Wall, Door
from extras.settings import TILE_SIZE
from tanks import EnemyRed, EnemyPurple, EnemyGreen, EnemyBrown
from tanks.enemies.bosses import WarTrain, MegaCannon, Mecha

class ElementFactory:
    @staticmethod
    def create_element(valor, x, y, sprites, puertas, game_instance):
        """Crea una instancia del elemento correspondiente al valor."""
        if 5100 <= valor <= 5199:  # Puertas
            elemento = Door(x, y, sprites[1315], sprites[580])
            pos = valor - 5100
            if pos not in puertas:
                puertas[pos] = []
            puertas[pos].append(elemento)
            return elemento

        elif valor == 0:  # Jugador
            game_instance.camara_x = x // (game_instance.ancho_pantalla / TILE_SIZE) * game_instance.ancho_pantalla
            game_instance.camara_y = y // (game_instance.alto_pantalla / TILE_SIZE) * game_instance.alto_pantalla
            game_instance.player.establecer_posicion(x * TILE_SIZE, y * TILE_SIZE)
            return game_instance.player

        elif 7000 <= valor <= 7399:
            return ElementFactory.crear_enemigo(valor, x, y)
        elif valor == 7400:
            return Mecha(x, y)
        elif valor == 7401:
            return MegaCannon(x, y)
        elif valor == 7402:
            return WarTrain(x, y)

        elif 5000 <= valor <= 5099:  # Botones
            pos = valor - 5000
            puertas_a_activar = puertas.get(pos)
            return Button(x, y, sprites[2142], puertas_a_activar, game_instance)

        elif valor in game_instance.traps:
            return Trap(x, y, sprites[valor])
        elif valor in game_instance.lowWalls:
            return LowWall(x, y, sprites[valor])
        elif valor in game_instance.decorations:
            return Decoracion(x, y, sprites[valor])
        elif valor != -1 and valor in sprites:
            return Wall(x, y, sprites[valor])

        return None  # Si no hay un elemento válido

    @staticmethod
    def crear_enemigo(valor, x, y):
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
            2: "circular",
            3: "torreta",
        }

        base_tipo = (valor % 1000) // 100
        enemy_class = tipos_enemigos.get(base_tipo, EnemyBrown)

        base_patrulla = (valor % 100) // 10
        modo_patrulla = tipos_patrullas.get(base_patrulla, "horizontal")

        elite = False
        if valor % 10 != 0: elite = True

        enemigo = enemy_class(x, y, modo_patrulla, elite=elite)
        return enemigo
