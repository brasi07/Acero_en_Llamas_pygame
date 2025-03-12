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
            game_instance.camara_x = x // (
                        game_instance.ancho_pantalla / TILE_SIZE) * game_instance.ancho_pantalla
            game_instance.camara_y = y // (
                        game_instance.alto_pantalla / TILE_SIZE) * game_instance.alto_pantalla
            game_instance.player.establecer_posicion(x * TILE_SIZE, y * TILE_SIZE)
            return game_instance.player

        elif 7000 <= valor <= 7009:
            return EnemyBrown(x, y, valor % 10)
        elif 7010 <= valor <= 7019:
            return EnemyGreen(x, y, valor % 10)
        elif 7020 <= valor <= 7029:
            return EnemyPurple(x, y, valor % 10)
        elif 7030 <= valor <= 7039:
            return EnemyRed(x, y, valor % 10)
        elif 7040 <= valor <= 7049:
            return Mecha(x, y, valor % 10)
        elif 7050 <= valor <= 7059:
            return MegaCannon(x, y, valor % 10)
        elif 7060 <= valor <= 7069:
            return WarTrain(x, y, valor % 10)

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
