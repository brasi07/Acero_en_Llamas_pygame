import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla en modo pantalla completa
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Tanque Mazmorra")
pygame.mouse.set_visible(False)  # Ocultar el cursor del ratón

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)


# Cargar imágenes del tanque y escalarlas
def cargar_y_escalar_imagen(ruta, escala):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (imagen.get_width() * escala, imagen.get_height() * escala))

tank_size = 1
tanque_sprites = {
    "izquierda": cargar_y_escalar_imagen("res/tanque_izquierda.png", tank_size),
    "derecha": cargar_y_escalar_imagen("res/tanque_derecha.png", tank_size),
    "arriba": cargar_y_escalar_imagen("res/tanque_arriba.png", tank_size),
    "abajo": cargar_y_escalar_imagen("res/tanque_abajo.png", tank_size),
    "arriba_izquierda": cargar_y_escalar_imagen("res/tanque_arriba_izquierda.png", tank_size),
    "arriba_derecha": cargar_y_escalar_imagen("res/tanque_arriba_derecha.png", tank_size),
    "abajo_izquierda": cargar_y_escalar_imagen("res/tanque_abajo_izquierda.png", tank_size),
    "abajo_derecha": cargar_y_escalar_imagen("res/tanque_abajo_derecha.png", tank_size),
}

# Inicializar tanque
tanque_img = tanque_sprites["abajo"]
tanque_rect = tanque_img.get_rect()
tanque_rect.center = (ANCHO // 2, ALTO // 2)

# Definir un muro
muro = pygame.Rect(350, 200, 100, 25)  # (x, y, ancho, alto)

# Velocidad del tanque
velocidad = 1

# Bucle principal
ejecutando = True
while ejecutando:
    pantalla.fill(NEGRO)  # Fondo negro

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            ejecutando = False

    # Movimiento del tanque
    teclas = pygame.key.get_pressed()
    direccion = None

    nuevo_rect = tanque_rect.copy()
    if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
        nuevo_rect.x -= velocidad
        nuevo_rect.y -= velocidad
        direccion = "arriba_izquierda"
    elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
        nuevo_rect.x += velocidad
        nuevo_rect.y -= velocidad
        direccion = "arriba_derecha"
    elif (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
        nuevo_rect.x -= velocidad
        nuevo_rect.y += velocidad
        direccion = "abajo_izquierda"
    elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
        nuevo_rect.x += velocidad
        nuevo_rect.y += velocidad
        direccion = "abajo_derecha"
    elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        nuevo_rect.x -= velocidad
        direccion = "izquierda"
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        nuevo_rect.x += velocidad
        direccion = "derecha"
    elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
        nuevo_rect.y -= velocidad
        direccion = "arriba"
    elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        nuevo_rect.y += velocidad
        direccion = "abajo"

    # Verificar colisión con el muro
    if not nuevo_rect.colliderect(muro):
        tanque_rect = nuevo_rect

    # Cambiar el sprite del tanque según la dirección
    if direccion:
        tanque_img = tanque_sprites[direccion]

    # Dibujar el muro
    pygame.draw.rect(pantalla, BLANCO, muro)

    # Dibujar el tanque
    pantalla.blit(tanque_img, tanque_rect)

    # Actualizar pantalla
    pygame.display.flip()

    # Control de FPS
    pygame.time.Clock().tick(60)

pygame.quit()
