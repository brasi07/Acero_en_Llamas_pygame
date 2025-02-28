import os.path
from pathlib import Path

import spritesheet
from settings import RESIZE_PLAYER, ELIMINAR_FONDO, TILE_SIZE

import pygame


class ResourceManager(object):
    resources = {}

    @classmethod
    def load_file(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            carpeta_recursos = Path(__file__).parent.parent / 'res'
            image_path = list(carpeta_recursos.rglob(name))

            if image_path:
                cls.resources[name] = image_path[0]
                return cls.resources[name]

            raise FileNotFoundError(f"No se encontró el archivo {name} en {carpeta_recursos}")


    @classmethod
    def escalar_y_cargar_animacion(cls, name, sizex, sizey, numberSprites, resizex=RESIZE_PLAYER, resizey=RESIZE_PLAYER):
        ruta = cls.load_file(name)
        sprite_sheet = spritesheet.SpriteSheet(ruta)
        animacion = sprite_sheet.load_strip((0, 0, sizex, sizey), numberSprites, ELIMINAR_FONDO)
        return [pygame.transform.scale(frame, (resizex * TILE_SIZE, resizey * TILE_SIZE)) for frame in animacion]


    @classmethod
    def generar_sprites(cls, resizex, resizey, nombre):
        sprite_base = cls.escalate_image(nombre+".png", resizex, resizey)
        sprite_base_45 = cls.escalate_image(nombre+"_45.png", resizex, resizey)

        return {
            "arriba": sprite_base,
            "derecha": pygame.transform.rotate(sprite_base, -90),
            "izquierda": pygame.transform.rotate(sprite_base, 90),
            "abajo": pygame.transform.rotate(sprite_base, 180),
            "arriba_izquierda": sprite_base_45,
            "arriba_derecha": pygame.transform.rotate(sprite_base_45, -90),
            "abajo_izquierda": pygame.transform.rotate(sprite_base_45, 90),
            "abajo_derecha": pygame.transform.rotate(sprite_base_45, 180)
        }


    @classmethod
    def escalate_image(cls, name, resizex, resizey):
        image = cls.load_file(name)
        imagen = pygame.image.load(str(image))
        return pygame.transform.scale(imagen, (resizex * TILE_SIZE, resizey * TILE_SIZE))