#from collections.abc import Iterable
#from typing import Any
from pygame import mixer
import pygame, os, random
import csv
import Button
from configuraciones import *

mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Argentina 1985')

font_tittle = pygame.font.Font('fonts/Jueguito.ttf', 34)

#load music and sounds
music_fondo = pygame.mixer.Sound('sounds/No Bombardeen Buenos Aires.mp3')
music_fondo.set_volume(0.3)
music_fondo.play(0,243000)

level_one_song = pygame.mixer.Sound('sounds/No Bombardeen Buenos Aires.mp3')
level_one_song.set_volume(0.3)

jump_sound = pygame.mixer.Sound('sounds/audio_jump.wav')
jump_sound.set_volume(0.5)
shot_sound = pygame.mixer.Sound('sounds/audio_shot.wav')
shot_sound.set_volume(0.5)
grenade_sound = pygame.mixer.Sound('sounds/audio_grenade.wav')
grenade_sound.set_volume(0.5)
item_equip_sound = pygame.mixer.Sound('sounds/item_equip.mp3')
item_equip_sound.set_volume(0.5)
milanga_sound = pygame.mixer.Sound('sounds/milanga_atroden.mp3')
milanga_sound.set_volume(0.5)
coin_sound = pygame.mixer.Sound('sounds/coin.wav')
coin_sound.set_volume(0.5)
cassete_sound = pygame.mixer.Sound('sounds/audio_cassete.mp3')
cassete_sound.set_volume(0.5)


#load images
#icon
icon_image = pygame.image.load('assets/soda_icon.png')
pygame.display.set_icon(icon_image)

#BUTTOM
start_img = pygame.image.load('assets/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('assets/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/img/restart_btn.png').convert_alpha()
#BACKGROUND
menu_image = pygame.image.load('assets/img/background/cassettesss.jpg')
menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH,SCREEN_HEIGHT))

pine_img = pygame.image.load('assets/img/background/pine1.png').convert_alpha()
pine_img_2 = pygame.image.load('assets/img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('assets/img/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('assets/img/background/sky_cloud.png').convert_alpha()

#tile images
images_list = []
for x in range(TILE_TYPES):
	imagen = pygame.image.load(f'assets/img/tile/{x}.png')
	imagen = pygame.transform.scale(imagen, (TILE_SIZE, TILE_SIZE))
	images_list.append(imagen)

#bullet
granade_image = pygame.image.load("assets/img/icons/grenade.png").convert_alpha()
bullet_image = pygame.image.load("assets/img/icons/bullet.png").convert_alpha()
#boxes
health_box_image = pygame.image.load("assets/img/icons/health_box.png").convert_alpha()
ammo_box_image = pygame.image.load("assets/img/icons/ammo_box.png").convert_alpha()
grenade_box_image = pygame.image.load("assets/img/icons/grenade_box.png").convert_alpha()
coin_image = pygame.image.load('assets/img/icons/coin.png').convert_alpha()

#VIDEO TAPES
video_tapes = pygame.image.load('assets/img/videotape.png').convert_alpha()

item_boxes = {
	'Health': health_box_image,
	'Ammo': ammo_box_image,
	'Grenade': grenade_box_image,
	'Coin': coin_image
}

#define fonts
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, color, x, y):
	img = font.render(text, True, color)
	screen.blit(img, (x,y))

def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(sky_img, (x * width - bg_scroll * 0.5  ,0))
		screen.blit(mountain_img,(x * width  - bg_scroll * 0.6 , SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine_img,(x * width  - bg_scroll+0.7, SCREEN_HEIGHT - pine_img.get_height() - 150))
		screen.blit(pine_img_2,(x * width - bg_scroll*0.8, SCREEN_HEIGHT - pine_img.get_height()))
	#pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

def resert_level():
	enemies_group.empty()
	bullet_group.empty()
	explosion_group.empty()
	grenade_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for fila in range(FILAS):
		r = [-1] * COLUMNAS
		data.append(r)

	return data


class Soldier(pygame.sprite.Sprite):
	def __init__(self,char_type, x, y, scale,speed, ammo, grenades):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.score = 0
		self.scores = []
		self.coins = 0

		#balas
		self.ammo = ammo
		self.start_ammo = ammo
		self.shoot_cooldown = 0

		#granadas
		self.grenades = grenades

		#vidas
		self.health = 100
		self.max_health = self.health

		#la direccion indica que mira para la derecha
		self.direction = 1
	
		self.velocidad_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

		#variables ia
		self.idling = False
		self.idling_counter = 0
		self.move_counter = 0
		self.vision = pygame.Rect(0,0,150,5)


		#load all images for the players
		animation_types = ["Idle", "Run", "Jump", "Death"]
		for animation in animation_types:
			#reset temporary list of images
			temp_list = []
			#count number of files the folder	
			numero_de_frames = len(os.listdir(f'assets/img/{self.char_type}/{animation}'))
			for i in range(numero_de_frames):	
				img = pygame.image.load(f'assets/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)


		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self):
		self.update_animation()
		self.check_alive()
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1
	
	def move_enemy_randomly(self):
		"""
		makes the enemy a self movement with random
			and generate a range or rectangle of vision

		"""
		if self.alive and player.alive:
			#si es igual a uno cambia la accion 
			#checkea el idle
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0) #idle - inmovil
				self.idling = True
				self.idling_counter = 50

			#checkeamos si el enemigo esta cerca del jugador
			if self.vision.colliderect(player.rect):
				#se detiene y empieza a disparar al jugador
				self.update_action(0)#:0 = quieto
				#shoot
				self.shoot()
			#si el enemigo no ve al jugador:
			else:
				if self.idling == False:
					if self.direction == 1:
						ia_moving_right = True
					else:
						ia_moving_right = False
					ia_moving_left = not ia_moving_right
					self.update_action(1)#1 Run
					self.move(ia_moving_left, ia_moving_right)
					self.move_counter += 1
					#UPDATE ENEMIES VISION
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
					pygame.draw.rect(screen, RED, self.vision)

					if self.move_counter > TILE_SIZE:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False

		#scrolll
		self.rect.x += screen_scroll

	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0

		dx = 0 #cuanto el jugador se va a mover en cada iteracion 
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump and self.in_air == False:
			self.velocidad_y = -15
			self.jump = False
			self.in_air = True

		#apply gravity
		self.velocidad_y += GRAVITY
		if self.velocidad_y > 10:
			self.velocidad_y
		dy += self.velocidad_y
		
		#check for collision
		for tile in world.obstacle_list:
			#check the collition uin x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
				#if the ia have collied a wall, then turn around
				if self.char_type == 'enemy':
					self.direction *= -1
					self.move_counter = 0


			#check collition in y direction
			if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
				#check if  below the ground, jumping
				if self.velocidad_y < 0: #the player
					self.velocidad_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, ie falling
				elif self.velocidad_y >= 0 :
					self.velocidad_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom

		#check collition with the water
		if pygame.sprite.spritecollide(self, water_group, False):
			#wwwwwwwww
			self.health = 0

		level_complete = False
		if pygame.sprite.spritecollide(self, exit_group, False):
			level_complete = True
		
		#check is fallen out
		if self.rect.bottom > SCREEN_HEIGHT:
			self.health = 0


		#CHECK IF GOING OFF THE EDGES OF SCREEN
		if self.char_type == 'player':
			if self.rect.x + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll base on palyer position
		if self.char_type == 'player':
			if (self.rect.right > SCREEN_WIDTH - SCROLL_LIMITES and bg_scroll < (world.lenght_level * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_LIMITES and bg_scroll > abs(dx)): #indica el valor absoluto de mi delta x  en positivo
				self.rect.x -= dx
				screen_scroll = -dx
		
		return screen_scroll, level_complete

	def update_animation(self):
		#UPDATE ANIMATIONS
		ANIMATION_COOLDOWN = 100
		#uodate image depending on current frames
		self.image = self.animation_list[self.action][self.frame_index]
		#check  if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#RESTART ANIMATION
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3: #deadth
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0
		
	def shoot(self):
		if self.shoot_cooldown == 0 and self.ammo > 0:
			self.shoot_cooldown = 20	
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			#reduce las balas
			self.ammo -= 1
			shot_sound.play()

	def update_action(self, new_action):
		#check if the new action is diferent to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animations settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()
	
	def check_alive(self):
		if self.health <= 0:
			###
			#player.score += 50
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)
	
	def save_score(self, name, score, level):
		
		with open ('score.csv', 'a', newline='') as file:
			write = csv.writer(file)
			write.writerow([name, score, level])

	def read_csv(self, filename):
		
		with open(filename, 'r') as file:
			reader = csv.reader(file)
			for row in reader:
				self.scores.append(row)
		return self.scores

	def draw_ranking(self):
		#height_row = 106

		for ranking in self.scores:
			name = ranking[0]
			score = ranking[1]
			ranking_text = font_tittle.render(f'{name}: {score}', True, "White")
			#draw_text(ranking_text, font_tittle, 'White', SCREEN_HEIGHT - 50, 100)
			screen.blit(ranking_text,(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
		#pygame.draw.rect(screen, RED, self.rect, 1)


###################################################################################################
	
class World():
	def __init__(self):
		#self.lista_de_obstaculos = []
		self.obstacle_list = []

	def process_data(self, data):

		self.lenght_level = len(data[0])#cuantas columnas y cuantos tiles

		#itera sobre cada valor en el archivo de data
		for y, fila in enumerate(data):
			for x, tile in enumerate(fila):
				if tile >= 0:
					img = images_list[tile]
					img_rect = img.get_rect()
					#encuentro la posicon de x e y de la imagen
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)

					if tile >= 0 and tile <= 8: #OBSTACULOS
						self.obstacle_list.append(tile_data)
					elif tile >= 9 and tile <=10:
						water = Water(img,  x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <=	14:
						decoration = Decoration(img,  x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 15: #JUGADOR
						player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 7, 20, 5)
						health_bar = Health_Bar(10,10,player.health, player.max_health)
					elif tile == 16: #ENEMIGO
						enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2,20, 0)
						#enemy_2 = Soldier('enemy', 300, 200, 1.65, 2,20, 0)
						enemies_group.add(enemy)
					elif tile == 17: #create caja de balas
						item_box = ItemBox("Ammo",  x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 18: #create caja de vidas
						item_box = ItemBox("Grenade",  x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 19: #create caja de granadas
						item_box = ItemBox("Health",  x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 20:#crear exit
						exit = Exit(img,  x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)
					elif tile == 21:#coin
						item_box = ItemBox("Coin",  x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)

		return player, health_bar 		

	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll	
			screen.blit(tile[0],tile[1])

class Decoration(pygame.sprite.Sprite):
	def __init__(self, image, x , y):
		pygame.sprite.Sprite.__init__(self)	
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
	def __init__(self, image, x , y):
		pygame.sprite.Sprite.__init__(self)	
		self.image = image
		self.rect  = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, image, x , y):
		pygame.sprite.Sprite.__init__(self)	
		self.image = image
		self.rect  = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x , y):
		pygame.sprite.Sprite.__init__(self)	
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE //2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x +=screen_scroll
		#check if the palyer has picked up the box
		if pygame.sprite.collide_rect(self, player):
			
			#what kind of box it was ?
			if self.item_type == "Health":
				milanga_sound.play()
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == "Ammo":
				item_equip_sound.play()
				player.ammo += 10
			elif self.item_type == "Grenade":
				item_equip_sound.play()
				player.grenades += 3
			elif self.item_type == "Coin":
				coin_sound.play()
				player.coins += 1
				player.score += 10
				print(player.coins)
			#delete item
			self.kill() 

class Health_Bar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update new health
		self.health = health
		#calcular radio dibujado de vidas
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, "Black", (self.x - 2, self.y - 2, 154,24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150,20))
		pygame.draw.rect(screen, "Green", (self.x, self.y, 150 * ratio ,20))

	def update(self):
		pass	
	
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_image
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.direction = direction

	def update(self):
		#move bullet
		self.rect.x += (self.direction * self.speed) + screen_scroll
		#check si se fue de pantalla
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

		#check colision con obstaculos
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):#tile 1 es el rectangulo de la imagen
				#pygame.draw.rect(screen, RED, (tile[1].x , tile[1].y, 50,50))
				self.kill()
		#check colision
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		for enemy in enemies_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					player.score += 25
					self.kill()

class Granade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.timer = 100
		self.velocidad_y = -15
		self.speed = 7
		self.image = granade_image
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.direction = direction
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self):
		self.velocidad_y += GRAVITY
		dx = self.direction * self.speed
		dy = self.velocidad_y

		#update grenade position

		#check colision with plataforms and level
		for tile in world.obstacle_list:

			#check collision walls or plataforms
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				self.direction *= -1
				dx = self.direction * self.speed
			#check collition in y direction
			if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
				self.speed = 0 #se sigue deslizando (podria ser un superpoder)
				#check if  below the ground, thrown up
				if self.velocidad_y < 0: #the player
					self.velocidad_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, ie falling
				elif self.velocidad_y >= 0:
					self.velocidad_y = 0
					dy = tile[1].top - self.rect.bottom

		self.rect.x += dx + screen_scroll
		self.rect.y += dy

		#countdown timer
		self.timer -= 1
		if self.timer <= 0:
			grenade_sound.play()
			self.kill()
			explosion = Explosion(self.rect.x, self.rect.y, 0.5)
			explosion_group.add(explosion)
			#do damege to anyone who is nearby
				#abs no importa si es negativo o positico
			if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
				abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2 :
				player.health -= 50
				#print(player.health)
			for enemy in enemies_group:
				if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
					abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2 :
					enemy.health -= 50
					player.score += 50
					#print(enemy.health)

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1,6):
			img = pygame.image.load(f"assets/img/explosion/exp{num}.png").convert_alpha()
			img = pygame.transform.scale(img,( int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0 

	def update (self):
		#scroll
		self.rect.x += screen_scroll

		EXPLOSION_SPEED = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			#if the animatios is complete then eliminate the explosion
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.color = colour
		self.speed = speed
		self.fade_counter = 0

	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed

		if self.direction == 1:
			pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2: #vertical screen fade
			pygame.draw.rect(screen, self.color, (0,0, SCREEN_WIDTH, 0 + self.fade_counter))

		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete

##########################################################################################

#screen fade
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, 'Black', 4)
end_fade = ScreenFade(1, BLACK, 4)

#buttoms
start_buttom = Button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_buttom = Button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = Button.Button(SCREEN_WIDTH // 2 -110 , SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#sprite groups
enemies_group = pygame.sprite.Group() 
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Creo una lista vacia para mi data
world_data = []
for fila in range(FILAS):
	r = [-1] * COLUMNAS
	world_data.append(r)

#cargo la data de mi nivel y creo el mapa
with open(f"level{level}_data.csv", newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, fila in enumerate(reader):
		for y, tile in enumerate(fila):#obtengo la fila, #tile es igual a cada valor de mi fila	
			world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)

run = True
while run:

	clock.tick(FPS)

	if start_game == False:	
		
		#draw menu
		screen.fill(BG)

		#screen.blit(menu_image,(0,0))

		texto = font_tittle.render("Argentina 1985", True, "White")
		texto_rect = texto.get_rect()
		texto_rect.center = (SCREEN_WIDTH // 2 -210, SCREEN_HEIGHT//2 - 250)
		screen.blit(texto, (SCREEN_WIDTH // 2 -230, SCREEN_HEIGHT//2 - 250))
		#buttoms
		if start_buttom.draw(screen):
			start_game = True
			start_intro = True
		if exit_buttom.draw(screen):
			run = False
	else:
	
		#draw background
		draw_bg()
		#draw world map
		world.draw()

		#health
		health_bar.draw(player.health)

		#show ammo
		draw_text(f"AMMO:  ", font, 'White', 10,35)
		for x in range(player.ammo):
			screen.blit(bullet_image, (90 + (x * 10), 40))
		#show grenade
		draw_text(f"GRENADE: ", font, 'White', 10,60)
		for x in range(player.grenades):
			screen.blit(granade_image, (135 + (x * 15), 60))
		# draw_text(f"Health: {player.health}", font, 'White', 50,50)

		draw_text(f"Score:  {player.score}", font, 'White', SCREEN_WIDTH - 150,35)

		player.update()
		player.draw()

		for enemy in enemies_group:
			enemy.move_enemy_randomly()
			enemy.update()
			enemy.draw()

		#update and draw groups
		bullet_group.update()
		grenade_group.update()
		explosion_group.update()
		item_box_group.update()
		decoration_group.update()
		water_group.update()
		exit_group.update()

		bullet_group.draw(screen)
		grenade_group.draw(screen)
		explosion_group.draw(screen)
		item_box_group.draw(screen)
		decoration_group.draw(screen)
		water_group.draw(screen)
		exit_group.draw(screen)

		#SHOW INTRO
		if start_intro == True:
			
			if intro_fade.fade():
				start_intro = False
				intro_fade.fade_counter = 0

		#update player actions 
		if player.alive:
			#shoot 
			if shoot:
				player.shoot()
			#lanzar granadas
			elif grenade and granada_lanzada == False and player.grenades > 0:
				grenade = Granade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
							player.rect.top , player.direction)
				grenade_group.add(grenade)
				#reduce grenades
				player.grenades -= 1
				granada_lanzada = True
			if player.in_air:
				player.update_action(2)#2:jump
			elif moving_left or moving_right:
				player.update_action(1) #1:means run
			else:
				player.update_action(0)#0: uy quieto
			screen_scroll, level_complete = player.move(moving_left, moving_right)
			bg_scroll -= screen_scroll
			#check if level complete
			if level_complete:
				player.save_score("Catriel", player.score, level)
				start_intro = True
				level += 1
				bg_scroll = 0
				world_data = resert_level()
				if level <= MAX_LEVEL:
					#print(level)
					if level == 4:
						player.alive=False
						
						break
					#Load in level data and create world
					with open(f"level{level}_data.csv", newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, fila in enumerate(reader):
							for y, tile in enumerate(fila):#obtengo la fila, #tile es igual a cada valor de mi fila	
								world_data[x][y] = int(tile)

					world = World()
					player, health_bar = world.process_data(world_data)

		else:	
			#music_fondo.stop()
			screen_scroll = 0 #depende del jugador
			if death_fade.fade():
				if restart_button.draw(screen):
					death_fade.fade_counter = 0
					start_intro = True
					bg_scroll = 0 #poniendo la imagen al comienzo
					world_data = resert_level() #reseteo la lista data de mi mundo

					#Load in level data and create world
					with open(f"level{level}_data.csv", newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, fila in enumerate(reader):
							for y, tile in enumerate(fila):#obtengo la fila, #tile es igual a cada valor de mi fila	
								world_data[x][y] = int(tile)

					world = World()
					player, health_bar = world.process_data(world_data)

				
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_r:
				grenade = True
			if event.key == pygame.K_w and player.alive:
				player.jump  = True
				jump_sound.play()
			if event.key == pygame.K_ESCAPE:
				run = False


		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False	
			if event.key == pygame.K_r:
				grenade = False
				granada_lanzada = False


	pygame.display.update()

pygame.quit()