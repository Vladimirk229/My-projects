import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.rect=self.image.get_rect()
        self.image.fill((255,0,0))
        self.rect.centerx=gun.rect.centerx
        self.rect.centery=gun.rect.centery

    def update(self):
        self.rect.y-=10
        self.score=0
