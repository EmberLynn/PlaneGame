import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                0,(SCREEN_HEIGHT/2)
            )
        )

    def update(self, pressed_keys):
        # update player's position
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)
    # move the sprite
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

pygame.mixer.init()
pygame.init()

pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)# loop forever

move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("sounds/Collision.ogg")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a custom event for enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# custom event for clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clockobject = pygame.time.Clock()

running = True
# Main game loop
while running:

    # use this to control overall frames -- larger = faster
    clockobject.tick(30)

    # loop through list of events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        # Add an enemy based on event triggered
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        # Add a cloud when cloud event is triggered
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # check for key pressed and update player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update all enemies in existence
    enemies.update()

    #update all clouds
    clouds.update()

    screen.fill((66, 135, 245))

    # surf = pygame.Surface((50,50))

    # surf.fill((0,0,0))
    # rect = surf.get_rect()

    # surf_center = (
    #     (SCREEN_WIDTH-surf.get_width())/2,
    #     (SCREEN_HEIGHT-surf.get_height())/2,
    # )

    # screen.blit(surf, surf_center)

    # screen.blit(player.surf, player.rect)
    # draw everyone all at once instead (rendering)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check for collisons
    if pygame.sprite.spritecollideany(player, enemies):
        # end the game if a collison happens
        player.kill()

        # stop all sounds and play collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        running = False

    # pygame.draw.circle(screen, (0,0,255), (250,250), 75)

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()