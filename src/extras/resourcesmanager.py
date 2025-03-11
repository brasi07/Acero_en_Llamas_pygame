import csv
import os
from pathlib import Path

from extras import spritesheet
from extras.settings import RESIZE_PLAYER, ELIMINAR_FONDO, TILE_SIZE, RESIZE_CANNON

import pygame


class ResourceManager(object):
    resources = {}

    @classmethod
    def locate_resource(cls, name):
        carpeta_recursos = Path(__file__).parent.parent.parent / 'res'
        resource = list(carpeta_recursos.rglob(name))

        if resource:
            cls.resources[name] = resource[0]
            return cls.resources[name]

        raise FileNotFoundError(f"No se encontró {name} en {carpeta_recursos}")

    @classmethod
    def load_animation(cls, name, sizex, sizey, number_sprites, resizex=RESIZE_PLAYER, resizey=RESIZE_PLAYER):
        if name in cls.resources and isinstance(cls.resources[name], list):
            return cls.resources[name]

        ruta = cls.locate_resource(name)  # Ubicar el recurso

        sprite_sheet = spritesheet.SpriteSheet(ruta)  # Intentar cargar el spritesheet
        animacion = sprite_sheet.load_strip((0, 0, sizex, sizey), number_sprites, ELIMINAR_FONDO)

        cls.resources[name] = [pygame.transform.scale(frame, (resizex * TILE_SIZE, resizey * TILE_SIZE)) for frame in animacion]

        return cls.resources[name]

    @classmethod
    def load_sprites(cls, resizex, resizey, nombre):

        if nombre in cls.resources:
            return cls.resources[nombre]
        else:
            sprite_base = cls.load_and_scale_image(nombre + ".png", resizex, resizey)
            sprite_base_45 = cls.load_and_scale_image(nombre + "_45.png", resizex, resizey)
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
    def cargar_canon(cls, numberweapon, sprite_type, tank_color):

        if f"{sprite_type}{tank_color}" in cls.resources:
            return cls.resources[f"{sprite_type}{tank_color}"]

        weapon_sprite_sheet = spritesheet.SpriteSheet(ResourceManager.locate_resource(f"{sprite_type}{tank_color}.png"))
        weapon_strip = weapon_sprite_sheet.load_strip((0, 0, 96, 96), 16, ELIMINAR_FONDO)
        weapon_sprites = [pygame.transform.scale(frame, (
        RESIZE_CANNON * TILE_SIZE, RESIZE_CANNON * TILE_SIZE)) for frame in
                          weapon_strip]
        sprite_weapon = weapon_sprites[numberweapon]

        cls.resources[f"{sprite_type}{tank_color}"] = sprite_weapon

        return cls.resources[f"{sprite_type}{tank_color}"]

    @classmethod
    def load_files_from_folder(cls, carpeta):

        if carpeta in cls.resources:
            return cls.resources[carpeta]

        sprites = {}

        for archivo in os.listdir(carpeta):
            if archivo.endswith(".png"):
                id_sprite = archivo.split(".")[0]  # Obtiene el nombre sin la extensión
                sprites[int(id_sprite)] = pygame.image.load(os.path.join(carpeta, archivo))

        cls.resources[carpeta] = sprites

        return sprites

    @classmethod
    def load_map_from_csv(cls, archivo):
        """Carga el mapa desde un archivo CSV y lo convierte en una lista de listas."""

        if archivo in cls.resources:
            return cls.resources[archivo]

        mapa = []
        with open(archivo, newline='') as csvfile:
            lector = csv.reader(csvfile)
            for fila in lector:
                mapa.append([int(valor) for valor in fila])

        cls.resources[archivo] = mapa

        return mapa

    @classmethod
    def buscar_archivos_mapa(cls, mundo_number):
        """Busca archivos que coincidan con el patrón 'Mapa_{mundo}_{capa}.csv'."""

        carpeta = cls.locate_resource("mapas")
        archivos = []

        for archivo in os.listdir(carpeta):
            if archivo.startswith(f"Mapa_{mundo_number}_") and archivo.endswith(".csv"):
                archivos.append(os.path.join(carpeta, archivo))

        return archivos


    @classmethod
    def load_and_scale_image(cls, name, resizex, resizey):

        imagen = cls.load_image(name)
        imagen_escalada = pygame.transform.scale(imagen, (resizex * TILE_SIZE, resizey * TILE_SIZE))

        return imagen_escalada

    @classmethod
    def load_image(cls, name):

        if name in cls.resources:
            return cls.resources[name]
        else:
            image = cls.locate_resource(name)
            imagen = pygame.image.load(str(image))
            cls.resources[name] = imagen
            return imagen