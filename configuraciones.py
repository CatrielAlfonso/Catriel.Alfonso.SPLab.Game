import pygame

#medidas
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

CENTER = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2)

#colores
BLACK = (0,0,0)
BG = (144, 201, 120)
RED = (255, 0, 0)

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
start_game = False
start_intro = False

#TILE_SIZE = 40
level = 1
FILAS = 16 
TILE_SIZE = SCREEN_HEIGHT // FILAS
TILE_TYPES = 22
COLUMNAS = 150
SCROLL_LIMITES= 200
screen_scroll = 0
bg_scroll = 0
MAX_LEVEL = 3
score = 0
kill_enemy = 20
level_pass = 30
monedas = 10


#define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
granada_lanzada = False
