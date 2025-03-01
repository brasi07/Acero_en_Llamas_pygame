from pathlib import Path

import spritesheet
from settings import RESIZE_PLAYER, ELIMINAR_FONDO, TILE_SIZE

import pygame


class ResourceManager(object):
    resources = {}

    @classmethod
    def locate_file(cls, name):
        carpeta_recursos = Path(__file__).parent.parent / 'res'
        image_path = list(carpeta_recursos.rglob(name))

        if image_path:
            cls.resources[name] = image_path[0]
            return cls.resources[name]

        raise FileNotFoundError(f"No se encontró el archivo {name} en {carpeta_recursos}")


    @classmethod
    def load_animation(cls, name, sizex, sizey, number_sprites, resizex=RESIZE_PLAYER, resizey=RESIZE_PLAYER):

        if name in cls.resources:
            return cls.resources[name]
        else:
            ruta = cls.locate_file(name)
            sprite_sheet = spritesheet.SpriteSheet(ruta)
            animacion = sprite_sheet.load_strip((0, 0, sizex, sizey), number_sprites, ELIMINAR_FONDO)
            cls.resources[name] =  [pygame.transform.scale(frame, (resizex * TILE_SIZE, resizey * TILE_SIZE)) for frame in animacion]
            return cls.resources[name]


    @classmethod
    def load_sprites(cls, resizex, resizey, nombre):

        if nombre in cls.resources:
            return cls.resources[nombre]
        else:
            sprite_base = cls.load_image(nombre + ".png", resizex, resizey)
            sprite_base_45 = cls.load_image(nombre + "_45.png", resizex, resizey)
            conjunto_sprites = {
                "arriba": sprite_base,
                "derecha": pygame.transform.rotate(sprite_base, -90),
                "izquierda": pygame.transform.rotate(sprite_base, 90),
                "abajo": pygame.transform.rotate(sprite_base, 180),
                "arriba_izquierda": sprite_base_45,
                "arriba_derecha": pygame.transform.rotate(sprite_base_45, -90),
                "abajo_izquierda": pygame.transform.rotate(sprite_base_45, 90),
                "abajo_derecha": pygame.transform.rotate(sprite_base_45, 180)
            }

            cls.resources[nombre] = conjunto_sprites

            return conjunto_sprites


    @classmethod
    def load_image(cls, name, resizex, resizey):

        if name in cls.resources:
            return cls.resources[name]
        else:
            image = cls.locate_file(name)
            imagen = pygame.image.load(str(image))
            imagen_escalada = pygame.transform.scale(imagen, (resizex * TILE_SIZE, resizey * TILE_SIZE))
            cls.resources[name] = imagen_escalada
            return imagen_escalada