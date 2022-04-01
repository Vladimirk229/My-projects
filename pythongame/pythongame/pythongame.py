import pygame
import sys
from pygame.sprite import Group
from bullet import Bullet
from ufo import Ino
from stats import Stats
import time
from pygame import mixer
pygame.init()

class Gun():
    def __init__(self, screen):
        self.screen=screen
        self.image=pygame.image.load('images/pixil-frame-0.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        self.rect.centerx=self.screen_rect.centerx
        self.center=float(self.rect.centerx)
        self.rect.bottom=self.screen_rect.bottom
        self.mright=False
        self.mleft=False

    def output(self):
        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        if self.mright and self.rect.right<self.screen_rect.right:
            self.center+=8
        if self.mleft and self.rect.left>0:
            self.center-=8
        self.rect.centerx=self.center

    def create_gun(self):
        self.center=self.screen_rect.centerx

def update(bg_color, screen, stats, sc, gun, bul, inos):
    background_image = pygame.image.load('images/background.jpg')
    screen.blit(background_image, (0, 0))
    sc.show_score()
    bul.update()
    bul.draw(screen)
    gun.output()
    inos.draw(screen)

def update_bullets(screen, stats, sc, inos, bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    collisions=pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score+=len(inos)
            explosion_sound=mixer.Sound('sounds/explosion.wav')
            explosion_sound.play()
        sc.image_score()
    if len(inos)==0:
        bullets.empty()
        create_army(screen, inos)

def create_army(screen, inos):
    ino=Ino(screen)
    ino_width=ino.rect.width
    ino_height=ino.rect.height
    for row_number in range(5):
        for ino_number in range(17):
            ino=Ino(screen)
            ino.x=ino_width+ino_width*ino_number
            ino.y=ino_height+ino_height*row_number
            ino.rect.x=ino.x
            ino.rect.y=ino.rect.height+2*ino.rect.height*row_number
            inos.add(ino)

def gun_kill(stats, screen, gun, inos, bullets):
    if stats.guns_left > 0:
        stats.guns_left-=1
        inos.empty()
        bullets.empty()
        create_army(screen, inos)
        gun.create_gun()
        time.sleep(1)
    else:
        stats.run_game=False
        sys.exit()

def inos_check(stats, screen, gun, inos, bullets, Flag):
    screen_rect=screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom>=screen_rect.bottom:
            gun_kill(stats, screen, gun, inos, bullets)
            break  
    for ino in inos.sprites():
        if ino.rect.left<=screen_rect.left and Flag==False:
            Flag=True
            break
    for ino in inos.sprites():
        if ino.rect.right>=screen_rect.right and Flag==True:
            Flag=False
            break
    inos.update(Flag)
    return Flag

def update_inos(stats, screen, gun, inos, bullets, Flag):
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, gun, inos, bullets)
    return inos_check(stats, screen, gun, inos, bullets, Flag)

class Scores():
    def __init__(self, screen, stats):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.stats=stats
        self.text_color=(0,255,0)
        self.font=pygame.font.SysFont(None, 36)
        self.image_score()

    def image_score(self):
        self.score_img=self.font.render(str(self.stats.score), True, self.text_color, (0,0,0))
        self.score_rect=self.score_img.get_rect()
        self.score_rect.right=self.screen_rect.right-40
        self.score_rect.top=20

    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)

screen=pygame.display.set_mode((1900,1000), pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HWSURFACE)
pygame.display.set_caption("Space invaders")
gun=Gun(screen)
bullets=Group()
inos=Group()
create_army(screen, inos)
stats=Stats()
sc=Scores(screen, stats)
bullet_sound=mixer.Sound('sounds/bullet.wav')
clock = pygame.time.Clock()
Flag=True

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                gun.mright=True
            elif event.key==pygame.K_a:
                gun.mleft=True
            elif event.key==pygame.K_SPACE:
                bullet_sound.play()
                screen.fill((0,0,0))
                new_bullet=Bullet(gun)
                bullets.add(new_bullet)
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                gun.mright=False
            elif event.key==pygame.K_a:
                gun.mleft=False
    if stats.run_game:
        gun.update_gun()
        update((0,0,0), screen, stats, sc, gun, bullets, inos)
        update_bullets(screen, stats, sc, inos, bullets)
        Flag=update_inos(stats, screen, gun, inos, bullets, Flag)
        pygame.display.update()
        clock.tick(60)
