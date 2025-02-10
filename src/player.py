import pygame

class Player:
    def __init__(self):
        # Cargar imágenes del tanque y escalarlas
        self.sprites = {
            "izquierda": self.cargar_y_escalar_imagen("../res/tanque_izquierda.png", 1.5),
            "derecha": self.cargar_y_escalar_imagen("../res/tanque_derecha.png", 1.5),
            "arriba": self.cargar_y_escalar_imagen("../res/tanque_arriba.png", 1.5),
            "abajo": self.cargar_y_escalar_imagen("../res/tanque_abajo.png", 1.5),
            "arriba_izquierda": self.cargar_y_escalar_imagen("../res/tanque_arriba_izquierda.png", 1.5),
            "arriba_derecha": self.cargar_y_escalar_imagen("../res/tanque_arriba_derecha.png", 1.5),
            "abajo_izquierda": self.cargar_y_escalar_imagen("../res/tanque_abajo_izquierda.png", 1.5),
            "abajo_derecha": self.cargar_y_escalar_imagen("../res/tanque_abajo_derecha.png", 1.5),
        }
        self.image = self.sprites["abajo"]
        self.rect = self.image.get_rect(center=(400, 300))
        self.velocidad = 1

    def cargar_y_escalar_imagen(self, ruta, escala):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (imagen.get_width() * escala, imagen.get_height() * escala))

    def update(self, muro):
        teclas = pygame.key.get_pressed()
        direccion = None
        nuevo_rect = self.rect.copy()

        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_derecha"
        elif (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_derecha"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            nuevo_rect.x -= self.velocidad
            direccion = "izquierda"
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            nuevo_rect.x += self.velocidad
            direccion = "derecha"
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            nuevo_rect.y -= self.velocidad
            direccion = "arriba"
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            nuevo_rect.y += self.velocidad
            direccion = "abajo"

        # Verificar colisión con el muro
        if not nuevo_rect.colliderect(muro):
            self.rect = nuevo_rect

        if direccion:
            self.image = self.sprites[direccion]

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
